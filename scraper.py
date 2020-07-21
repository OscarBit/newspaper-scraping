import requests
import lxml.html as html
import os
import datetime as datetime

HOME_URL = 'https://www.larepublica.co'

XPATH_LINK_TO_ARTICLE = '//div/h2/a/@href' #'//div[@class="V_Title"]/h2/a/@*' DO NOT WORKS
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/a[@class="economiaSect"]/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY  = '//div[@class="html-content"]/p[not(@class)]/text()'
XPATH_AUTOR = '//div[@class="autorArticle"]/p/text()'

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                autor = parsed.xpath(XPATH_AUTOR)[0]
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as file:
                file.write(f'{title}\n{autor}')
                file.write('\n\n')
                file.write(f'{summary}\n')
                for p in body:
                    file.write(f'\n{p}')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(f'Links to notices: {links_to_notices}')
            
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()


if __name__ == "__main__":
    run()