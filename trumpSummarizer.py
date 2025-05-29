import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import time

def get_message():
    # Send a request to the news website
    url = "https://www.reuters.com/"
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all article titles and summaries
    article_titles = soup.find_all('h2', class_='article-title')
    article_summaries = soup.find_all('p', class_='article-summary')

    # Extract the text from the article titles and summaries
    titles = [title.get_text() for title in article_titles]
    summaries = [summary.get_text() for summary in article_summaries]

    # Tokenize the summaries and remove stopwords
    stop_words = set(stopwords.words('english'))
    tokenized_summaries = [word_tokenize(summary) for summary in summaries]
    filtered_summaries = [[word for word in summary if word.lower() not in stop_words] for summary in tokenized_summaries]

    # Summarize the articles using NLTK's sentence extraction
    sentences = [sent_tokenize(summary) for summary in filtered_summaries]
    summarized_sentences = [sentence[0] for sentence in sentences]

    # Combine the summarized sentences into a single long text
    long_text = ' '.join(summarized_sentences)

    print(long_text)
    return long_text