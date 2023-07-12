import os.path
import spacy as sp
import pandas as pd
import numpy as np

def get_texts(file_directory, mode="r", encoding="utf-8"):
    text_names, text_datas = list(), list()
    entire_text = ""
    for text_name in os.listdir(file_directory):
        if text_name.endswith(".txt"):          
            file_path = os.path.join(str(file_directory), text_name)
            with open(file_path, mode='r', encoding='utf-8', errors='ignore') as text:
                text_data = text.read()
            text_names.append(text_name)
            text_datas.append(text_data)
            entire_text += text_data + " "
    return text_names, text_datas, entire_text

def get_BoW():
    text_names, text_datas, entire_text = get_texts(file_directory)
    bows = dict()
    global_dict = list()
    for token in nlp(entire_text):
        lemma = token.lemma_
        if (lemma not in stop_words) and (lemma.isalpha() == True) and (lemma not in global_dict):
                global_dict.append(lemma)

    for text_name, text_data in zip(text_names, text_datas):
        vector = [ 0 ] * len( global_dict )
        for word in nlp(text_data):
            if word.lemma_ in global_dict:
	            vect_pos = global_dict.index(word.lemma_)
	            vector[ vect_pos ] += 1
        bows[text_name] = vector
    df = pd.DataFrame(index=bows.keys(), data=bows.values(), columns=global_dict)
    return df

def apply_threshold(df, given_threshold):
    #given_threshold = input("Please enter a threshold: ")
    new_df = df.copy(deep=True)
    binarise = lambda value: 0 if value < given_threshold else 1
    filtered = np.vectorize(binarise)
    i = 0
    for arr in df.values:
        #Apply to Rows
        new_df.iloc[i,] = filtered(arr)
        i += 1

    dont_remove = list()
    for i in (range(len(new_df.columns))):
        #Apply to Columns
        if np.sum(new_df.iloc[:,i]) > 0:
            dont_remove.append(i)
    filtered_df = new_df.iloc[:, dont_remove]
    return filtered_df

def get_graph(df):
    import matplotlib.pyplot as plt
    threshold = 0
    threshold_data = list()
    for threshold in range(11):
        filtered = apply_threshold(df, threshold)
        threshold_data.append(len(filtered.columns))
    plt.scatter(threshold_data)
    plt.xlabel(r"Threshold")
    plt.ylabel(r"Sentence Amount")
    plt.show()

def get_zScore(df):
    z_scores = list()
    for column_index in range(len(df.columns)):
        column_array = np.array(df.iloc[:,column_index])
        total_freq = np.sum(column_array)
        text_amount = len(column_array)
        for row_index in range(len(df)):
            freq = column_array[row_index]
            z_score = (freq - (total_freq/text_amount)) / np.std(column_array)
            z_scores.append(z_score)

def get_iFIdF(df):
    to_remove = list()
    for column_index in (range(len(df.columns))):
        column_array = df.iloc[:,column_index]
        row_scores = list()
        for row_index in range(len(df)):
            freq = column_array[row_index]
            docs_inc = sum(el > 0 for el in column_array)
            score = freq * np.log(len(df) / docs_inc)
            row_scores.append(score)

        if sum(row_scores) == 0:
            to_remove.append(column_index)
    filtered_df = df.drop(df.columns[to_remove],axis = 1)
    return tfidf_dict

def Jaccard_dissimilarity(vect_1, vect_2):
    intersection = len(list(set(vect_1).intersection(vect_2)))
    union = (len(set(vector_1)) + len(set(vector_2))) - intersection
    result = float(intersection) / union
    return result
def Manhattan_distance(vect_1, vect_2):
    result = sum(abs(vect_1 - vect_2))
    return result
def Euclidean_distance(vect_1, vect_2):
    result = np.sqrt(np.sum(np.square(vect_1 - vect_2)))
    return result
def Cosine_dissimilarity(vect_1, vect_2):
    result = 1 - (np.dot(vect_1, vect_2) / (np.linalg.norm(vect_1) * np.linalg.norm(vect_2)))
    return result

def PCA_reduction(df, information_ratio=0.9):
    from sklearn.decomposition import PCA
    for n in range(len(df.columns)):
        pca = PCA(n_components=n)
        pca_reduced_data = pca.fit_transform(df)
        results = sum(pca.explained_variance_ratio_)
        if results >= information_ratio:
            break
    return pca_reduced_data

def SVD_reduction(df):
    from sklearn.decomposition import TruncatedSVD
    svd = TruncatedSVD(n_components=2)
    svd_reduced_data = svd.fit_transform(df)
    return svd_reduced_data

def get_MDS(df):
    from sklearn.manifold import MDS
    mds = MDS(n_components=2)
    scaled_df = mds.fit_transform(df)
    plt.scatter(scaled_df[:,0], scaled_df[:,1])
    plt.show()

def get_tSNE(df):
    from sklearn.manifold import TSNE
    tsne = TSNE(n_components=2)
    tsne_result = tsne.fit_transform(df.to_numpy())
    tsne_result.shape
    tsne_result_df = pd.DataFrame({'tsne_1': tsne_result[:,0], 'tsne_2': tsne_result[:,1]})

def main(input_directory, output_directory):
    file_directory = os.path.expanduser(r"/Users/admin/Desktop/Workplace/Data/my_texts")
    nlp = sp.load('en_core_web_sm')
    stop_words = sp.lang.en.stop_words.STOP_WORDS
    texts = get_texts(input_directory)
    bow = get_BoW()
    get_graph(df)
    
if (__name__ == "__main__"):
    input_directory = os.path.expanduser(r"/Users/admin/Desktop/Workplace/Data/my_texts")
    output_directory = os.path.expanduser(r"/Users/admin/Desktop/threshold_graphs.jpg")
    main(input_directory, output_directory)
    