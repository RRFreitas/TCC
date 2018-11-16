import pickle

class EncodingsHandler:

    def __init__(self, encodingsFile):
        self.encodingsFile = encodingsFile
        self.encodings = self.carregarEncodings()

    def carregarEncodings(self):
        try:
            return pickle.loads(open(self.encodingsFile, "rb").read())
        except:
            return {"encodings": [], "ids": []}

    def salvarEncodings(self):
        print("[INFO] serializando encodings...")

        try:
            f = open(self.encodingsFile, "wb")
            f.write(pickle.dumps(self.encodings))
            f.close()
        except:
            print("[ERRO] encodings não foram salvos")

    def __del__(self):
        self.salvarEncodings()