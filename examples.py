import click
import os
import re
import json
import string
from os.path import join
from collections import defaultdict
from html.parser import HTMLParser
import ipdb


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return "".join(self.fed)


@click.group()
def cli():
    """
    Welcome to my search example...
    """
    pass


@cli.command()
def example1():
    """
    Simple search example to find a word in a string.

    using the Regex lib we can find words in a string.
    """
    mytext = "Hello PyCon CZ! Welcome to Ostrava!"

    x = re.findall("Welcome", mytext)

    print(x)


@cli.command()
def example2():
    """
    Search files across a folder structure.

    :arg

    We will walk the file structure and append our results
    to a results list.
    """
    results = []
    search_term = "lorem"
    for root, dirs, files in os.walk("./files"):
        for filename in files:
            file_path = join(root, filename)
            with open(file_path, "r") as datafile:
                data = datafile.readlines()
                ret = re.findall(search_term, "".join(data))
                if ret:
                    results.append([search_term, file_path])
    print(results)


@cli.command()
def example3():
    """
    Create a really simple inverted index

    This inverted index isn't very helpful. Why?

    Because we don't do any analysis on the words before generating
    the index.
    """
    index = defaultdict(set)
    search_term = "lorem"
    for root, dirs, files in os.walk("./files"):
        for file_name in files:
            file_path = join(root, file_name)
            with open(file_path) as datafile:
                data = "".join(datafile.readlines())
                for word in data.split():
                    index[word].add(file_path)

    for term, filenames in index.items():
        print(f"{term}:\t{filenames}")


@cli.command()
def example4():
    """
    Example Analyzer
    """
    mytext = "<p>I will jump the fence, before Susan jumps the fence but <em>after</em> Bret has already jumped over the fence</p>"

    def charfilter(input_string):
        s = MLStripper()
        s.feed(input_string)
        return s.get_data()

    def tokenizer(input_string):
        for position, word in enumerate(input_string.split()):
            yield {
                "token": word.translate(word.maketrans("", "", string.punctuation)),
                "position": position,
            }

    def token_filter(token):
        token["token"] = token["token"].lower()
        return token

    def analyize(input_string):
        print("Character filter will strip out html...\n")
        print(f"Before: {input_string}")
        input_string = charfilter(input_string)
        print(f"After: {input_string}")

        print(
            "\nStandard tokenizer will separate the tokens on whitespace and strip punctuation"
        )
        print(f"{[x for x in tokenizer(input_string)]}")

        print("\nLowercase tokenfilter will lowercase all the tokens.")
        print(f"{[token_filter(token) for token in tokenizer(input_string)]}")

    analyize(mytext)


if __name__ == "__main__":
    cli()
