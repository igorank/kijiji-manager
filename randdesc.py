import os
from random import choice


def read(path, file):
    with open(path + "\\" + file) as f:
        lines = f.read()
        return lines


class RandomDescription:

    def __new__(cls, path):
        files = []
        for x in os.listdir(path):
            if x.endswith(".txt"):
                files.append(x)
        print(files)
        file = choice(files)
        data = read(path, file)
        return data
