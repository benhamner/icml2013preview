import os
import subprocess

data_path  = os.path.join(os.environ["DataPath"], "icml2013preview")
temp_path  = os.path.join(data_path, "temp.txt")

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

def get_text_from_pdf(pdf_path):
    if os.path.exists(temp_path):
        os.remove(temp_path)
    subprocess.call(["pdftotext.exe", pdf_path, temp_path])
    f = open(temp_path)
    text = f.read()
    f.close()
    return text

class Paper:
    def __init__(self, title, authors, pdf_url, pdf_path):
        self.title = title
        self.authors = authors
        self.pdf_url = pdf_url

        download_paper_if_not_exists(pdf_url, pdf_path)

        self.text = get_text_from_pdf(pdf_path)
        create_thumbnail(title, pdf_path)

    def to_dict(self):
        return { "title": self.title,
                 "authors": self.authors,
                 "thumbnail_path": "thumbnails" + self.title.encode("ascii", "ignore") + ".jpg",
                 "pdf_url": self.pdf_url}