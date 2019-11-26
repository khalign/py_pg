import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://news.ycombinator.com/')
soup = BeautifulSoup(res.text, 'html.parser')
news = soup.select('.storylink')
subtext = soup.select('.subtext')


def custom_hn (links, subtext):
    hn = []
    for i, _ in enumerate(news):
        title = news[i].getText()
        link = news[i].get('href', None)
        score = subtext[i].select('.score')
        if len(score):
            votes = int(score[0].getText().replace(' points', ''))
            if votes > 99:
                hn.append({'title': title, 'link': link, 'votes': votes})
    return sorted(hn, key = lambda n:n['votes'], reverse = True)
    


pprint.pprint(custom_hn(news, subtext))