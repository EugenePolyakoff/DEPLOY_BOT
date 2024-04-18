# import json
# import re
# import subprocess
# from time import sleep
#
#
command = """curl -S -X POST \
-H 'Version: 15.1' \
-H 'Accept: application/json' \
-H 'SEC: bb472e6a-54a7-4d7c-89fe-596db25e39ae' \
'https://qradar-dev-01.soc.bi.zone/api/ariel/searches?query_expression=SELECT%20%20%20%20QIDNAME%28qid%29%20as%20%27Event_Name%27%2C%20%20%20%22username%22%20as%20%27Username%27%2C%20%20%20%22Ariel%20Cursor%20ID%22%20as%20%27Search%20Id%20Executed%27%2C%20%20%20%22searchid%22%20as%20%27Search%20Id%20Completed%27%20FROM%20events%20WHERE%20QIDNAME%28qid%29%3D%27Search%20Executed%27%20OR%20QIDNAME%28qid%29%3D%27Search%20Completed%27%20last%206%20hours'"""

# result = subprocess.run(command, shell=True, capture_output=True, text=True)
#
# cursor_id = re.match(r'\"cursor_id\": \"([^\"]+)', result.stdout)
#
# command = f"""curl -S -X GET \
# -H 'Version: 15.1' \
# -H 'Accept: application/json' \
# -H 'SEC: bb472e6a-54a7-4d7c-89fe-596db25e39ae' \
# 'https://qradar-dev-01.soc.bi.zone/api/ariel/searches/{cursor_id}'"""
#
# while True:
#     result = subprocess.run(command, shell=True, capture_output=True, text=True)
#     unloading_readiness_status = re.search(r'\"status\": \"([^\"]+)', result.stdout).group(1)
#     if unloading_readiness_status == "COMPLETED":
#         break
#     sleep(1)
#
# command = f"""curl -S -X GET \
# -H 'Range: items=0-4000' \
# -H 'Version: 15.1' \
# -H 'Accept: application/json' \
# -H 'SEC: bb472e6a-54a7-4d7c-89fe-596db25e39ae' \
# 'https://qradar-dev-01.soc.bi.zone/api/ariel/searches/{cursor_id}/results' > /home/deploy_bot/stdout.json"""
#
# complite_reg_exp = r"Event_Name': 'Search Completed'.*Search Id Completed': '([^']+)"
# executed_reg_exp = r"Event_Name': 'Search Executed'.*Search Id Executed': '([^']+)"
# active_searchers = []
#
# with open('stdout.json', 'r') as json_file:
#     data = json.load(json_file)
#
#     complited_events_id = []
#     executed_events_id = []
#
#     for i_event in data['events']:
#         if 'Search Completed' in str(i_event):
#             complited_events_id.append(re.search(complite_reg_exp, str(i_event)).group(1))
#         elif 'Search Executed' in str(i_event):
#             executed_events_id.append(re.search(executed_reg_exp, str(i_event)).group(1))
#
#     unique_id = list(set(complited_events_id) - set(executed_events_id))
#     unique_id.extend(set(executed_events_id) - set(complited_events_id))
#
#     for i_unique_id in unique_id:
#         for i_event in data['events']:
#             if f"Search Id Executed': '{i_unique_id}'" in str(i_event):
#                 active_searchers.append(i_event['Username'])
# print(unique_id)
# print(active_searchers)
import csv
import re
# searchers_ids = []
# with open('employees_bd.csv', newline='') as csvfile:
#     reader = csv.reader(csvfile)
#     if not reader:
#         pass
#
#     for i_people in reader:
#         if 'a.barkov' in i_people[0]:
#             print('A')

a = [1, 2 , 3, 3, 3]
print(set(a))



# URL="https://qradar-dev-01.soc.bi.zone/api/ariel/searches"
# SEC_TOKEN="bb472e6a-54a7-4d7c-89fe-596db25e39ae"
# QUERY_EXPRESSION="SELECT%20%20%20%20QIDNAME%28qid%29%20as%20%27Event_Name%27%2C%20%20%20%22username%22%20as%20%27Username%27%2C%20%20%20%22Ariel%20Cursor%20ID%22%20as%20%27Search%20Id%20Executed%27%2C%20%20%20%22searchid%22%20as%20%27Search%20Id%20Completed%27%20FROM%20events%20WHERE%20QIDNAME%28qid%29%3D%27Search%20Executed%27%20OR%20QIDNAME%28qid%29%3D%27Search%20Completed%27%20last%206%20hours"
# OUT_FILE="/home/deploy_bot/stdout.json"
#
# # Отправка POST запроса для создания поиска
# response=$(curl -S -X POST \
#     -H 'Version: 15.1' \
#     -H 'Accept: application/json' \
#     -H "SEC: $SEC_TOKEN" \
#     "$URL?query_expression=$QUERY_EXPRESSION")
#
# cursor_id=$(echo "$response" | grep -oP '"cursor_id": "\K[^"]+')
#
# #echo $cursor_id > /home/deploy_bot/test_file.txt
#
# while true; do
#     response=$(curl -S -X GET \
#         -H 'Version: 15.1' \
#         -H 'Accept: application/json' \
#         -H "SEC: $SEC_TOKEN" \
#         "$URL/$cursor_id")
#
#     # Проверка статуса завершения поиска
#     unloading_readiness_status=$(echo "$response" | grep -oP '"status": "\K[^"]+')
#     if [ "$unloading_readiness_status" = "COMPLETED" ]; then
#         break
#     fi
#     sleep 1
# done
# echo "Ready!"
#
# curl -S -X GET \
#     -H 'Range: items=0-4000' \
#     -H 'Version: 15.1' \
#     -H 'Accept: application/json' \
#     -H "SEC: $SEC_TOKEN" \
#     "$URL/$cursor_id/results" > "$OUT_FILE"
#
# #python /home/deploy_bot/users_json_parser.py
# echo "Done!"
