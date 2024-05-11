"""
    Creation date:
        5th May 2024
    Creator:
        B.Delorme
    Main purpose:
        
        
        
        Create a special category for expressions that contains several words,
        or even a whole and independent sentence.
"""

import json
# import os
# import pickle
# import sys

import numpy as np
from abc import ABC, abstractmethod
from loguru import logger
from tensorflow.keras.layers import Embedding, Dense, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import make_sampling_table
from tensorflow.keras.preprocessing.sequence import skipgrams
from tensorflow.keras.preprocessing.text import Tokenizer

EMBEDDING_DIM = 100



class MLHandler(ABC):
    """
    Class that defines the interface between the app and the Machine Learning models.

    Mish-mash between dev and MLOps.
    """
    def __init__(self, user_name, db_name):
        self.user_name = user_name
        self.db_name = db_name

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass



with open('./conf/ml_models/ml.json', 'r') as json_file:
    ML_JSON = json.load(json_file)


def pre_process_text_data(text_corpus):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(text_corpus)
    return tokenizer


def create_training_samples(tokenizer):
    vocab_size = len(tokenizer.word_index) + 1
    sequences = [i for i in range(0, vocab_size)]
    sampling_table = make_sampling_table(vocab_size)
    skip_grams = skipgrams(
        sequences,
        vocab_size,
        window_size=4,
        sampling_table=sampling_table
    )
    skip_grams = skip_grams[0]
    return skip_grams


def encode_training_samples(skip_grams):
    target_words, context_words = zip(*skip_grams)
    return target_words, context_words


def create_raw_model(tokenizer_fitted, embedding_dim):
    """
    Define your neural network architecture
    """
    vocab_size = len(tokenizer_fitted.word_index) + 1
    model = Sequential([
        Embedding(
            vocab_size,
            embedding_dim,
            input_length=1
        ),
        Flatten(),
        Dense(
            vocab_size,
            activation='softmax'
        )
    ])
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer='adam'
    )
    return model


def train_model(model, target_words, context_words):
    model.fit(
        x=np.array(target_words),
        y=np.array(context_words),
        epochs=20
    )
    return model


def load_word_vectors(model):
    """
    Retrieve the learned word vectors from the embedding layer.
    
    `word_vectors` will be a 2D numpy array
    where each row corresponds to the embedding vector for a word
    
    The shape of `word_vectors` will be (vocab_size, embedding_dim),
    where `vocab_size` is the size of the vocabulary
    and `embedding_dim` is the dimensionality of the word embeddings
    """
    # Assuming the embedding layer is the first layer in the model
    embedding_layer = model.layers[0]
    word_vectors = embedding_layer.get_weights()[0]
    return word_vectors


def calculate_concept_embedding(tokenizer, notion_sequences, word_vectors):
    concept_embeddings = []
    logger.debug(f"Number of notion sequences: {len(notion_sequences)}")
    logger.debug(f"Word vectors shape: {word_vectors.shape}")
    for notion_seq in notion_sequences:
        related_words = [
            tokenizer.index_word[idx]
            for idx in notion_seq
            if idx in tokenizer.index_word
        ]
        logger.debug(f"notion: {notion_seq}")
        logger.debug(f"Related words: {related_words}")
        concept_embedding = np.mean(
            [
                word_vectors.get(word, np.zeros(word_vectors.vector_size))
                for word in related_words
            ],
            axis=0
        )
        concept_embeddings.append(concept_embedding)
    return concept_embeddings


def get_matrix_embedding(text_corpus, notions, embedding_dim):
    tokenizer = pre_process_text_data(text_corpus)
    notion_sequences = tokenizer.texts_to_sequences(notions)
    skip_grams = create_training_samples(tokenizer)
    target_words, context_words = encode_training_samples(skip_grams)
    model = create_raw_model(tokenizer, embedding_dim)
    model = train_model(model, target_words, context_words)
    word_vectors = load_word_vectors(model)
    concept_embeddings = calculate_concept_embedding(
        tokenizer,
        notion_sequences,
        word_vectors
    )
    embedding_matrix = np.vstack(concept_embeddings)
    return embedding_matrix


def get_text_corpus():
    words_sample_dict = ML_JSON['words_sample']
    text_corpus = []
    for key, values in words_sample_dict.items():
        text_corpus.extend(values)
    return text_corpus


if __name__ == '__main__':
    text_corpus = get_text_corpus()
    embedding_matrix = get_matrix_embedding(
        text_corpus,
        ML_JSON['notions'],
        EMBEDDING_DIM
    )
    print(embedding_matrix.shape)
    print(embedding_matrix[0])
    print(embedding_matrix[0])
    print(embedding_matrix)
