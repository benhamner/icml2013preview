from bs4 import BeautifulSoup
from gensim import corpora, models, similarities
import json
import os
from paper import Paper
import re
import requests
import urllib

data_path  = os.path.join(os.environ["DataPath"], "icml2013preview")
paper_path = os.path.join(data_path, "papers")

def extract_pdf_urls(html_content):
    soup = BeautifulSoup(html_content)
    links = soup.find_all('a')
    links = [link for link in links if link.contents[0]=="pdf"]
    print("%d Papers Found" % len(links))
    return links

def get_title_and_authors(soup):
    br = soup.find("br")
    if br is not None and ";" not in soup.contents[0]:
        first_break_loc = soup.contents.index(br)
        title = re.findall(r"\d+\s*,(.+),?", soup.contents[0])[0].strip()
        authors = soup.contents[first_break_loc+1].strip()
    else:
        title = re.findall(r"\d+\s*,(.+),", soup.contents[0])[0].strip()
        authors = re.findall(r"\d+\s*,.+,(.+)", soup.contents[0])[0].strip()
    title = title.replace(",", "").encode("ascii", "ignore")
    authors = authors.encode("ascii", "ignore")
    return title, authors

def download_pdfs(site_url):
    print("Downloading PDF's From %s" % site_url)
    r = requests.get(site_url)
    html = r.content
    links = extract_pdf_urls(html)
    papers = []
    for link in links:
        title, authors = get_title_and_authors(link.parent)
        print("%s" % title.encode('ascii', 'ignore'))
        print("   %s" % authors.encode('ascii', 'ignore'))
        pdf_link = link.get("href")
        root, file_name = os.path.split(pdf_link)
        save_path = os.path.join(paper_path, file_name)
        paper = Paper(title, authors, pdf_link, save_path)
        papers.append(paper)
    return papers

def download_all_days():
    papers1 = download_pdfs("http://icml.cc/2013/?page_id=868") # Monday    June 17
    # papers2 = download_pdfs("http://icml.cc/2013/?page_id=874") # Tuesday   June 18
    # papers3 = download_pdfs("http://icml.cc/2013/?page_id=876") # Wednesday June 19

    return papers1 #+papers2+papers3

def main():
    papers = download_all_days()
    texts = [paper.tokens for paper in papers]
    dictionary = corpora.Dictionary(texts)
    print(dictionary)
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    print("training lda")
    lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=6, update_every=0, passes=100)
    print(lda.show_topics(-1, 15))
    print("lda trained")

    for paper, doc_bow in zip(papers, corpus_tfidf):
        paper.set_topics([x[1] for x in lda[doc_bow]])
 
    f = open("data.json", "w")

    data = {
        "papers": [paper.to_dict() for paper in papers],
        "topics": [" ".join([y[1] for y in lda.show_topic(x, 100)[:20]]) for x in range(6)]
    }
    print(data["topics"])

    f.write(json.dumps(data))
    f.close()

    import pdb;pdb.set_trace()

if __name__=="__main__":
    main()