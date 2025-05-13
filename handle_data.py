import copy
def analyze_data(data, thresholds):

    data = data['data'][-12:]

    average_1hour = copy.deepcopy(thresholds)
    for key, value in average_1hour.items():
        average_1hour[key] = 0
    average_counter = copy.deepcopy(average_1hour)

    issue_detected = 0
    body = f"Data at "

    body += data[-1]['datetime'][:10] + ' ' + data[-1]['datetime'][11:16] + '\n'
    body += f"Name      val   average   units    threshold\n"

    for i, sample in enumerate(data):

        for channel in sample['channels']:
            if channel['valid']:
                name = channel['name']
                units = channel['units']
                value = channel['value']

                average_counter[name] += 1
                average_1hour[name] += value

    for channel in data[-1]['channels']:
        if channel['valid']:
            name = channel['name']
            units = channel['units']
            value = channel['value']

            average_1hour[name] /= average_counter[name]

            print(f"{name:<8}  {value:<5} {units:^10}")
            if value > thresholds[name]:
                issue_detected = 1

            body += f"{name:<8}  {value:<5} [{average_1hour[name]:<5.2f}] {units:^10} {thresholds[name]:<5}\n"

    return body, issue_detected