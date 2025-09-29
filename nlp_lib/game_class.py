import numpy as np

class Contratexto:
    def __init__(self, general_words, general_vectors, target_words, target_vectors):
        self.GameData = {}
        self.general_words: np.ndarray = general_words
        self.general_vectors: np.ndarray = general_vectors
        self.target_words: np.ndarray = target_words
        self.target_vectors: np.ndarray = target_vectors

        self.target_idx = self._get_random_target_index()
        self.target_word = self.target_words[self.target_idx]
        self.target_vector = self.target_vectors[self.target_idx]

        self.normalization = {
            "ç": "c", "ã": "a", "á": "a", "â": "a",
            "õ": "o", "ó": "o", "ô": "o",
            "ẽ": "e", "é": "e", "ê": "e",
            "ĩ": "i", "í": "i", "î": "i",
            "ũ": "u", "û": "u", "ú": "u",
        }

        self.create_game_data()

    def _cosine_similarity(self, vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def create_game_data(self):
        self.GameData = {}
        word_list = []

        for word, vector in zip(self.general_words, self.general_vectors):
            coef = self._cosine_similarity(self.target_vector, vector)
            word_list.append((coef, word))

        word_list.sort()

        for idx, element in enumerate(word_list):
            word: str = element[1].lower()
            self.GameData[word] = idx + 1
            self.GameData[idx + 1] = word

    def normalize(self, input_str: str) -> str:
        res = input_str
        for letra, replacement in self.normalization.items():
            res = res.replace(letra, replacement)
        return res.lower()

    def get_word_in_position(self, pos: int) -> str | None:
        return self.GameData.get(pos, None)

    def guess_word(self, word: str) -> int | None:
        word = self.normalize(word)
        return self.GameData.get(word, None)

    def _get_random_target_index(self):
        return np.random.randint(len(self.target_words))
