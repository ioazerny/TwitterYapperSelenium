import requests
from bs4 import BeautifulSoup
from newspaper import Article
import nltk
import json


def get_message():
    url = "https://news.google.com/rss/search?q=donald+trump&hl=en-US&gl=US&ceid=US:en"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.find_all("item")

    summaries = []

    for item in items[:5]:  # Just the first 5 articles
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
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            }

            url = "https://news.google.com/_/DotsSplashUi/data/batchexecute"
            response = requests.post(url, headers=headers, data=payload)
            array_string = json.loads(response.text.replace(")]}'", ""))[0][2]
            article_url = json.loads(array_string)[1]

            article = Article(article_url)

            print(article.url)

            article.download()

            article.parse()
            article.nlp()

            artSum = article.summary

            # Create a summary with title, URL, and summary
            #summary = f"Title: {title}\nURL: {link}\nSummary: {artSum}\n\n"
            #summaries.append(summary)
            
        except Exception as e:
            print(f"Error processing article: {e}")
            continue

    return "\n".join(summaries)