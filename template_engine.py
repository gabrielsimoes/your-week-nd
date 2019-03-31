from jinja2 import Environment, FileSystemLoader
import json

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
		event_array.append(event)
	print(event_array[1]["partial_days"][0]["day"])

output = template.render(events=event_array)
with open('landing_dynamic.html', 'w') as f:
	print(output, file=f)
