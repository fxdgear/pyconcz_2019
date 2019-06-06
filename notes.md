# Intro to Search Using Python

* Have you ever used a search engine?
* Have you ever wondered how the basics of search work?

We’ll use Python to delve into the basics of search.
What exactly is an inverted index and how does it help us in trying to build and use search?
What is analysis and how is it used?
How does changing the behavior of analisys change the behavior of our search.
How does it change the behavior of building the inverted index.

Hopefully, after the talk, you’ll walk away with a bit deeper understanding of how
search engines work, which will translate into helping you optimize deploying your own search experiences.

## What is Search?

Search is a very general term, but in most cases when people refer to "search" they want to find specific
segments of text in a much larger corpus of text.

### BasiciSearch Examples:

#### 1. Ctrl-f

We've all used Ctrl-f before. Open a file, keyboard command, type what your looking for. This works great
when you wanna search for a word in a file. But this quickly stops scaling when you start searching in
multiple files

#### 2. grep

I'm sure most of you have used grep before. Much more handy to seach multiple files. Can grep across
a handful of files, traverse a directory structure, etc. This scales well across multiple files. But
when we start having hundreds, thousands, hundreds of thousands, millions, etc...

#### How do we do this in python?

```python
import re

mytext = "Hello PyCon CZ! Welcome to Ostrava!"

x = re.findall("Welcome", mytext)

print(x)

>>> ['Welcome']
```

We can even see this example with a files in a directory structure:

```python
import os
from os.path import join
import re

results = []
for root, dirs, files in os.walk("mydirectory"):
    for file in files:
        with open(join(root, file)) as datafile:
            data = datafile.readlines()
            ret = re.findall("Welcome", data)
             if ret:
                results.appnd(["Welcome", join(root,file)])
print(results)
```

What we've just done here is created a simple inverted index which
holds our search term, the file that it was found on and the line number. This
reverse index doesn't help us much cause we have to create it for every search we make.

## Inverted Index

What is an Index? Ever read a book, and if you flip to the back it lists all the interesting
words alphabetically and lists, in order, the page numbers those words can be found on.

As we saw in the last example we were able to create a simple reverse index which listed our

1. search term
2. our file that the term was found in
3. the line number that the term was found on.

What if instead of creating the reverse index everytime we searched our documents, we created
the reverse index one time and then everytime we wanted to search our documents we would instead
do a lookup on our reverse index.

This process is called "indexing". It's the process of taking a document, breaking it up into
words and then aggregating the page numbers (or filenames) that they exist on.

Lets try indexing some documents in python.

```python
from collections import defaultdict
index = defaultdict(set)

for root, dirs, files in os.walk("mydirectory"):
    for file in files:
        file_path = join(root, file)
        with open(file_path) as datafile:
            for word in data.split(" "):
                file_list = index.get(word, set)
                file_list.add(file_path)

print(index)
```

What we've just done here is created an inverted index where we have index all the words in all
the files and we are able to reference what file each word appears in.

This index isn't very useful though. Why not?

When we create our index in this way what we've done is created an entry for every word. If we have
for example a sentence that says "I will jump the fence, before Susan jumps the fence but after Bret already jumped over the fence."

This sentence demonstrates how bad our index will be. We are going to have the following terms in our index:

* `jump`
* `jumped`
* `jumps`

Typically when we search for a term we want the other tenses of that term as well. This is where we get into what's known as "Analysis".

## Analysis

Analysis in search, is the process of inspecting each token and manipulating it to a root word/term and/or ignoring terms that shouldn't be index.

In Elasticsearch we call the process that does analysis an "Analyzer". Lets look closer at what an analyzer does.

1. Character Filters - In this step we want to transform the string. IE lowercasing a word or substituting
2. Tokenization - The ouput from the Character Filter is passed to the tokenizer which returns a list of tokens
3. Token Filtering - The token filter can do more optional transformations on the idividual tokens.
