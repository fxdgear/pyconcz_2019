from collections import defaultdict
from character_filters import html_strip
from tokenizers import standard_tokenizer
from token_filters import (
    lowercase_tokenfilter,
    snowball_tokenfilter,
    stopword_tokenfilter,
)


class Analyzer(object):
    def __init__(self, char_filters=None, tokenizer=None, token_filters=None):
        self.char_filters = char_filters
        self.tokenizer = tokenizer
        self.token_filters = token_filters

    def analyze(self, text):
        """
        Analyze a string of text.

        Returns a listcomp of tokens which have:
          * been run through the token filters
          * which were created by the tokenizer
          * which were created from a string which had run through the character filters.

        """
        # First we run the string through the character filters
        filtered_text = self._character_filtering(text)

        # next we will tokenize the text
        for token in self._tokenize(text):

            # yield a token_filtered token.
            yield self._token_filtering(token)

    def _character_filtering(self, text):
        """
        For each character filter, run the text through the character filters.
        Return the finalized filtered text.
        """
        for char_filter in self.char_filters:
            text = char_filter(text)

        return text

    def _tokenize(self, text):
        for token in self.tokenizer(text):
            yield token

    def _token_filtering(self, token):
        for token_filter in self.token_filters:
            token = token_filter(token)

        return token


class Index(object):
    def __init__(
        self,
        analyzer=Analyzer(
            char_filters=[html_strip],
            tokenizer=standard_tokenizer,
            token_filters=[
                lowercase_tokenfilter,
                snowball_tokenfilter,
                stopword_tokenfilter,
            ],
        ),
    ):
        def default_factory():
            return {"linenumbers": set(), "tokens": list()}

        self._index = defaultdict(default_factory)
        self.analyzer = analyzer

    def index(self, document):
        with open(document) as docfile:
            for linenumber, line in enumerate(docfile.readlines()):
                for token in self.analyze(line):
                    token.update({"linenumber": linenumber, "line": line})
                    self._index[token["token"]]["linenumbers"].add(linenumber)
                    self._index[token["token"]]["tokens"].append(token)

    def analyze(self, line):
        return self.analyzer.analyze(line)

    def _highlight_line(self, token):
        highlighed_line = token["line"].split()
        highlighed_line[token["position"]] = f"]]{highlighed_line[token['position']]}[["
        return " ".join(highlighed_line)

    def search(self, term):
        analyzed_term = self.analyze(term)
        tokens = [x["token"] for x in analyzed_term]
        try:
            search_results = {}
            results = [self._index[token] for token in tokens]
            for result in results:
                for token in result["tokens"]:
                    print(f"{token['linenumber']}:\t{self._highlight_line(token)}")

        except KeyError:
            return None
