import os
from random import choice


def read(path, file):
    with open(path + "\\" + file) as f:
        lines = f.read()
        return lines


class RandomDescription:

    def __new__(cls, path):
        files = os.listdir(path)
        files = [f for f in files if os.path.isfile(path + '/' + f)]
        file = choice(files)
        data = read(path, file)
        return data
