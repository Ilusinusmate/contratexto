from random import choice
from typing import List

from settings import BASE_DIR


class Contratexto():
    def __init__(self, general_words_df, target_words):
        self.GameData = {}
        self.general_words_df: tuple = general_words_df
        self.target_words: tuple = target_words
        self.target_word = self._get_random_target_word()
        self.normalization = {
            "ç" : "c",
            "ã" : "a",
            "á" : "a",
            "â" : "a",
            "õ" : "o",
            "ó" : "o",
            "ô" : "o",
            "ẽ" : "e",
            "é" : "e",
            "ê" : "e",
            "ĩ" : "i",
            "í" : "i",
            "î" : "i",
            "ũ" : "u",
            "û" : "u",
            "ú" : "u",
        }


        self.create_game_data()



    def create_game_data(self):  
        self.GameData = {}      

        for palavra in self.general_words_df:
            if not palavra.has_vector: continue

            if not self.target_word.has_vector: 
                self.target_word = self._get_random_target_word()
                self.create_game_data()

            coef = self.target_word.similarity(palavra)
            self.GameData[palavra.text] = coef 
    
        word_list: List = list(self.GameData.items())
        
        word_list.sort(reverse = True, key=lambda x: x[1])

        for idx, element in enumerate(word_list):
            word: str = element[0].lower()
            self.GameData[word] = idx + 1
            self.GameData[idx + 1] = word



    def normalize(self, input_str: str) -> str:
        res = input_str
        for letra, replacement in self.normalization.items():
            res = res.replace(letra, replacement)
        return res.lower()



    def search_word_position(self, pos: int) -> str:
        return self.GameData.get(pos, None)



    def get_position_of_word(self, word: str) -> int:
        word = self.normalize(word)
        return self.GameData.get(word, None)


    
    def _get_random_target_word(self):
        return choice(self.target_words)