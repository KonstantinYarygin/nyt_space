from parser import Article, ArticleCorpus
from collections import defaultdict, Counter
from time import time
import pandas as pd
import numpy as np
import datetime
import pickle

def cos(x, y):
    dot = np.sum(x*y)
    magn_x = np.sqrt(np.sum(x**2))
    magn_y = np.sqrt(np.sum(y**2))
    return dot / (magn_x * magn_y)

with open('corpora_parsed/nyt_space_corpus_2003-2017.pkl', 'rb') as f:
    space_corpus = pickle.loads(f.read())
with open('corpora_parsed/nyt_business_corpus_2003-2017.pkl', 'rb') as f:
    business_corpus = pickle.loads(f.read())
print('loaded')

space_wc_year = defaultdict(lambda: Counter())
business_wc_year = defaultdict(lambda: Counter())
for article in space_corpus:
    space_wc_year[article.date.year] += article.word_count
for article in business_corpus:
    business_wc_year[article.date.year] += article.word_count

for year in range(2003, 2017):
    sum_wc = space_wc_year[year] + business_wc_year[year]
    # sum_wc_mc = sum_wc.most_common(20000)
    sum_wc_mc = sum_wc.items()
    year_vocab = sorted(list({word for word, count in sum_wc_mc}))
    # year_vocab = sorted(list({x for x in space_wc_year[year]} & {x for x in business_wc_year[year]}))
    space_vec = np.array([space_wc_year[year][word] for word in year_vocab])
    business_vec = np.array([business_wc_year[year][word] for word in year_vocab])
    print(year, cos(space_vec, business_vec))

print()
business_wc = sum(business_wc_year.values(), Counter())

for year in range(2003, 2017):
    sum_wc = space_wc_year[year] + business_wc
    # sum_wc_mc = sum_wc.most_common(20000)
    sum_wc_mc = sum_wc.items()
    year_vocab = sorted(list({word for word, count in sum_wc_mc}))
    # year_vocab = sorted(list({x for x in space_wc_year[year]} & {x for x in business_wc_year[year]}))
    space_vec = np.array([space_wc_year[year][word] for word in year_vocab])
    business_vec = np.array([business_wc[word] for word in year_vocab])
    print(year, cos(space_vec, business_vec))

