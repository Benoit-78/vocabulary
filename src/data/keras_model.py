
import json

import numpy as np


with open('./conf/ml_models/ml.json', 'r', encoding='utf-8') as json_file:
    ML_JSON = json.load(json_file)

notions = ML_JSON['notions']

path_to_glove_file = "./data/embedding/glove.6B.100d.txt"


def get_text_corpus():
    words_sample_dict = ML_JSON['words_sample']
    text_corpus = []
    for key, values in words_sample_dict.items():
        text_corpus.extend(values)
    return text_corpus


embeddings_index = {}
with open(path_to_glove_file) as f:
    for line in f:
        word, coefs = line.split(maxsplit=1)
        coefs = np.fromstring(coefs, "f", sep=" ")
        embeddings_index[word] = coefs

print("Found %s word vectors." % len(embeddings_index))


text_corpus = get_text_corpus()

num_tokens = len(text_corpus) + 2
embedding_dim = 100
hits = 0
misses = 0

# Prepare embedding matrix
embedding_matrix = np.zeros((num_tokens, embedding_dim))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # Words not found in embedding index will be all-zeros.
        # This includes the representation for "padding" and "OOV"
        embedding_matrix[i] = embedding_vector
        hits += 1
    else:
        misses += 1
print("Converted %d words (%d misses)" % (hits, misses))



