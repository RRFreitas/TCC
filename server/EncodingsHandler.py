import pickle

class EncodingsHandler:

    def __init__(self, encodingsFile):
        self.encodingsFile = encodingsFile
        self.encodings = self.carregarEncodings()

    def deletarEncodings(self):
        print("[INFO] deletando encodings...")
        self.encodings = {"encodings": [], "ids": []}
        self.salvarEncodings()


    def adicionarEncoding(self, pessoa_id, encoding):
        self.encodings["ids"].append(pessoa_id)
        self.encodings["encodings"].append(encoding)
        self.salvarEncodings()

    def carregarEncodings(self):
        try:
            print("[INFO] carregando encodings...")
            f = open(self.encodingsFile, "rb")
            enc = pickle.loads(f.read())
            f.close()

            print(enc)
            return enc
        except:
            return {"encodings": [], "ids": []}

    def salvarEncodings(self):
        print("[INFO] serializando encodings...")
        print(self.encodings)
        try:
            f = open("encodings.pickle", "wb")
            f.write(pickle.dumps(self.encodings))
            f.close()
            print("[INFO] encodings serializados")
        except Exception as err:
            print(err)
            print("[ERRO] encodings não foram salvos")