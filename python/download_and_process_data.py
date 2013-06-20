from bs4 import BeautifulSoup
from collections import Counter
import cPickle as pickle
from gensim import corpora, models, similarities
import itertools
import json
import os
from paper import Paper
import re
import requests
import urllib

def extract_pdf_urls(html_content):
    soup = BeautifulSoup(html_content)
    links = soup.find_all('a')
    links = [link for link in links if link.contents[0]=="pdf"]
    print("%d Papers Found" % len(links))
    return links

def get_title_and_authors(soup):
    valid_characters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ")
    br = soup.find("br")
    if br is not None and ";" not in soup.contents[0]:
        first_break_loc = soup.contents.index(br)
        title = re.findall(r"\d+\s*,(.+),?", soup.contents[0])[0].strip()
        authors = soup.contents[first_break_loc+1].strip()
    else:
        title = re.findall(r"\d+\s*,(.+),", soup.contents[0])[0].strip()
        authors = re.findall(r"\d+\s*,.+,(.+)", soup.contents[0])[0].strip()
    title = title.replace(",", "").encode("ascii", "ignore")
    title = "".join([c for c in title if c in valid_characters])
    authors = authors.encode("ascii", "ignore")
    authors = [author.strip() for author in authors.split(";")]
    return title, authors

def download_pdfs(site_url, paper_path):
    print("Downloading PDF's From %s" % site_url)
    r = requests.get(site_url)
    html = r.content
    links = extract_pdf_urls(html)
    papers = []
    for link in links:
        title, authors = get_title_and_authors(link.parent)
        print("%s" % title.encode('ascii', 'ignore'))
        print("   %s" % ", ".join(authors))
        pdf_link = link.get("href")
        root, file_name = os.path.split(pdf_link)
        save_path = os.path.join(paper_path, file_name)
        paper = Paper(title, authors, pdf_link, save_path)
        papers.append(paper)
    return papers

def download_all_days(paper_path):
    papers_day1 = download_pdfs("http://icml.cc/2013/?page_id=868", paper_path) # Monday    June 17
    papers_day2 = download_pdfs("http://icml.cc/2013/?page_id=874", paper_path) # Tuesday   June 18
    papers_day3 = download_pdfs("http://icml.cc/2013/?page_id=876", paper_path) # Wednesday June 19

    return papers_day1+papers_day2+papers_day3
