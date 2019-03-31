import re
import json
import string
from datetime import datetime
from pprint import pprint
from bs4 import BeautifulSoup
import unicodedata
import requests

URL_WEEK_ND = 'https://ndworks.nd.edu/news/theweek-nd/'
URL_WEEK = 'http://theweek.createsend1.com/t/ViewEmail/r/'
CALENDARS_ND = [
    ('cal_artsandentertainment', 'Arts and Entertainment'),
    ('cal_student_activities', 'Student Life'),
    ('athletics', 'Athletics'),
    ('cal_sustainability', 'Sustainability'),
    ('faculty_and_staff', 'Faculty and Staff'),
    ('health_and_recreation', 'Health and Recreation'),
    ('lectures_and_conferences', 'Lectures and Conferences'),
    ('open_to_the_public', 'Open to the Public'),
    ('religious_and_spiritual', 'Religious and Spiritual'),
    ('school_of_architecture', 'School of Architecture'),
    ('college_of_arts_and_letters', 'College of Arts and Letters'),
    ('mendoza_college_of_business', 'Mendoza College of Business'),
    ('college_of_engineering', 'College of Engineering'),
    ('graduate_school', 'Graduate School'),
    ('hesburgh_libraries', 'Hesburgh Libraries'),
    ('law_school', 'Law School'),
    ('college_of_science', 'College of Science'),
    ('cal_keough', 'Keough School of Global Affairs'),
    ('centers_and_institutes', 'Centers and Institutes'),
]
URL_CAL = 'https://m.nd.edu/current_students/calendar/events?feed='
URL_EVENT = 'https://m.nd.edu/current_students/calendar/events.json?_kgoui_include_html=1&_kgoui_region=kgoui_Rcontent_I0_Rcontent_I0_Rright&id=event-'

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

REGEX_DATE = re.compile('('+('|'.join(MONTHS))+')\S*\s*([0-9]+)')
REGEX_WEEK_ID = re.compile('&ID=([^&]+)')
REGEX_WEEK_ID_ALT = re.compile('/t/r-([A-Za-z0-9]+)')
REGEX_EVENT_ID = re.compile('id=event-([A-Za-z0-9%-]+)')

def parse_week_list():
    # month_last_occurence: keeps track of the last index a month appeared in
    # the result array
    month_last_occurence = [-1]*len(MONTHS)

    # month_year: keeps track of the year of the month's last appearance in the
    # result array
    month_year = [datetime.now().year + 1]*12

    # Get page, parse and select 'main' tag's children
    r = requests.get(URL_WEEK_ND)
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find('main').children

    # result: a list of tuples that is returned at the end of the function
    result = []

    # Iterate through tags which are direct children of the 'main' content tag
    for tag in content:
        # If the tag is an 'h2' tag, then it represents a new week
        if tag.name == 'h2':
            # Get data from 'h2' tag and the 'a' tag
            date = ''.join(tag.stripped_strings)
            link = tag.find_next("a")
            who = link.get_text()
            url = link.get('href')

            # Unicode normalize strings
            date = unicodedata.normalize('NFKD', date)
            who = unicodedata.normalize('NFKD', who)
            url = unicodedata.normalize('NFKD', url)

            # Parse date with regex
            m_date = REGEX_DATE.search(date)
            month = MONTHS.index(m_date.group(1))
            day = int(m_date.group(2))

            # Parse week id
            m_id = REGEX_WEEK_ID.search(url)
            if m_id is None:
                m_id = REGEX_WEEK_ID_ALT.search(url)
            wid = m_id.group(1)

            # Test if we went back one year
            if month_last_occurence[month] != len(result):
                month_year[month] -= 1

            # Set year based on the last year for the given month
            year = month_year[month]

            # Append a tuple to result list (and fix month's 0-indexation)
            result.append((year, month+1, day, who, wid))

            # Update month_last_occurence to reflect that we are looking
            # at the given month
            month_last_occurence[month] = len(result)

    return result

def parse_week(week):
    r = requests.get(URL_WEEK+week[4])
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find('table').find_all('tr', recursive=False)[-1].find('td').find_all('table', recursive=False)[1:-1]

    result = []

    for section in content:
        [section_title, paragraphs, _] = section.find_all('tr', recursive=False)

        section_title = ' '.join(section_title.stripped_strings).replace('\t', ' ').replace('\r', ' ')
        section_events = [' '.join(p.stripped_strings).replace('\t', ' ').replace('\r', ' ') for p in paragraphs.find('td').find_all('p', recursive=False)]

        result.append((section_title, section_events))

    return result

def scrap_weeks(output_file):
    output_file.write('\t'.join(['week_date', 'week_category', 'week_id', 'section_name', 'event_content']) + '\n')

    for week in parse_week_list():
        events = parse_week(week)
        for section in events:
            for event in section[1]:
                output_file.write('\t'.join(["%d-%d-%d" % (week[0], week[1], week[2]), week[3], week[4], section[0], event]) + '\n')

def parse_calendar(cal):
    r = requests.get(URL_CAL+cal[0])
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find_all('a', class_='kgoui_list_item_action')

    result = []

    for link in content:
        m_id = REGEX_EVENT_ID.search(link.get('href'))
        result.append(m_id.group(1))

    return result

def parse_event(eid):
    r = requests.get(URL_EVENT+eid, headers={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    })
    j = json.loads(r.text)

    content = [j for j in [j for j in j['response']['contents'][0]['regions'] if j['name'] == 'actions'][0]['contents'] if j['class'] == 'KGOUIActionAddToCalendar'][0]['fields']

    fixstr = lambda s: s in set(string.printable)

    title = ''.join(filter(fixstr, content['title']))
    description = ''.join(filter(fixstr, content['description']))
    location = ''.join(filter(fixstr, content['location']))
    date_start = int(content['startDate']['value']['kgoDeflatedData']['timestamp'])
    date_end = int(content['endDate']['value']['kgoDeflatedData']['timestamp'])

    return (title, description, location, date_start, date_end)

def scrap_calendars(output_file):
    cals = dict(CALENDARS_ND)
    events = {}
    exists = {}

    for cal in CALENDARS_ND:
        print(cal)
        cal_events = parse_calendar(cal)
        for eid in cal_events:
            if eid in exists:
                if cal[0] not in events[exists[eid]]['categories']:
                    events[exists[eid]]['categories'].append(cal[0])
            else:
                try:
                    event = parse_event(eid)
                    exists[eid] = event[0]
                    if event[0] not in events:
                        events[event[0]] = {
                            'title': event[0],
                            'description': event[1],
                            'location': event[2],
                            'whole_days': [],
                            'partial_days': [],
                            'categories': [cal[0]],
                        }

                    if event[4] - event[3] >= 86000:
                        events[event[0]]['whole_days'].append(datetime.fromtimestamp(event[3]).strftime('%Y-%m-%d'))
                    else:
                        events[event[0]]['partial_days'].append({
                            'day': datetime.fromtimestamp(event[3]).strftime('%Y-%m-%d'),
                            'start': datetime.fromtimestamp(event[3]).strftime('%I:%M %p'),
                            'end': datetime.fromtimestamp(event[4]).strftime('%I:%M %p'),
                        })
                except:
                    print('Event information has error!')

    output_file.write(json.dumps({
        'cals': cals,
        'events': events,
    }))


scrap_weeks(open("weeks.csv", "w"))
scrap_calendars(open("events.json", "w"))

