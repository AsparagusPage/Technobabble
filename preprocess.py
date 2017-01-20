#!/usr/bin/env python3

import argparse
import re

import nltk
from nltk.corpus import stopwords
import pandas as pd

def main():
    parser = argparse.ArgumentParser(\
            description="Preprocess CSV of subtitles for training word2vec model")
    parser.add_argument("csv", help="CSV file of subtitles to preprocess")
    parser.add_argument("--write-prefix", default="corpus", help="prefix to use for output file name")
    parser.add_argument("--column", default="text", help="the column to find text in in the csvs")
    parser.add_argument("--keepstop", action="store_true", help="keep stopwords")
    parser.add_argument("--lemma", action="store_true", help="lemmatize")
    parser.add_argument("--append", action="store_true", help="Append to file instead of write")
    args = parser.parse_args()


    # Read the text to be preprocessed
    df = pd.read_csv(args.csv, delimiter="\t", quoting=3)
    df = df.fillna("")
    texts = df[args.column]

    # Include options used in filename
    filename = args.write_prefix
    if args.keepstop:
        filename += "-keepstop"
    if args.lemma:
        filename += "-lemma"
    filename += ".txt"

    # Determine whether to overwrite or append
    file_flag = "a" if args.append else "w"

    # Write the preprocessed text into the new file
    with open(filename, file_flag) as f:
        f.write(preprocess(texts, args.keepstop, args.lemma))

def preprocess(texts, keepstop, lem, stops=None):
    if stops is None:
        stops = set(stopwords.words("english"))
    processed_texts = []
    # For each row of raw text
    for text in texts:
        # Break into sentences and clean each sentence
        text_sents = nltk.tokenize.sent_tokenize(text)
        text_sents = [clean(sent, keepstop, lem, stops) for sent in text_sents]
        # Join sentences back together, separated by new line
        processed_text = "\n".join(text_sents)
        processed_texts.append(processed_text)
    # Join everything back together, separated by new line
    return "\n".join(processed_texts)

def clean(text, keepstop, lem, stops):
    # Remove punctuation and make everything lower case
    text = strip_punct(text.lower())
    # Remove stopwords unless told otherwise
    if not keepstop:
        text = strip_stopwords(text, stops)
    # Lemmatize words if asked to
    if lem:
        text = lemmatize(text)

    return text

def strip_punct(text):
    return re.sub("[^a-zA-Z]", " ", text)

def strip_stopwords(text, stops):
    # Throw out stopwords
    words = [word for word in text.lower().split() if word not in stops]

    return " ".join(words)

def lemmatize(text):
    # Tag words with parts of speech for WordNetLemmatizer
    tagged_text = word_net_tag(text)
    lemmed_text = []
    # Initialize lemmatizer
    lemma = nltk.stem.wordnet.WordNetLemmatizer()
    # Lemmatize each word according to its part of speech
    for word, tag in tagged_text:
        lemmed_text.append(lemma.lemmatize(word, tag))

    return " ".join(lemmed_text)

def word_net_tag(text):
    # Tag the text with nltk's part of speech tagger
    text_tuples  = nltk.pos_tag(nltk.tokenize.word_tokenize(text))
    # Tuples are inflexible, convert to list of lists
    tagged_text = []
    for tup in text_tuples:
        tagged_text.append(list(tup))
    # Convert the tags to the ones used by the word net lemmatizer.
    # Inspired by a post on theforgetfulcoder.blogspot.com
    tag_dict = {"NN":"n", "JJ":"a", "VB":"v", "RB":"r"}
    for pair in tagged_text:
        if pair[1][:2] in tag_dict:
            # Only look at the first two letters of original tag.
            pair[1] = tag_dict.get(pair[1][:2])
        # If something's weird, tag with WordNetLemmatizer's default "n"
        else:
            pair[1] = "n"


    return tagged_text

if __name__ == "__main__":
    main()
