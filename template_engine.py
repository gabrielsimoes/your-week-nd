from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

template = env.get_template('landing.html')

event = {
	"title": "NDConomics Dynamic", 
	"tags": ["Economics", "Comedy", "Physics"], 
	"description": "Round table with economists Henrique Meirelles, Paulo Guedes, Milton Friedman and special guest Vitor Furtado, world champion in saying garbage.", 
	"date": "Friday, 6PM", 
	"location": "141 DeBartolo Hall"
}

output = template.render(event=event)
with open('landing_dynamic.html', 'w') as f:
    print(output, file=f)  # Python 3.x