import json
import pickle

settings = json.load(open("data/settings/key.json"))
pickle.dump(settings, open("data/settings/key.pkl", "wb"))
