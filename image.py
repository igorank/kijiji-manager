class Image:
    """Image data type
    """

    def __init__(self, filename, path):
        self.filename = filename
        self.photo_path = path + "\\" + filename
        self.content_type = f'image/{filename[-3:]}'

    def read(self):
        with open(self.photo_path, "rb") as file:
            return file.read()
