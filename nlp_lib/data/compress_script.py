import pickle, gzip
import numpy as np
import pandas as pd
from spacy.tokens import Doc, DocBin
from pathlib import Path
import spacy

BASE_DIR = Path(__file__).parent


import spacy
import numpy as np
from spacy.tokens import DocBin

nlp = spacy.load("pt_core_news_lg")
doc_bin = DocBin().from_disk(BASE_DIR / "target_words_compressed.bin")
docs = list(doc_bin.get_docs(nlp.vocab))

words = []
vectors = []
for doc in docs:
    for token in doc:
        if token.has_vector:
            words.append(token.text)
            vectors.append(token.vector)

np.savez_compressed(BASE_DIR / "target_words_compressed.npz", words=np.array(words), vectors=np.array(vectors))


