class FileManager:

    @staticmethod
    def get_filesdata(filename, emails=False):
        if emails:
            with open(filename) as file:
                lines = file.read().splitlines()
        else:
            with open(filename, encoding='utf-8') as file:
                lines = file.read().splitlines()
        return lines
