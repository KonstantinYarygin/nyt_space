from bs4 import BeautifulSoup
from nltk import word_tokenize, pos_tag
from collections import Counter
import string
import re

PUNCTUATION_REGEXP = re.compile('[{}]'.format(re.escape(string.punctuation)))

class Article(object):
    """docstring for Article"""
    def __init__(self):
        self.header = ''
        self.paragraphs = []
        self.date = ''
        self.author = ''
        self.n_words = 0

    def __str__(self):
        article_str = ''
        article_str += '=' * (len(self.header) + 6) + '\n'
        article_str += '   {header}   \n'.format(header=self.header)
        article_str += '=' * (len(self.header) + 6) + '\n'
        article_str += 'author: {author}\n'.format(author=self.author)
        article_str += 'date: {date}\n'.format(date=self.date)
        article_str += '{n_words} words\n\n'.format(n_words=self.n_words)
        for paragraph in self.paragraphs:
            article_str += '{paragraph}\n'.format(paragraph=paragraph)
        return article_str

    def extract_from_node(self, article_node):
        span_nodes = [node for node in article_node.find_all('span') if node.has_attr('class')]
        header_nodes = [node for node in span_nodes if node['class'] == ['enHeadline']]
        if header_nodes:
            self.header = header_nodes[0].text.strip()

        p_nodes = [node for node in article_node.find_all('p') if node.has_attr('class')]
        paragraph_nodes = [node for node in p_nodes if 'articleParagraph' in node['class']]
        self.paragraphs = [node.text.strip() for node in paragraph_nodes]

        div_nodes = [node for node in article_node.find_all('div')]

        date_matches = [re.match('^\d{1,2} \w+ \d{4}$', node.text) for node in div_nodes]
        date_list = [m.group(0) for m in date_matches if m]
        if date_list:
            self.date = date_list[0]

        n_word_matches = [re.search('^(\d+) words$', node.text) for node in div_nodes]
        n_words_list = [m.group(1) for m in n_word_matches if m]
        if n_words_list:
            self.n_words = int(n_words_list[0])

        div_nodes_class = [node for node in div_nodes if node.has_attr('class')]
        author_nodes = [node for node in div_nodes_class if node['class'] == ['author']]
        if author_nodes:
            self.author = author_nodes[0].text.replace('By', '').strip()

    def tokenize(self):
        text = ' '.join(self.paragraphs)
        words = word_tokenize(text)
        return words

    def get_top_tfidf(self, n=10):
        text = ' '.join(self.paragraphs)
        words = [word.lower() for word in word_tokenize(text)]
        words = [PUNCTUATION_REGEXP.sub('', word) for word in words]
        words = [word for word in words if word]
        words = [word for word, tag in pos_tag(words) if tag not in {'DT', 'IN', 'TO', 'CC'}]
        w_counter = Counter(words)
        # top = [(word, c / self.n_words) for word, c in w_counter.most_common(n)]
        top = [word for word, c in w_counter.most_common(n)]
        return top

class ArticleCorpus(list):
    def __init__(self):
        list.__init__(self)
        self.n_articles = 0

    def add_from_html_file(self, html_file_path):
        soup = BeautifulSoup(open(html_file_path))
        div_nodes = [node for node in soup.find_all('div') if node.has_attr('class')]
        article_nodes = [node for node in div_nodes if node['class'] == ['article']]
        for article_node in article_nodes:
            a = Article()
            a.extract_from_node(article_node)
            self.append(a)
            self.n_articles += 1


if __name__ == '__main__':
    corpus = ArticleCorpus()
    corpus.add_from_html_file('data/howparc.html')
    for article in corpus:
        print(article.get_top_tfidf(10))
