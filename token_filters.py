import snowballstemmer

with open("./stopwords") as stopwords:
    STOPWORDS = stopwords.readlines()


def lowercase_tokenfilter(token):
    """
    Convert all tokens to lowercase value
    """
    token["token"] = token["token"].lower()
    return token


def stopword_tokenfilter(token):
    """
    Token filter to remove stop words
    """
    if token["token"] not in STOPWORDS:
        return token
    return None


def snowball_tokenfilter(token):
    """
    Snowball token filter

    uses the Snowball stemming library collection for python:
      https://github.com/shibukawa/snowball_py
    """
    stemmer = snowballstemmer.stemmer("english")
    token["token"] = stemmer.stemWord(token["token"])
    return token
