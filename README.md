# Stock Price Email Notifier

## Description

This script fetches current stock prices for a predefined list of symbols (AMZN, NVDA, GOOG) using the Alpha Vantage API. It then formats this information and sends it as an email notification. The script also includes logging for monitoring and troubleshooting.

## Features

*   Fetches real-time stock prices from Alpha Vantage (`GLOBAL_QUOTE` endpoint).
*   Sends formatted stock price information via email.
*   Supports configuration of email recipients, sender details, and SMTP server settings.
*   Uses environment variables for sensitive email credentials (recommended).
*   Logs script activity, API responses, and errors to `stock_fetcher.log`.
*   Includes instructions for manual execution and automated scheduling.

## Setup Instructions

### 1. Get the Script
Clone this repository or download the `stock_fetcher.py` script and `requirements.txt` file.

```bash
# If git is installed:
# git clone <repository_url>
# cd <repository_directory>
```

### 2. Create a Python Virtual Environment (Recommended)
It's highly recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Install the required `requests` library:

```bash
pip install -r requirements.txt
```

### 4. Alpha Vantage API Key
An API key from Alpha Vantage is required to fetch stock data.
*   You can get a free API key from [Alpha Vantage Support Page](https://www.alphavantage.co/support/#api-key).
*   The script will prompt you to enter this key when run manually. For automated execution, see the "Scheduling" section for crucial modifications.

### 5. Email Configuration
The script needs to be configured with your email details to send notifications. The following variables are used in `stock_fetcher.py` and can be set up primarily using environment variables for security:

*   `TO_EMAIL`: The recipient's email address.
    *   Default placeholder: `"recipient_email@example.com"`
    *   Set via environment variable: `export TO_EMAIL="your_recipient@example.com"` (Linux/macOS) or set in your system's environment variables (Windows).
*   `FROM_EMAIL`: The sender's email address (this will appear as the "From" field in the email).
    *   Default placeholder: `"your_email@example.com"`
    *   Set via environment variable: `export FROM_EMAIL="your_sender_email@example.com"`
*   `SMTP_SERVER`: Your SMTP server address.
    *   Default placeholder: `"smtp.gmail.com"`
    *   Set via environment variable: `export SMTP_SERVER="smtp.yourprovider.com"`
*   `SMTP_PORT`: The SMTP server port (e.g., 587 for TLS, 465 for SSL).
    *   Default placeholder: `587`
    *   Set via environment variable: `export SMTP_PORT="587"`
*   `SMTP_USER`: Your SMTP username (often the same as `FROM_EMAIL`).
    *   Default placeholder: Value of `FROM_EMAIL` (which itself might be a placeholder).
    *   **Strongly recommend setting via environment variable**: `export SMTP_USER="your_smtp_username"`
*   `SMTP_PASSWORD`: Your SMTP password (or App Password if using services like Gmail with 2FA).
    *   **No default placeholder for security.** The script relies on this being set, preferably as an environment variable.
    *   **MUST be set via environment variable for secure operation**: `export SMTP_PASSWORD="your_smtp_password_or_app_password"`

**Security Note**: It is strongly recommended to use environment variables for `SMTP_USER` and `SMTP_PASSWORD` rather than hardcoding them directly into the script, especially for `SMTP_PASSWORD`. The script is designed to read these from environment variables.

## Running the Script Manually

1.  Open your terminal or command prompt.
2.  Navigate to the directory where `stock_fetcher.py` is located.
3.  Ensure your virtual environment is activated (if you created one).
4.  Run the script:
    ```bash
    python stock_fetcher.py
    ```
5.  The script will prompt you to enter your Alpha Vantage API key.
6.  If email environment variables (especially `SMTP_PASSWORD`) are not set, the script will warn you and may prompt for confirmation before attempting to send an email with placeholder/incomplete details. For successful manual runs, ensure these are set appropriately.

## Scheduling the Script (Automation)

To run the script automatically at regular intervals (e.g., market open and close), you can use cron (Linux/macOS) or Task Scheduler (Windows).

**VERY IMPORTANT FOR AUTOMATION:**
The script, as currently written for interactive use, prompts for the Alpha Vantage API key. For automated execution (cron jobs or scheduled tasks), **you MUST modify `stock_fetcher.py` to obtain the API key non-interactively.** The recommended way is to read it from an environment variable, similar to how email credentials are handled.

**Example Modification in `stock_fetcher.py` (around line 168):**
```python
# Current interactive prompt:
# api_key_input = input("Enter your Alpha Vantage API key: ")

# Replace with or modify to use an environment variable for automation:
# api_key_input = os.environ.get("ALPHA_VANTAGE_API_KEY")
# if not api_key_input:
#     logger.error("ALPHA_VANTAGE_API_KEY environment variable not set.")
#     # Decide how to handle this: exit, or skip fetching, etc.
#     # For now, let's assume it must be set for automation:
#     print("ALPHA_VANTAGE_API_KEY environment variable not set. Cannot run in automated mode without it.")
#     exit(1) # Or handle more gracefully
```
**Failure to make the API key input non-interactive will cause scheduled tasks to hang or fail.** Similarly, ensure all email credentials (`TO_EMAIL`, `FROM_EMAIL`, `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, and especially `SMTP_PASSWORD`) are set as environment variables so no prompts are needed.

---
*The following instructions are adapted from `scheduling_instructions.md`.*

# Scheduling stock_fetcher.py for Regular Execution

This guide provides instructions on how to schedule the `stock_fetcher.py` script to run automatically at specified times using Cron (for Linux/macOS) or Task Scheduler (for Windows).

The goal is to fetch stock prices twice on trading days:
*   **9:30 AM Eastern Time (ET)** (typically market open)
*   **4:30 PM Eastern Time (ET)** (typically after market close)

## 1. Important: Time Zones

Cron and Task Scheduler use the server's local time zone. You **must** convert 9:30 AM ET and 4:30 PM ET to your server's local time to set the correct schedule.

*   **Example**: If your server is in Central Time (CT), which is ET -1 hour:
    *   9:30 AM ET becomes 8:30 AM CT.
    *   4:30 PM ET becomes 3:30 PM CT.
*   Use an online time zone converter or your system's date utilities to find the correct offset.

## 2. Using Cron (Linux/macOS)

Cron is a time-based job scheduler in Unix-like operating systems.

### a. Open Crontab Editor
Open your user's crontab file for editing by running:
```bash
crontab -e
```
If it's your first time, you might be asked to choose an editor (e.g., nano, vim).

### b. Add Cron Entries
Add the following lines to the crontab file. **Adjust the times according to your server's local time zone equivalent of 9:30 AM ET and 4:30 PM ET.** Also, replace `/usr/bin/python3` with the actual path to your Python 3 interpreter and `/path/to/stock_fetcher.py` with the absolute path to the script.

The format is: `MINUTE HOUR * * DAY_OF_WEEK COMMAND`
*   `*` means "any value".
*   `DAY_OF_WEEK`: 1-5 represents Monday to Friday (common trading days).

**Example (assuming server is in ET and script is in `/home/user/scripts/`):**
```cron
# Run at 9:30 AM ET, Monday to Friday
30 9 * * 1-5 /usr/bin/python3 /home/user/scripts/stock_fetcher.py

# Run at 4:30 PM ET, Monday to Friday
30 16 * * 1-5 /usr/bin/python3 /home/user/scripts/stock_fetcher.py
```

**Important:**
*   **Absolute Paths**: Always use absolute paths for both the Python interpreter and the script file.
*   **Permissions**: Ensure `stock_fetcher.py` is executable or readable by the Python interpreter.
*   **Environment Variables**: For cron jobs, environment variables (like `ALPHA_VANTAGE_API_KEY`, `TO_EMAIL`, `FROM_EMAIL`, `SMTP_USER`, `SMTP_PASSWORD`, etc.) must be explicitly set for the cron execution context. Some ways to do this:
    *   Define them at the top of your crontab file (e.g., `SMTP_PASSWORD="yourpassword"`). This is generally readable in the crontab, so consider security.
    *   Source a separate, secured file with the exports: `30 9 * * 1-5 . /home/user/.env_vars; /usr/bin/python3 /path/to/stock_fetcher.py` (ensure `.env_vars` is protected).
    *   Set them directly in the command (less secure as they appear in process list): `30 9 * * 1-5 SMTP_PASSWORD="pass" /usr/bin/python3 /path/to/stock_fetcher.py`

### c. Save and Exit
Save the crontab file and exit the editor.

### d. Checking Cron Logs
Check logs via `grep CRON /var/log/syslog` (Debian/Ubuntu) or `/var/log/cron` (RedHat/CentOS). Redirect script output for more detailed logs from the script itself (including Python errors):
```cron
30 9 * * 1-5 /usr/bin/python3 /path/to/stock_fetcher.py >> /path/to/stock_fetcher_cron_output.log 2>&1
```
Also, check `stock_fetcher.log` as configured within the script.

## 3. Using Task Scheduler (Windows)

### a. Open Task Scheduler
Search for "Task Scheduler" in the Start Menu.

### b. Create a Basic Task
1.  **Name/Description**: e.g., "Fetch Stock Prices AM".
2.  **Trigger**: "Daily", set local time equivalent of 9:30 AM ET.
3.  **Action**: "Start a program".
    *   **Program/script**: Path to `python.exe` (e.g., `C:\Python39\python.exe` or your venv path: `C:\path\to\venv\Scripts\python.exe`).
    *   **Add arguments**: Absolute path to `stock_fetcher.py`.
    *   **Start in**: Absolute path to the directory containing `stock_fetcher.py`.
4.  **Finish**. Repeat for a 4:30 PM ET task.

### c. Weekdays Only & Environment Variables
*   Edit the task trigger for weekdays (e.g., set to "Weekly" and select Mon-Fri).
*   For environment variables in Task Scheduler:
    *   Set them globally for the user account under which the task will run (System Properties -> Environment Variables). This is the most common method.
    *   Alternatively, use a wrapper batch script as the "program" in Task Scheduler. The batch script would first set environment variables (`SET VARNAME=value`) and then call the Python script.

### d. Checking Task History
Use the "History" tab in Task Scheduler for troubleshooting execution issues. Also, check `stock_fetcher.log`.

## 4. General Advice for Automated Execution (Recap)

*   **Test Manually First**: Ensure the script runs flawlessly with your non-interactive credential setup (all keys/passwords as environment variables).
*   **Secure Credential Management**: **Modify the script to read ALL sensitive data (API key, email details) non-interactively from environment variables.**
*   **Logging**: The script logs to `stock_fetcher.log`. This is your primary source for debugging script-specific issues.
*   **Python Virtual Environments**: If using a venv, ensure the scheduled task correctly uses the Python interpreter from that venv.

---

## Logging

The script logs its operations, successful fetches, email sending status, and any errors to a file named `stock_fetcher.log` in the same directory as the script. Check this file for detailed information if you encounter issues.

## Troubleshooting

*   **Check `stock_fetcher.log`**: This is the first place to look for error messages or status updates from the script.
*   **Cron/Task Scheduler Logs**: Check system logs for cron or the history tab in Task Scheduler for issues related to task execution itself.
*   **Invalid API Key**: Ensure your Alpha Vantage API key is correct, active, and correctly provided to the script (especially via environment variable `ALPHA_VANTAGE_API_KEY` for automated runs).
*   **Email Credentials**: Double-check `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, and `SMTP_PASSWORD` environment variables. For Gmail, you might need to use an "App Password" if 2-Step Verification is enabled. SMTP logs in `stock_fetcher.log` will indicate authentication failures.
*   **Firewall/Network Issues**: Ensure your server can connect to `www.alphavantage.co` (port 443) and your SMTP server on the specified port.
*   **Dependencies**: Make sure the `requests` library is installed in the Python environment being used (`pip install -r requirements.txt`).
*   **Path Issues (Automation)**: When using cron or Task Scheduler, always use absolute paths for the script and the Python interpreter. Ensure environment variables are correctly set and accessible by the execution context of the scheduled task.

## Dependencies

*   `requests`: For making HTTP requests to the Alpha Vantage API. (Listed in `requirements.txt`)
*   Python Standard Libraries: `smtplib`, `email.mime.text`, `os`, `logging`, `socket`.
