"""
This file runs the pipeline
"""

import cPickle as pickle
import download_and_process_data
import json
import lda
import os
import paper

def data_to_json_file(json_path, papers, lda_model):
    f = open(json_path, "w")

    data = {
        "papers": [paper.to_dict() for paper in papers],
        "topics": [[y[1] for y in lda_model.show_topic(x, 20)] for x in range(lda_model.num_topics)]
    }
    print(data["topics"])

    f.write(json.dumps(data))
    f.close()

def add_topics_to_papers(lda_model, papers, corpus):
    for paper, doc_bow in zip(papers, corpus):
        paper_topics = [0 for x in range(lda_model.num_topics)]
        for topic_id, p in lda_model[doc_bow]:
            paper_topics[topic_id] = p
        paper.set_topics(paper_topics)

def main(paper_path, json_path):
    papers = download_and_process_data.download_all_days(paper_path)

    # save papers for quicker exploration
    pickle.dump(papers, open(os.path.join(paper_path, "papers.pickle"), "w"))

    lda_model, corpus, dictionary = lda.lda_pipeline(papers)
    add_topics_to_papers(lda_model, papers, corpus)
    data_to_json_file(json_path, papers, lda_model)

if __name__=="__main__":
    data_path  = os.path.join(os.environ["DataPath"], "icml2013preview")
    paper_path = os.path.join(data_path, "papers")
    temp_path  = os.path.join(data_path, "temp.txt")
    json_path  = "data.json"
    main(paper_path, json_path)