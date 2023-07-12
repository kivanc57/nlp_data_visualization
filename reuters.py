import os
import re
from bs4 import BeautifulSoup
import spacy

def get_texts(file_directory, mode="r", encoding="utf-8"):
    titles = []
    for file_name in os.listdir(file_directory):
        if file_name.endswith(".sgm"):          
            file_path = os.path.join(str(file_directory), file_name)
            with open(file_path, mode='r', encoding='utf-8', errors='ignore') as f:
                data_file = f.read()
                
                soup = BeautifulSoup(data_file, 'html.parser')
                contents = soup.find_all('title')
                
                for content in contents:
                    titles.append(nlp(content.text.lower()))
    return titles


def detect_pos(titles):
    verbs = {}
    subjects = {}
    objects = {}

    for title in titles:
        for token in title:
            pos = token.pos_
            if token.pos_ == "VERB":
                if token.lemma_ not in verbs:
                    verbs[token.lemma_] = 1
                    continue
                else:
                    new_amount = verbs[token.lemma_] + 1
                    verbs[token.lemma_] = new_amount

            if token.dep_ == "nsubj":
                if token.lemma_ not in subjects:
                    subjects[token.lemma_] = 1
                    continue
                else:
                    new_amount = subjects[token.lemma_] + 1
                    subjects[token.lemma_] = new_amount

            if token.dep_.endswith("obj"):
                if token.lemma_ not in objects:
                    objects[token.lemma_] = 1
                    continue
                else:
                    new_amount = objects[token.lemma_] + 1
                    objects[token.lemma_] = new_amount
                    
    sorted_verbs = dict(    list(sorted(verbs.items(),
                                key=lambda item: item[1],
                                reverse=True))[:10])

    sorted_subjects = dict( list(sorted(subjects.items(),
                                key=lambda item: item[1],
                                reverse=True))[:10])

    sorted_objects = dict(  list(sorted(objects.items(),
                                key=lambda item: item[1],
                                reverse=True))[:10])
    
    return sorted_verbs, sorted_subjects, sorted_objects

def write_results(results):
    verbs, subjects, objects = results
    with open(r"/Users/admin/Desktop/Most10.txt", mode="w+", encoding="utf-8") as new_text:
        for verb, subj, obj in zip(verbs.items(), subjects.items(), objects.items()):  
            verb_amont, subject_amount, object_amount = str(verbs[verb]), str(subjects[subj]), str(objects[obj])
            new_text.write( verb + " " + verb_amont + "/t" + subj + " " + subject_amount + "/t" + obj + " " + object_amount)


nlp = spacy.load('en_core_web_sm')
file_directory = os.path.expanduser(r"/Users/admin/Desktop/Workplace/Data/reuters21578")
texts = get_texts(file_directory)
results = detect_pos(texts)
write_results(results)