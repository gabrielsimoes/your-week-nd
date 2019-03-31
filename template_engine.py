from jinja2 import Environment, FileSystemLoader
import json
from datetime import datetime

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
		if len(event["partial_days"]) > 0:
			weekday = datetime.strptime(event["partial_days"][0]["day"] , '%Y-%m-%d')
			weekday = weekday.strftime('%A')
			start_time = event["partial_days"][0]["start"][:-3]
			end_time = event["partial_days"][0]["end"]
			event["formatted_date"] = weekday + ", " + start_time + "-" + end_time
		event_array.append(event)

# event1 = {
# 	"title": "NDConomics Dynamic", 
# 	"tags": ["Economics", "Comedy", "Physics"], 
# 	"description": "Round table with economists Henrique Meirelles, Paulo Guedes, Milton Friedman and special guest Vitor Furtado, world champion in saying garbage.", 
# 	"date": "Friday, 6:00PM", 
# 	"location": "141 DeBartolo Hall"
# }

# event2 = {
# 	"title": "Alan Turing at ND", 
# 	"tags": ["Mathematics", "Machine Learning"], 
# 	"description": "Join Alan Turing on an interesting lecture about the future of Machine Learning.", 
# 	"date": "Wednesday, 2:00PM", 
# 	"location": "B19 - Fitzpatrick Hall of Engineering"
# }

# event3 = {
# 	"title": "Event 3", 
# 	"tags": ["Tag 1", "Tag 2"], 
# 	"description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam in justo libero. Suspendisse nec dolor et enim iaculis tincidunt.", 
# 	"date": "Thursday, 3:00PM", 
# 	"location": "Jenkins Hall"
# }

# event4= {
# 	"title": "Event 4", 
# 	"tags": ["Tag 1", "Tag 2"], 
# 	"description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam in justo libero. Suspendisse nec dolor et enim iaculis tincidunt.", 
# 	"date": "Thursday, 3:00PM", 
# 	"location": "Jenkins Hall"
# }

# event5 = {
# 	"title": "Rear Window (1954)",
# 	"tags": ["Movies"],
# 	"description": "Laid up with a broken leg, professional photographer L.B. “Jeff” Jefferies (James Stewart) combats the cabin fever swelling about...",
# 	"date": "Wednesday, 7:30PM",
# 	"location": "Browning Cinema, DeBartolo Performing Arts Center"
# }

# events = [event1, event2, event3, event4, event5];

output = template.render(events=event_array)
with open('landing_dynamic.html', 'w') as f:
	print(output, file=f)
