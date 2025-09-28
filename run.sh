#!/bin/bash 

pip install -r requirements.txt

python3 -m spacy download pt_core_news_lg

python3 -m main.py