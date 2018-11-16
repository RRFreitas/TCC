#!/usr/bin/env python3
import pickle

print("[INFO] carregando encodings...")
data = pickle.loads(open("encodings.pickle", "rb").read())

#print(str(data["encodings"][0]))

t = list(str(data["encodings"][0]))
print(t)