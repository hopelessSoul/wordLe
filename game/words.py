import random
import os

from dotenv import load_dotenv
load_dotenv()


def get_word(word_len) -> str:
    path = os.path.abspath(f'../src/words_{os.getenv("GAME_LANG")}')

    with open(path, encoding='utf-8') as file:
        words = file.readlines()
        words = [i for i in words if i.rstrip().__len__() == int(word_len)]
    word = random.choice(words)
    return word.lstrip().rstrip()


