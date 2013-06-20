from collections import Counter
from gensim import corpora, models, similarities
import itertools
import nltk

def papers_to_corpora(papers):
    texts = [paper.tokens for paper in papers]

    dictionary = corpora.Dictionary(texts)
    dictionary.filter_extremes(3, 0.4)
    print(dictionary)
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    return corpus_tfidf, dictionary

def train_lda(num_topics, corpus, dictionary):
    lda_model = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, update_every=1, passes=10)
    return lda_model

def lda_pipeline(papers):
    corpus, dictionary = papers_to_corpora(papers)
    lda_model = train_lda(6, corpus, dictionary)
    for i in range(lda_model.num_topics):
        print(" ".join([x[1] for x in lda_model.show_topic(i,10)]))
    return lda_model, corpus, dictionary
