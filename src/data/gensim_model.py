

import json

import numpy as np
from gensim.models import Word2Vec
from gensim.test.utils import common_texts
from loguru import logger

with open('./conf/ml_models/ml.json', 'r') as json_file:
    ML_JSON = json.load(json_file)
notions = ML_JSON['notions']


def download_model():
    model = Word2Vec(
        sentences=common_texts,
        vector_size=100,
        window=5,
        min_count=1,
        workers=4
    )
    model.save("./src/ml_models/word2vec.model")
    logger.success("Model saved")


def get_text_corpus():
    words_sample_dict = ML_JSON['words_sample']
    text_corpus = []
    for key, values in words_sample_dict.items():
        text_corpus.extend(values)
    return text_corpus


def train_model(text_corpus):
    model = Word2Vec.load('./src/ml_models/word2vec.model')
    text_corpus = [["hello", "world"]]
    model.train(
        text_corpus,
        total_examples=1,
        epochs=1
    )
    return model


def calculate_concept_embedding(notions, model):
    concept_embeddings = []
    for notion in notions:
        related_words = [word for word, _ in model.most_similar(notion)]
        concept_embedding = sum(
            model[word]
            for word in related_words
        ) / len(related_words)
        concept_embeddings.append(concept_embedding)
    return concept_embeddings


if __name__ == '__main__':
    download_model()
    text_corpus = get_text_corpus()
    model = train_model(text_corpus)
    concept_embeddings = calculate_concept_embedding(notions, model)
    embedding_matrix = np.vstack(concept_embeddings)
