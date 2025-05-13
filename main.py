from handle_website import *
from handle_email import *
from handle_data import *

# thresholds
thresholds = {'NO': 7, 'NOX': 30, 'NO2': 25, 'O3': 150, 'PM2.5': 50, 'Benzene': 15}

html = read_data_from_web()
data = parse_html_to_list(html)

if data != {}:

    body, email_report = analyze_data(data, thresholds)

    if email_report:
        send_email(body)

else:

    print("No <pre> tag found. Could not parse JSON.")
