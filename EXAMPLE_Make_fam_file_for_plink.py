from collections import defaultdict
import requests
import json

def request_URL(user_input):
	url = 'http://10.64.16.241:8000/' + user_input
	return url

# Get response from FastAPI
user_input = input('Please Enter "API router" (e.g. GET_coll )\n > ')
url = request_URL(user_input)
response = requests.get(url)
#print(response, response.text)

# Load FastAPI response into a dictionary
response_dict = json.loads(response.text)
#for i in response_dict['data'][0]:
#	print(i)

# Data Preprocessing: select needed fields
selected_fields_dict = defaultdict(str)
for i in response_dict['data'][0]:
	if i['Group'] == 'ERT組':
		i['Group'] = 'Case'
	elif i['Group'] == '非ERT組':
		i['Group'] = 'Control'
	selected_fields_dict[i['SampleID']] = i['Group']
#print(selected_fields_dict)

with open('FabryDisease_case_control.txt', 'w') as f:
	for sampleid in selected_fields_dict:
		f.write(sampleid + '\t' + selected_fields_dict[sampleid] + '\n')

with open('FabryDisease_93.list', 'w') as f:
	for sampleid in selected_fields_dict:
                f.write(sampleid + '\n')
