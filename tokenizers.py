import string


def standard_tokenizer(input_string):
    """
    Standard Tokenizer returns tokens split on whitespace
    and removes punctuation
    """
    for position, word in enumerate(input_string.split()):
        yield {
            "token": word.translate(word.maketrans("", "", string.punctuation)),
            "position": position,
        }
