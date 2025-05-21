import json
import pickle


def jsonToPkl():
    settings = json.load(open("data/settings/key.json"))
    pickle.dump(settings, open("data/settings/key.pkl", "wb"))
