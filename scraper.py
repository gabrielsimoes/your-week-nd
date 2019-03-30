import re
from datetime import datetime
from pprint import pprint
from bs4 import BeautifulSoup
import unicodedata
import requests

URL_MAIN = 'https://ndworks.nd.edu/news/theweek-nd/'
URL_WEEK = 'http://theweek.createsend1.com/t/ViewEmail/r/'
URL_ND_7D = 'https://m.nd.edu/current_students/calendar/events?feed=upcoming_events_7d'
URL_ND_EVENT = ''

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

REGEX_DATE = re.compile('('+('|'.join(MONTHS))+')\S*\s*([0-9]+)')
REGEX_WEEK_ID = re.compile('&ID=([^&]+)')
REGEX_WEEK_ID_ALT = re.compile('/t/r-([A-Za-z0-9]+)')

def parse_week_list():
    # month_last_occurence: keeps track of the last index a month appeared in
    # the result array
    month_last_occurence = [-1]*len(MONTHS)

    # month_year: keeps track of the year of the month's last appearance in the
    # result array
    month_year = [datetime.now().year + 1]*12

    # Get page, parse and select 'main' tag's children
    r = requests.get(URL_MAIN)
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
    # Get page, parse and select relevant tags
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


with open("weeks.csv", "w") as output_file:
    scrap_weeks(output_file)
