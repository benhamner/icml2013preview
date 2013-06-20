from collections import Counter
import nltk
from nltk.corpus import stopwords
import os
import re
import subprocess

data_path  = os.path.join(os.environ["DataPath"], "icml2013preview")
paper_path = os.path.join(data_path, "papers")
temp_path  = os.path.join(data_path, "temp.txt")

english_stop_words = set(stopwords.words("english"))

def download_paper_if_not_exists(pdf_url, pdf_path):
    if not os.path.exists(pdf_path):
        print("Downloading %s" % pdf_url)
        urllib.urlretrieve(pdf_url, pdf_path)

def create_thumbnail(title, pdf_path):
    thumb_name = "thumbnails/" + title.encode("ascii", "ignore") + ".jpg"
    if not os.path.exists(thumb_name):
        args = ["montage.exe", "%s[0-7]" % pdf_path, "-mode", "Concatenate", "-tile", "x1", "-quality", "80", "-resize", "x230","-trim", thumb_name]
        print(" ".join(args))
        subprocess.call(args)
    return thumb_name

def get_text_from_pdf(pdf_path):
    if os.path.exists(temp_path):
        os.remove(temp_path)
    subprocess.call(["pdftotext.exe", pdf_path, temp_path])
    f = open(temp_path)
    text = f.read()
    f.close()
    return text

def tokenize(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [x for x in tokens if re.match(r"^[a-z]+$", x) is not None]
    tokens = [x for x in tokens if len(x)>2 and x not in english_stop_words]
    counter = Counter(tokens)
    tokens = [x for x in tokens if counter[x]>2]
    print(counter.most_common(20))
    return tokens, [x[0] for x in counter.most_common(100)]

class Paper:
    def __init__(self, title, authors, pdf_url, pdf_path):
        self.title = title
        self.authors = authors
        self.pdf_url = pdf_url
        self.topics = []

        download_paper_if_not_exists(pdf_url, pdf_path)

        self.text = get_text_from_pdf(pdf_path)
        self.tokens, self.most_common = tokenize(self.text)
        self.thumbnail_path = create_thumbnail(title, pdf_path)


    def to_dict(self):
        return { "title": self.title,
                 "authors": self.authors,
                 "thumbnail_path": self.thumbnail_path,
                 "pdf_url": self.pdf_url,
                 "most_common": self.most_common,
                 "topics": self.topics}

    def set_topics(self, topics):
        self.topics = topics