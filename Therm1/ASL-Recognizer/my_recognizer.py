import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD': LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD': LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    test_sequences = list(test_set.get_all_Xlengths().values())
    try:
        for test_X, test_length in test_sequences:
            best_score = float('-inf')
            best_word = None
            logL_dict = {}
            for word, model in models.items():
                logL = model.score(test_X, test_length)
                logL_dict[word] = logL
                if logL > best_score:
                    best_score = logL
                    best_word = word
            probabilities.append(logL_dict)
            guesses.append(best_word)
    except:
        pass
    return probabilities, guesses
