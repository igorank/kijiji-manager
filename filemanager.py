class FileManager:

    @staticmethod
    def get_filesdata(filename, emails=False):
        if emails:
            with open(filename) as f:
                lines = f.read().splitlines()
        else:
            with open(filename, encoding='utf-8') as f:
                lines = f.read().splitlines()
        return lines
