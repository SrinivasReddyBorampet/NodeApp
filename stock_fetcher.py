import requests
import os
import smtplib
from email.mime.text import MIMEText
import socket # For socket.gaierror
import logging

# --- Logging Configuration ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # Set default level to INFO; can be changed to DEBUG for more verbosity

# File handler
try:
    file_handler = logging.FileHandler('stock_fetcher.log', mode='a') # Append mode
    file_handler.setLevel(logging.INFO) # Set level for file handler
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except IOError:
    # This might happen in environments where file writing is restricted.
    # Fallback to console logging or handle as appropriate.
    print("Warning: Could not open stock_fetcher.log for writing. Logging to console only for this session.")
    # Optionally, add a console handler here as a fallback if file logging fails
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # console_handler.setFormatter(console_formatter)
    # logger.addHandler(console_handler)


# Basic console message if logger has no handlers (e.g. file failed AND no console handler added above)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__) # re-get logger after basicConfig
    logger.warning("File logger failed to initialize and no other handlers configured. Using basicConfig for console logging.")


# --- End Logging Configuration ---

def fetch_stock_price(api_key, symbol):
    """
    Fetches the stock price for a given symbol using Alpha Vantage API.

    Args:
        api_key: Your Alpha Vantage API key. (Note: Will not be logged)
        symbol: The stock symbol (e.g., "AMZN").

    Returns:
        A tuple containing the stock symbol and its price, or None if an error occurs.
    """
    logger.info(f"Initiating stock price fetch for symbol: {symbol}")
    # Construct URL without logging the API key directly.
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    try:
        # Redact API key if logging URL for debugging (though generally avoid logging URLs with keys)
        logger.debug(f"Requesting URL: {url.replace(api_key, 'REDACTED_API_KEY') if api_key else url}")
        response = requests.get(url, timeout=10) # Added timeout
        logger.info(f"API response status code for {symbol}: {response.status_code}")
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()
        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            price = data["Global Quote"]["05. price"]
            logger.info(f"Successfully fetched price for {symbol}: {price}")
            return symbol, price
        elif "Error Message" in data: # Specific error from Alpha Vantage
            error_msg = data['Error Message']
            logger.error(f"Alpha Vantage API error for {symbol}: {error_msg}")
            print(f"API Error for {symbol}: {error_msg}")
            return symbol, None
        elif "Note" in data: # API call limit reached or other informational note
            note_msg = data['Note']
            logger.warning(f"Alpha Vantage API note for {symbol}: {note_msg}")
            print(f"API Note for {symbol}: {note_msg}") # Often this is a "thank you for using" message on success too
            # Check if price is also available despite the note
            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                 price = data["Global Quote"]["05. price"]
                 logger.info(f"Price found for {symbol} despite API note: {price}")
                 return symbol, price
            return symbol, None # If only a note and no price
        else:
            logger.error(f"Unexpected API response format for {symbol}. Full response: {data}")
            print(f"Error: Unexpected response format for {symbol}. See logs for full response.")
            return symbol, None
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error fetching data for {symbol}: {e}. Response: {e.response.text if e.response else 'No response text'}", exc_info=True)
        print(f"Error fetching data for {symbol}: HTTP Error - {e}. Check logs.")
        return symbol, None
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error fetching data for {symbol}: {e}", exc_info=True)
        print(f"Error fetching data for {symbol}: Connection Error - {e}. Check logs.")
        return symbol, None
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout error fetching data for {symbol}: {e}", exc_info=True)
        print(f"Error fetching data for {symbol}: Timeout - {e}. Check logs.")
        return symbol, None
    except requests.exceptions.RequestException as e: # Catch-all for other requests issues
        logger.error(f"Request exception fetching data for {symbol}: {e}", exc_info=True)
        print(f"Error fetching data for {symbol}: Request Error - {e}. Check logs.")
        return symbol, None
    except ValueError as e: # Includes JSONDecodeError if response is not valid JSON
        logger.error(f"JSON parsing error or value error for {symbol}: {e}. Response text: {response.text if 'response' in locals() and hasattr(response, 'text') else 'Response object not available or no text attribute'}", exc_info=True)
        print(f"Error: Could not parse server response for {symbol}. Check logs.")
        return symbol, None
    except KeyError as e:
        logger.error(f"KeyError: Likely missing 'Global Quote' or '05. price' in response for {symbol}. Missing key: {e}. Data: {data if 'data' in locals() else 'Data not parsed'}", exc_info=True)
        print(f"Error: Unexpected response structure from API for {symbol}. Check logs.")
        return symbol, None
    except Exception as e: # Catch any other unexpected errors
        logger.critical(f"An critical unexpected error occurred while fetching price for {symbol}: {e}", exc_info=True)
        print(f"An critical unexpected error occurred for {symbol}. Check logs for details.")
        return symbol, None

def format_prices_for_email(stock_data):
    """
    Formats a list of stock data into a string for an email.

    Args:
        stock_data: A list of tuples, where each tuple contains a stock symbol and its price.
                    Example: [('AMZN', '150.00'), ('NVDA', '450.00')]

    Returns:
        A formatted string with stock prices, or a message if no data is available.
    """
    if not stock_data:
        return "No stock data available."

    formatted_string = "Stock Prices:\n"
    for symbol, price in stock_data:
        if price is not None:
            try:
                # Attempt to format price as currency, assuming it's a string that can be converted to float
                formatted_string += f"{symbol}: ${float(price):.2f}\n"
            except ValueError:
                # Handle cases where price might not be a valid number string
                formatted_string += f"{symbol}: {price} (unable to format as currency)\n"
        else:
            formatted_string += f"{symbol}: Data not available\n"
    return formatted_string.strip()

def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_password):
    """
    Sends an email using SMTP.

    Args:
        subject: The subject of the email.
        body: The body of the email.
        to_email: The recipient's email address.
        from_email: The sender's email address.
        smtp_server: The SMTP server address.
        smtp_port: The SMTP server port.
        smtp_user: The SMTP username. (Note: Will not be logged directly)
        smtp_password: The SMTP password. (Note: Will not be logged)

    Returns:
        True if the email was sent successfully, False otherwise.
    """
    # Log basic info, be careful with sensitive details.
    logger.info(f"Initiating email send. Subject: '{subject}', To: {to_email}, From: {from_email}, Server: {smtp_server}:{smtp_port}, User: {smtp_user}")
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        if smtp_port == 465:  # Standard SSL port
            logger.debug(f"Connecting to SMTP server {smtp_server}:{smtp_port} using SMTP_SSL.")
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=15) # Added timeout
        else:  # Standard TLS port
            logger.debug(f"Connecting to SMTP server {smtp_server}:{smtp_port} using SMTP with STARTTLS.")
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=15) # Added timeout
            server.ehlo()
            server.starttls()
            server.ehlo()
        
        # Do not log smtp_password. Log username only if necessary for debugging and if policy allows.
        logger.debug(f"Logging into SMTP server with user: {smtp_user}.")
        server.login(smtp_user, smtp_password) # Password not logged
        logger.info(f"Sending email to {to_email}.")
        server.sendmail(from_email, to_email, msg.as_string())
        server.close()
        logger.info("Email sent successfully!")
        print("Email sent successfully!")
        return True
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP authentication failed for user {smtp_user} on {smtp_server}:{smtp_port}. Error: {e}", exc_info=True)
        print("Error: SMTP authentication failed. Check username/password and SMTP settings (e.g., 'App Password' for Gmail). See logs.")
    except socket.gaierror as e: # DNS resolution error
        logger.error(f"Socket/DNS error: Could not connect to SMTP server '{smtp_server}'. Error: {e}", exc_info=True)
        print(f"Error: Could not connect to SMTP server '{smtp_server}'. Check server address, port, and network. See logs.")
    except smtplib.SMTPConnectError as e:
        logger.error(f"SMTP connect error for {smtp_server}:{smtp_port}. Error: {e}", exc_info=True)
        print(f"Error: Could not connect to SMTP server at {smtp_server}:{smtp_port}. Check server/port and firewall. See logs.")
    except smtplib.SMTPServerDisconnected as e:
        logger.warning(f"SMTP server disconnected unexpectedly. Server: {smtp_server}:{smtp_port}. Error: {e}", exc_info=True)
        print("Error: SMTP server disconnected unexpectedly. See logs.")
    except smtplib.SMTPException as e: # Catch other smtplib specific errors
        logger.error(f"An SMTP exception occurred while sending email. Error: {e}", exc_info=True)
        print(f"An SMTP error occurred: {e}. See logs.")
    except Exception as e: # Catch-all for other errors
        logger.critical(f"An critical unexpected error occurred while sending email: {e}", exc_info=True)
        print(f"An critical unexpected error occurred while sending email. Check logs for details.")
    return False

if __name__ == '__main__':
    logger.info("--- Stock Fetcher Script Started ---")
    symbols = ["AMZN", "NVDA", "GOOG"]
    # For automated scripts, API keys and credentials should come from env vars or a secure config file.
    # The script currently prompts for API key, which is fine for interactive use.
    # For email, it uses placeholders or environment variables.
    
    api_key_input = input("Enter your Alpha Vantage API key: ")
    # Log only the presence or length of the API key, not the key itself.
    if api_key_input:
        logger.info("Alpha Vantage API key provided by user (length: %d).", len(api_key_input))
    else:
        logger.warning("Alpha Vantage API key not provided by user.")


    if not api_key_input:
        print("API key is required to fetch stock prices.")
        logger.error("Script cannot proceed without API key.")
    else:
        logger.info(f"Processing symbols: {', '.join(symbols)}")
        fetched_prices_count = 0
        fetched_data_list = [] # Renamed from fetched_prices to avoid confusion with count

        for symbol_to_fetch in symbols:
            logger.info(f"Attempting to fetch price for symbol: {symbol_to_fetch}")
            # Pass api_key_input directly; fetch_stock_price handles logging carefully.
            result = fetch_stock_price(api_key_input, symbol_to_fetch)
            
            if result and result[1] is not None:
                fetched_data_list.append(result)
                fetched_prices_count += 1
                logger.info(f"Successfully processed and stored data for symbol: {symbol_to_fetch}")
            elif result and result[1] is None:
                # Error or note already logged in fetch_stock_price
                fetched_data_list.append((symbol_to_fetch, None)) # Store placeholder for formatting
                logger.warning(f"Failed to get price for symbol: {symbol_to_fetch}, storing as (Symbol, None).")
            else:
                # This case implies an unexpected return from fetch_stock_price (e.g. it returned None itself)
                logger.error(f"Unexpected issue fetching data for {symbol_to_fetch}. `fetch_stock_price` returned None or an invalid result.")
                print(f"Failed to fetch data for {symbol_to_fetch} due to an unexpected internal issue. Check logs.")
                fetched_data_list.append((symbol_to_fetch, None)) # Store placeholder

        logger.info(f"Finished fetching all symbols. Successfully fetched prices for {fetched_prices_count}/{len(symbols)} symbols.")
        
        formatted_stock_data = format_prices_for_email(fetched_data_list)
        logger.info("Formatted stock data for email:\n%s", formatted_stock_data) # Log the actual data being sent (if not too large)
        print("\n--- Formatted Stock Prices ---")
        print(formatted_stock_data)

        # --- Email Configuration ---
        # Using environment variables is preferred for credentials in automated scripts.
        # Placeholders are fallback.
        TO_EMAIL = os.environ.get("TO_EMAIL", "recipient_email@example.com")
        FROM_EMAIL = os.environ.get("FROM_EMAIL", "your_email@example.com")
        SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        SMTP_PORT_STR = os.environ.get("SMTP_PORT", "587")
        SMTP_USER = os.environ.get("SMTP_USER", FROM_EMAIL) # Often same as FROM_EMAIL
        SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD") # No default for password

        try:
            SMTP_PORT = int(SMTP_PORT_STR)
        except ValueError:
            logger.error(f"Invalid SMTP_PORT: '{SMTP_PORT_STR}'. Must be an integer. Defaulting to 587.")
            print(f"Warning: Invalid SMTP_PORT configured ('{SMTP_PORT_STR}'). Using default 587.")
            SMTP_PORT = 587

        # Log email configuration details, except for the password.
        logger.info(f"Email Configuration - To: {TO_EMAIL}, From: {FROM_EMAIL}, Server: {SMTP_SERVER}:{SMTP_PORT}, User: {SMTP_USER}, Password Set: {'Yes' if SMTP_PASSWORD else 'No'}")

        print("\n--- Email Sending ---")

        # Check if essential email parameters are placeholders or missing (especially password)
        placeholders_used = (
            TO_EMAIL == "recipient_email@example.com" or
            FROM_EMAIL == "your_email@example.com" or
            SMTP_USER == "your_email@example.com" # If SMTP_USER defaults to FROM_EMAIL which is placeholder
        )
        critical_missing = not SMTP_PASSWORD # Password is critical

        if placeholders_used or critical_missing:
            warning_msg = []
            if placeholders_used:
                warning_msg.append("Default placeholder email values (recipient, sender, or server details) are being used.")
            if critical_missing:
                warning_msg.append("SMTP_PASSWORD is not set.")
            
            full_warning = " ".join(warning_msg)
            logger.warning(f"Email sending check: {full_warning}")
            print(f"WARNING: {full_warning}")
            print("To use actual email settings, ensure TO_EMAIL, FROM_EMAIL, SMTP_SERVER, SMTP_PORT, SMTP_USER, and especially SMTP_PASSWORD are correctly set (e.g., via environment variables or by modifying the script).")

            # Prompt for sending only if interactive and password is set (even if other placeholders are used)
            if os.isatty(0) and os.isatty(1): # Basic check for interactive terminal
                if critical_missing:
                    print("Email cannot be sent without SMTP_PASSWORD.")
                    logger.error("Email sending skipped: SMTP_PASSWORD is not configured.")
                else: # Password is set, but other placeholders might be active
                    send_attempt = input("Do you want to attempt to send the email with the current (potentially placeholder) settings? (yes/no): ").lower()
                    if send_attempt == 'yes':
                        logger.info("User opted to proceed with potentially placeholder email configuration (password is set).")
                        send_email("Daily Stock Price Report", formatted_stock_data, TO_EMAIL, FROM_EMAIL, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD)
                    else:
                        logger.info("Email sending skipped by user decision (placeholders active).")
                        print("Email sending skipped by user.")
            else: # Non-interactive mode
                logger.warning(f"Running in non-interactive mode. {full_warning} Email sending will be skipped.")
                print(f"Non-interactive mode: {full_warning} Email sending skipped. Configure settings properly for automated emails.")
        else:
            logger.info("Attempting to send email with fully configured credentials.")
            send_email("Daily Stock Price Report", formatted_stock_data, TO_EMAIL, FROM_EMAIL, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD)
            
    logger.info("--- Stock Fetcher Script Finished ---")
