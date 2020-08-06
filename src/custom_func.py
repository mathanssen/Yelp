import pickle


def save_obj(obj, name, path):
    """
    Saves object as a file
    """
    with open(path + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
def load_obj(name, path):
    """
    Loads pickle object
    """
    with open(path + name + '.pkl', 'rb') as f:
        return pickle.load(f)