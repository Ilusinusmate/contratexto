import asyncio
import pandas as pd
import spacy
from spacy.tokens import DocBin

from game_class import Contratexto
from settings import BASE_DIR

class GameManager:
    def __init__(self, queue_max_size: int):
        self.queue = asyncio.Queue(maxsize=queue_max_size)
        nlp = spacy.load("pt_core_news_lg")

        general_db = DocBin()
        general_db.from_disk(BASE_DIR / "data/dataset_compressed.bin")
        self.general_words_df = tuple(general_db.get_docs(nlp.vocab))

        target_db = DocBin()
        target_db.from_disk(BASE_DIR / "data/target_words_compressed.bin")
        self.target_words = tuple(target_db.get_docs(nlp.vocab))


    def create_game(self):
        return Contratexto(
            self.general_words_df,
            self.target_words,
        )    



    async def worker(self):
        while True:
            await self.queue.put(self.create_game())



    async def get_game(self):
        return await self.queue.get()


if __name__ == "__main__":
    games = []
    async def main():
        gm = GameManager(queue_max_size=3)
        task = asyncio.create_task(gm.worker())

        # pega alguns jogos
        for _ in range(5):
            game = await gm.get_game()
            print("Got game:", game)
            games.append(game)

        # encerra o worker
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("Worker cancelled")

    asyncio.run(main())