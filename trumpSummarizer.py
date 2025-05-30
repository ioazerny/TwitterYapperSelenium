import requests
from bs4 import BeautifulSoup
from newspaper import Article
import nltk


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
            
            article = Article(link)
            article.download()
            article.parse()
            article.nlp()

            # Create a summary with title, URL, and summary
            summary = f"Title: {title}\nURL: {link}\nSummary: {article.summary}\n\n"
            summaries.append(summary)
            
        except Exception as e:
            print(f"Error processing article: {e}")
            continue

    return "\n".join(summaries)