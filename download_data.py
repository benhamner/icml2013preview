from bs4 import BeautifulSoup
import os
import requests
import subprocess
import urllib

data_path  = os.path.join(os.environ["DataPath"], "icml2013preview")
paper_path = os.path.join(data_path, "papers")
temp_path  = os.path.join(data_path, "temp.txt")

def extract_pdf_urls(html_content):
    soup = BeautifulSoup(html_content)
    links = soup.find_all('a')
    links = [link for link in links if link.contents[0]=="pdf"]
    print("%d Papers Found" % len(links))
    return links

def download_pdfs(site_url):
    print("Downloading PDF's From %s" % site_url)
    r = requests.get(site_url)
    html = r.content
    links = extract_pdf_urls(html)
    paper_paths = []
    for link in links:
        pdf_link = link.get("href")
        root, file_name = os.path.split(pdf_link)
        save_path = os.path.join(paper_path, file_name)
        paper_paths.append(save_path)
        if os.path.exists(save_path):
            continue
        print("Downloading %s" % pdf_link)
        urllib.urlretrieve(pdf_link, save_path)
    return paper_paths

def download_all_days():
    papers1 = download_pdfs("http://icml.cc/2013/?page_id=868") # Monday    June 17
    papers2 = download_pdfs("http://icml.cc/2013/?page_id=874") # Tuesday   June 18
    papers3 = download_pdfs("http://icml.cc/2013/?page_id=876") # Wednesday June 19

    return papers1+papers2+papers3

def get_text(paper_paths):
    for i, p_path in enumerate(paper_paths):
        print("%d %s" % (i, p_path))
        if os.path.exists(temp_path):
            os.remove(temp_path)
        subprocess.call(["pdftotext.exe", p_path, temp_path])
        f = open(temp_path)
        text = f.read()
        f.close()
        print(text[:200])

def main():
    paper_paths = download_all_days()
    get_text(paper_paths)

if __name__=="__main__":
    main()