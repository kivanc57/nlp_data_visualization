import os.path
import numpy as np
import pandas as pd
from scipy import spatial
import matplotlib.pyplot as plt
from tqdm import tqdm
import json
import spacy as sp

def load_Word2Vec(Word2Vec_path):
    # To extract n-gram from text
    from gensim.models.phrases import Phrases, Phraser
    # To train word2vec
    from gensim.models import Word2Vec
    # To load pre trained word2vec
    from gensim.models import KeyedVectors
    # To read glove word embedding
    from gensim.scripts.glove2word2vec import glove2word2vec
    yelp_df = pd.read_json(Word2Vec_path, lines=True)
    yelp_df.isnull().sum()
    word_list = []
    for row_num in tqdm(range(len(yelp_df))):
        doc = nlp(yelp_df['text'][row_num])
        for token in doc:
            if (token.lemma_ not in word_list) and (token.is_stop == False) and (token.is_alpha == True):
                word_list.append(token.lemma_)
    yelp_df_clean = pd.DataFrame({'Word List': word_list})
        
def load_FastText(FastText_path):
    from gensim.models import FastText
    import io
    f = io.open(FastText_path, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, f.readline().split())
    embeddings_dict = {}
    for line in f:
        tokens = line.rstrip().split(' ')
        word = tokens[0]
        doc = nlp(word)
        for token in doc:
            if (token.lemma_ not in word_list) and (token.is_stop == False) and (token.is_alpha == True):
                embeddings_dict[token.lemma_] = np.asarray(tokens[1:], "float32")
    return embeddings_dict

def load_GloVe(GloVe_path, mode="r", encoding="utf-8"):
    embeddings_dict = {}
    with open(GloVe_path) as f:
        for line in f:
            values = line.split()
            word = values[0]
            doc = nlp(word)
            for token in doc:
                if (token.lemma_ not in word_list) and (token.is_stop == False) and (token.is_alpha == True):
                    vector = np.asarray(values[1:], "float32")
                    embeddings_dict[token.lemma_] = vector
    return embeddings_dict

def get_mean(embedding, embeddings_dict):
    return np.mean( embedding, axis=0 )

def get_euclidean(embedding_A, embedding_B, embeddings_dict):
    return np.sqrt(np.sum(np.square(embedding_A - embedding_B)))

def get_matrix(embeddings, embeddings_dict):
    #Expecting a list of embeddings as the inital input
    dm = spatial.distance.pdist(np.array(embeddings), 'euclidean')
    result =  spatial.distance.squareform(dm)
    return result

def find_closest_10(embedding, embeddings_dict):
    return (sorted(embeddings_dict.keys(), key=lambda word: spatial.distance.euclidean(embeddings_dict[word], embedding)))[1:11]

def get_tSNE(embeddings_dict):
    from sklearn.manifold import TSNE
    tsne = TSNE(n_components=2, random_state=0)
    words =  list(embeddings_dict.keys())
    vectors = [embeddings_dict[word] for word in words]
    Y = tsne.fit_transform(vectors[:100])
    plt.scatter(Y[:, 0], Y[:, 1])
    for label, x, y in zip(words, Y[:, 0], Y[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords="offset points")
    plt.show()

def main(Word2Vec_path, FastText_path, GloVe_path):
    nlp = sp.load("en_core_web_sm", disable=['ner', 'parser']) # disabling Named Entity Recognition for speed
    #embeddings_dict = load_FastText(FastText_path)
    #embeddings_dict = load_GloVe(FastText_path)
    load_Word2Vec(Word2Vec_path)
    #embeddings = [embeddings_dict["information"], embeddings_dict["UTC"]]
    #get_mean(embeddings_dict["information"], embeddings_dict)
    #print(find_closest_10(embeddings_dict["king"], embeddings_dict))
    #get_euclidean(embeddings_dict["dog"], embeddings_dict["cat"], embeddings_dict)
    #get_matrix(embeddings, embeddings_dict)
if __name__ == "__main__":
    Word2Vec_path = os.path.expanduser(r"/Users/admin/Desktop/archive/yelp_academic_dataset_tip.json")
    FastText_path = os.path.expanduser(r"/Users/admin/Desktop/Workplace/Data/wiki-news-300d-1M.vec")
    GloVe_path = os.path.expanduser(r"/Users/admin/Desktop/Workplace/Data/glove.6B/glove.6B.50d.txt")
    main(Word2Vec_path, FastText_path, GloVe_path)