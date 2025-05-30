import requests
from bs4 import BeautifulSoup
from newspaper import Article
import json
from requests.auth import HTTPDigestAuth
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def summarize_with_sumy(text, sentence_count=2):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary_sentences = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary_sentences)

def get_message():
    url = "https://news.google.com/rss/search?q=donald+trump&hl=en-US&gl=US&ceid=US:en&as_qdr=d"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.find_all("item")

    summaries = []

    for item in items[:1]:  # Limit to 1 article
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

            # Use better summarizer than article.nlp()
            custom_summary = summarize_with_sumy(article.text, sentence_count=2)
            full_output = f"{custom_summary}\n{article_url}"

            # Trim to exactly 279 characters
            if len(full_output) > 279:
                full_output = full_output[:100] + "..." + "\n\n" + article_url

            summaries.append(full_output)

        except Exception as e:
            continue

    return "\n".join(summaries)