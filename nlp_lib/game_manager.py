import asyncio
import numpy as np
import random

from nlp_lib.game_class import Contratexto
from nlp_lib.settings import BASE_DIR

class GameManager:
    def __init__(self, queue_max_size: int):
        self.queue = asyncio.Queue(maxsize=queue_max_size)

        # carregar os npz
        general = np.load(BASE_DIR / "data/dataset_compressed.npz", allow_pickle=True)
        target = np.load(BASE_DIR / "data/target_words_compressed.npz", allow_pickle=True)

        self.general_words = general["words"]
        self.general_vectors = general["vectors"]

        self.target_words = target["words"]
        self.target_vectors = target["vectors"]

        self.current_game: Contratexto | None = None

    def create_game(self):
        return Contratexto(
            self.general_words,
            self.general_vectors,
            self.target_words,
            self.target_vectors,
        )

    async def worker(self):
        while True:
            await self.queue.put(self.create_game())
            print("LOG: GAME ADDED TO QUEUE")

    async def get_game(self):
        print("LOG: GAME RETRIEVED FROM QUEUE")
        if self.current_game is not None:
            return self.current_game
        self.current_game = await self.queue.get()
        return self.current_game

    def end_game(self):
        self.current_game = None
