import json
import re


def json_parser():
    complite_reg_exp = r"Event_Name': 'Search Completed'.*Search Id Completed': '([^']+)"
    executed_reg_exp = r"Event_Name': 'Search Executed'.*Search Id Executed': '([^']+)"
    active_searchers = []

    with open('stdout.json', 'r') as json_file:
        data = json.load(json_file)

        complited_events_id = []
        executed_events_id = []

        for i_event in data['events']:
            if 'Search Completed' in str(i_event):
                complited_events_id.append(re.search(complite_reg_exp, str(i_event)).group(1))
            elif 'Search Executed' in str(i_event):
                executed_events_id.append(re.search(executed_reg_exp, str(i_event)).group(1))

        unique_id = list(set(complited_events_id) - set(executed_events_id))
        unique_id.extend(set(executed_events_id) - set(complited_events_id))

        for i_unique_id in unique_id:
            for i_event in data['events']:
                if "Search Id Executed': \'{}\'".format(i_unique_id) in str(i_event):
                    active_searchers.append(i_event['Username'])

    with open('/Users/e.polyakov/Downloads/DEPLOY_BOT/stdout.json', 'w'):
        pass

    return set(active_searchers)
