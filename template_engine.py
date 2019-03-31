from jinja2 import Environment, FileSystemLoader
import json
from datetime import datetime

def FormatDate(event):
	if len(event["whole_days"]) > 0:
		start_date = datetime.strptime(event["whole_days"][0], '%Y-%m-%d')
		end_date = datetime.strptime(event["whole_days"][-1], '%Y-%m-%d')
		if len(event["partial_days"]) > 0:
			start_time = event["partial_days"][0]["start"][:-3]
			end_time = event["partial_days"][0]["end"]
			event["formatted_date"] = start_date.strftime("%m/%d") + " - " + end_date.strftime("%m/%d") + ", " + start_time + "-" + end_time
		else:
			event["formatted_date"] = start_date.strftime("%m/%d") + " - " + end_date.strftime("%m/%d")

	elif len(event["partial_days"]) > 0:
		weekday = datetime.strptime(event["partial_days"][0]["day"] , '%Y-%m-%d')
		weekday = weekday.strftime('%A')
		start_time = event["partial_days"][0]["start"][:-3]
		end_time = event["partial_days"][0]["end"]
		event["formatted_date"] = weekday + ", " + start_time + "-" + end_time
	
	else:
		event["formatted_date"] = "See Details"
	return event

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

template = env.get_template('landing.html')

with open('events.json') as json_file:
	events_file = json.load(json_file)
	# print(events_all)
	events = events_file["events"]
	# for event in events 
	# 	print(event["title"])
	event_array = []
	for name, event in events.items():
		event = FormatDate(event)
		event_array.append(event)

output = template.render(events=event_array)
with open('landing_dynamic.html', 'w') as f:
	print(output, file=f)


