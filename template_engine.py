from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

template = env.get_template('landing.html')

event1 = {
	"title": "NDConomics Dynamic", 
	"tags": ["Economics", "Comedy", "Physics"], 
	"description": "Round table with economists Henrique Meirelles, Paulo Guedes, Milton Friedman and special guest Vitor Furtado, world champion in saying garbage.", 
	"date": "Friday, 6PM", 
	"location": "141 DeBartolo Hall"
}

event2 = {
	"title": "Alan Turing at ND", 
	"tags": ["Mathematics", "Machine Learning"], 
	"description": "Join Alan Turing on an interesting lecture about the future of Machine Learning.", 
	"date": "Wednesday, 2PM", 
	"location": "B19 - Fitzpatrick Hall of Engineering"
}

event3 = {
	"title": "Event 3", 
	"tags": ["Tag 1", "Tag 2"], 
	"description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam in justo libero. Suspendisse nec dolor et enim iaculis tincidunt. Nam lacinia turpis non faucibus tincidunt. Proin volutpat, nisi sit amet rutrum euismod, dui est maximus massa, in pharetra mauris erat pharetra erat.", 
	"date": "Thursday, 3PM", 
	"location": "Jenkins Hall"
}

event4= {
	"title": "Event 4", 
	"tags": ["Tag 1", "Tag 2"], 
	"description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam in justo libero. Suspendisse nec dolor et enim iaculis tincidunt. Nam lacinia turpis non faucibus tincidunt. Proin volutpat, nisi sit amet rutrum euismod, dui est maximus massa, in pharetra mauris erat pharetra erat.", 
	"date": "Thursday, 3PM", 
	"location": "Jenkins Hall"
}

events = [event1, event2, event3, event4];

output = template.render(events=events)
with open('landing_dynamic.html', 'w') as f:
	print(output, file=f)