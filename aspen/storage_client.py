class StorageClient:
    def __init__(self, credentials=None):
        self.credentials = credentials

    def read(self, read_storage):
        data = read_storage.read()
        print(data)
        return data

    def read_to_write(self, read_storage, write_storage):

        data = read_storage.read()
        write_storage.write(data)
