from handle_website import *
from handle_email import *
from handle_data import *
from handle_log import *

WEB_ERROR_COUNT_THRESHOLD = 6  # number of consecutive errors
# thresholds
thresholds = {'NO': 7, 'NOX': 30, 'NO2': 25, 'O3': 150, 'PM2.5': 50, 'Benzene': 15}

# Load previous state
state = load_state()

web_error_count = state.get("web_error_count")
code_error_count = state.get("code_error_count")

if web_error_count is None:
    web_error_count = 0
if code_error_count is None:
    code_error_count = 0

try:
    # Read website data
    html = read_data_from_web()
    data = parse_html_to_list(html)

    if data != {}:

        web_error_count = 0
        body, email_report = analyze_data(data, thresholds)

    else:

        email_report = 0
        body = ""
        web_error_count += 1
        print("No <pre> tag found. Could not parse JSON.")

    if email_report:
        send_email(subject="AQI Notification", body=body)

    if web_error_count > 0 and (web_error_count % WEB_ERROR_COUNT_THRESHOLD) == 0:
        send_email(subject="AQI Code web error", body=str(web_error_count) + " consecutive web errors occurred")

except:
    code_error_count += 1

if code_error_count == 1:
    send_email(subject="AQI Code execution error", body=str(code_error_count) + " execution error occurred")

state["last_run"] = datetime.now().isoformat()
state["web_error_count"] = web_error_count
state["code_error_count"] = code_error_count

# Save the updated state
save_state(state)
