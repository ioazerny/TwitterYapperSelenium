import requests
from bs4 import BeautifulSoup
from newspaper import Article
import nltk
import json
from requests.auth import HTTPDigestAuth

def get_message():
    url = "https://news.google.com/rss/search?q=donald+trump&hl=en-US&gl=US&ceid=US:en&as_qdr=d"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.find_all("item")

    summaries = []

    for item in items[:1]: # Original 5 articles, due to X/Twitter post character limits we will only retrieve 1 article at the moment
        try:
            title = item.title.text
            link = item.link.text

            redirect = requests.get(link)

            data = BeautifulSoup(redirect.text, 'html.parser').select_one('c-wiz[data-p]').get('data-p')
            obj = json.loads(data.replace('%.@.', '["garturlreq",'))

            payload = {
                'f.req': json.dumps([[['Fbv4je', json.dumps(obj[:-6] + obj[-2:]), 'null', 'generic']]])
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }

            url = "https://news.google.com/_/DotsSplashUi/data/batchexecute"
            basic = HTTPDigestAuth('user', 'pass')
            r = requests.post(url, headers=headers, data=payload, auth=basic)
            array_string = json.loads(r.text.replace(")]}'", ""))[0][2]
            article_url = json.loads(array_string)[1]

            article = Article(article_url)

            article.download()
            article.parse()
            article.nlp()

            artSum = article.summary

            # Create a summary with title, URL, and summary
            summary = f"{artSum}\n\n"
            summaries.append(summary)
            
        except Exception as e:
            continue

    return "\n".join(summaries)