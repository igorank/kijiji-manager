import os
from random import choice


def read(path, file):
    with open(path + "\\" + file) as f:
        lines = f.read()
        return lines


class RandomDescription:

    def __new__(cls, path):
        files = []
        for i in os.listdir(path):
            if i.endswith(('.txt', '.TXT')):
                files.append(i)
        file = choice(files)
        data = read(path, file)
        return data
