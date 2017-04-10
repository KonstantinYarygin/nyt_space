from bs4 import BeautifulSoup
from nltk import word_tokenize, pos_tag
from collections import Counter, defaultdict
import datetime
import pickle
import string
import csv
import re
import os

from time import time

PUNCTUATION_REGEXP = re.compile('[{}]'.format(re.escape(string.punctuation)))
MONTH_NUMBER = {
    'January':    1,
    'February':   2,
    'March':      3,
    'April':      4,
    'May':        5,
    'June':       6,
    'July':       7,
    'August':     8,
    'September':  9,
    'October':   10,
    'November':  11,
    'December':  12,
}
with open('top100en.csv', 'r') as f:
    TOP100EN = {line.strip() for line in f}

class Article(object):
    """docstring for Article"""
    def __init__(self):
        self.header = ''
        self.paragraphs = []
        self.date = ''

    def __str__(self):
        article_str = ''
        article_str += '=' * (len(self.header) + 6) + '\n'
        article_str += '   {header}   \n'.format(header=self.header)
        article_str += '=' * (len(self.header) + 6) + '\n'
        article_str += 'date: {date}\n'.format(date=self.date)
        for paragraph in self.paragraphs:
            article_str += '{paragraph}\n'.format(paragraph=paragraph)
        return article_str

    def extract_from_node(self, article_node):
        tr_nodes = article_node.find_all('tr')

        header_node = [n for n in tr_nodes if 'HD' in [b.text for b in n.find_all('b')]][0]
        header = ' '.join(x.text for x in header_node.find_all('span'))
        self.header = header.strip()

        lead_node = [n for n in tr_nodes if 'LP' in [b.text for b in n.find_all('b')]][0]
        lead = [x.text for x in lead_node.find_all('p') if x.has_attr('class')]
        text_nodes = [n for n in tr_nodes if 'TD' in [b.text for b in n.find_all('b')]]
        if text_nodes:
            text_node = text_nodes[0]
            text = [x.text for x in text_node.find_all('p') if x.has_attr('class')]
        else:
            text = []
        text = lead + text
        self.paragraphs = [chunk.strip() for chunk in text]

        date_node = [n for n in tr_nodes if 'PD' in [b.text for b in n.find_all('b')]][0]
        date = ' '.join(x.text for x in date_node.find_all('td') if re.match('\d{1,2} [A-z]+ \d{4}', x.text))
        day, month, year = date.split(' ')
        month = MONTH_NUMBER[month]
        self.date = datetime.date(int(year), month, int(day))

    def extract_word_counts(self):
        text = ' '.join(self.paragraphs)
        text = re.sub('\[http\:\/\/[^\]]*\]', '', text)
        words = [word.lower() for word in word_tokenize(text)]
        words = [PUNCTUATION_REGEXP.sub('', word) for word in words]
        words = [word for word in words if word and word not in TOP100EN]
        words = [word for word, tag in pos_tag(words) if tag not in {'DT', 'IN', 'TO', 'CC', 'PRP', 'PRP$'}]
        self.word_count = Counter(words)

class ArticleCorpus(list):
    def __init__(self):
        list.__init__(self)
        self.n_articles = 0

    def add_from_html_file(self, html_file_path):
        soup = BeautifulSoup(open(html_file_path))
        div_nodes = [node for node in soup.find_all('div') if node.has_attr('class')]
        carry_node = [node for node in div_nodes if node['class'] == ['carryOverOpen']][0]
        article_nodes = [node for node in carry_node.children
                             if node.has_attr('id') and \
                                node['id'].startswith('article-NYTF')]
        for article_node in article_nodes:
            a = Article()
            a.extract_from_node(article_node)
            a.html_file_name = os.path.basename(html_file_path)
            self.append(a)
            self.n_articles += 1

    def add_from_folder(self, folder_path, verbose=True):
        t1 = time()
        file_names = os.listdir(folder_path)
        for filename in file_names:
            file_path = os.path.join(folder_path, filename)
            if verbose:
                print('Loading articles from {}'.format(file_path))
            self.add_from_html_file(file_path)
        t2 = time()
        print('Done, total time: {:.3f}'.format(t2 - t1))

if __name__ == '__main__':
    corpus = ArticleCorpus()
    corpus.add_from_folder('data/tagged_space_2003-2017/')
    corpus.sort(key=lambda x: x.date)
    for a in corpus:
        a.extract_word_counts()
    pickle.dump(corpus, 'nyt_space_corpus_2003-2017.pkl')
