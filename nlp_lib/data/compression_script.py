import pickle, gzip
import numpy as np
import pandas as pd
from spacy.tokens import Doc, DocBin
from pathlib import Path
import spacy

BASE_DIR = Path(__file__).parent

INPUT_FILE = "a.csv"
OUTPUT_FILE = "target_words_compressed.bin"


dataset = pd.read_csv(BASE_DIR / INPUT_FILE)
nlp = spacy.load("pt_core_news_lg")
data = nlp.pipe(dataset["palavras"], batch_size=10000)

db = DocBin()
for item in data:
    db.add(item)

db.to_disk(BASE_DIR / OUTPUT_FILE)