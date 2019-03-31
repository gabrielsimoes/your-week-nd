import json

CATEGORIES = {
    'faith_and_service': 'Faith & Service',
    'health_and_recreation': 'Health & Recreation',
    # 'entertainment_categorized': 'Entertainment',
    'sports': 'Sports',
    'engineering': 'College of Engineering',
    'arts_and_letters': 'Arts & Letters',
    'mendoza': 'Mendoza College of Business',
    'science': 'College of Science',
    'law': 'School of Law',
}

events = []
categories = {}

for cat, name in CATEGORIES.items():
    for ev in json.load(open('data/'+cat+'.json')):
        if cat != 'entertainment_categorized':
            ev['category'] = cat
            events.append(ev)
            if cat not in categories:
                categories[cat] = name
            else:
                events.append(ev)
                ccat = ev['category']
                if ccat not in categories:
                    categories[ccat] = ccat.capitalize() + ' (Entertainment)'


