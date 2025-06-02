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

**Example (assuming server is in CT (ET-1) and script is in `/home/user/scripts/`):**
```cron
# Run at 8:30 AM CT (9:30 AM ET), Monday to Friday
30 8 * * 1-5 /usr/bin/python3 /home/user/scripts/stock_fetcher.py

# Run at 3:30 PM CT (4:30 PM ET), Monday to Friday
30 15 * * 1-5 /usr/bin/python3 /home/user/scripts/stock_fetcher.py
```

**Important:**
*   **Absolute Paths**: Always use absolute paths for both the Python interpreter and the script file to avoid issues with the cron job's execution environment. You can find the path to Python using `which python3`.
*   **Permissions**: Ensure `stock_fetcher.py` is executable (`chmod +x /path/to/stock_fetcher.py`) or that the Python interpreter can read and execute it.
*   **Environment**: Cron jobs run with a minimal environment. If your script relies on environment variables (like `API_KEY` if you were to load it from env), they must be set within the script or in the cron command itself. Our current script prompts for the API key, which won't work for an automated cron job. **You'll need to modify `stock_fetcher.py` to read the API key and email credentials from a configuration file or environment variables for automated execution.**

### c. Save and Exit
Save the crontab file and exit the editor. (e.g., `Ctrl+O`, then `Enter`, then `Ctrl+X` in nano). Cron will automatically pick up the changes.

### d. Checking Cron Logs
If the script doesn't run as expected, check the cron logs. The location can vary, but common places include:
*   `/var/log/syslog` (Debian/Ubuntu): `grep CRON /var/log/syslog`
*   `/var/log/cron` (RedHat/CentOS)
You can also redirect the script's output to a log file for debugging:
```cron
30 9 * * 1-5 /usr/bin/python3 /path/to/stock_fetcher.py >> /path/to/stock_fetcher.log 2>&1
```
This appends both standard output (`>>`) and standard error (`2>&1`) to `stock_fetcher.log`.

## 3. Using Task Scheduler (Windows)

Task Scheduler is the built-in job scheduler in Windows.

### a. Open Task Scheduler
Search for "Task Scheduler" in the Start Menu and open it.

### b. Create a Basic Task
1.  In the right-hand pane, click "Create Basic Task...".
2.  **Name and Description**: Enter a name (e.g., "Fetch Stock Prices AM") and an optional description. Click Next.
3.  **Trigger**:
    *   Select "Daily". Click Next.
    *   Set the **Start date**. For the time, enter the local time equivalent of **9:30 AM ET**.
    *   Recur every "1" days. Click Next.
4.  **Action**:
    *   Select "Start a program". Click Next.
    *   **Program/script**: Enter the path to your Python interpreter (e.g., `C:\Python39\python.exe` or just `python.exe` if it's in your system PATH).
    *   **Add arguments (optional)**: Enter the absolute path to your script (e.g., `C:\Users\YourUser\Documents\stock_fetcher.py`).
    *   **Start in (optional)**: Enter the directory where your script is located (e.g., `C:\Users\YourUser\Documents\`). This is important if your script uses relative paths to access other files (though `stock_fetcher.py` currently does not).
    *   Click Next.
5.  **Finish**: Review the settings and click "Finish".

### c. Create Second Task for PM Fetch
Repeat the steps above to create another task for **4:30 PM ET** (converted to your local time). Name it appropriately (e.g., "Fetch Stock Prices PM").

### d. Further Configuration (Weekdays Only)
To limit tasks to weekdays (Monday-Friday):
1.  Open Task Scheduler and find your created task in the "Task Scheduler Library".
2.  Double-click the task to open its Properties.
3.  Go to the "Triggers" tab.
4.  Select your daily trigger and click "Edit...".
5.  Under "Advanced settings", you might find options to specify days of the week, or you might need to set it to "Weekly" and then select Monday, Tuesday, Wednesday, Thursday, Friday. The exact options can vary slightly with Windows versions.
    *   Alternatively, for a daily trigger, you can add conditions or modify the trigger to run on specific days of the week if your version of Task Scheduler supports it directly in the daily trigger setup. If not, setting it up as a weekly trigger that runs on M,T,W,Th,F at the specified time is a common workaround.

### e. Checking Task History
If the script doesn't run as expected:
1.  In Task Scheduler, select the task from the library.
2.  In the bottom pane, or by right-clicking the task, look for a "History" tab or view. Enable it if it's not visible (View -> Show History).
    This tab will show run results, errors, etc.

**Important for Task Scheduler:**
*   Similar to cron, the script will run in a non-interactive session. **You must modify `stock_fetcher.py` to read the API key and email credentials from a configuration file or environment variables.** Prompts will not work.

## 4. General Advice for Automated Execution

*   **Test Manually First**: Before scheduling, always run `python3 /path/to/stock_fetcher.py` (or `python.exe C:\path\to\stock_fetcher.py`) directly from your command line or terminal. Ensure it executes without errors and that you have provided valid API keys/email details if you've modified it to be non-interactive.
*   **Secure Credential Management**:
    *   The current `stock_fetcher.py` prompts for the API key and has placeholders for email credentials. **This is not suitable for non-interactive, scheduled tasks.**
    *   **Modify the script** to read sensitive information (API key, email username/password) from:
        *   **Environment variables**: Set these in your server's environment or within the cron job/task definition if possible.
        *   **A configuration file** (e.g., `config.ini`, `.env` file): Make sure this file is secured and not publicly accessible. Add it to your `.gitignore` if using version control.
    *   Avoid hardcoding credentials directly into the script if it's stored in version control or shared.
*   **Logging**: Implement more robust logging within `stock_fetcher.py` itself. Instead of just printing to console, write status, fetched data, and errors to a dedicated log file. This makes troubleshooting scheduled tasks much easier.
*   **Python Virtual Environments**: If you use a Python virtual environment for your project, ensure you call the Python interpreter from that environment in your cron job or task.
    *   Example for cron: `/path/to/your/venv/bin/python3 /path/to/stock_fetcher.py`
    *   Example for Task Scheduler: Program: `/path/to/your/venv/Scripts/python.exe`

By following these instructions, you should be able to schedule `stock_fetcher.py` to run automatically. Remember that making the script non-interactive by handling credentials securely is a critical step for automation.
