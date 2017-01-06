#!/usr/bin/env python3

import argparse

import nltk
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Preprocess CSV of subtitles")
    parser.add_argument("csv", help="CSV of subtitles to preprocess")
    parser.add_argument("--write-prefix", default="corpus", help="prefix to use for output file name")
    parser.add_argument("--column", default="text", help="the column to find text in in the csvs")
    parser.add_argument("--nopunc", action="store_true", help="strip punctuation")
    parser.add_argument("--nostop", action="store_true", help="remove stopwords")
    parser.add_argument("--lemma", action="store_true", help="lemmatize")
    parser.add_argument("--stem", action="store_true", help="stem")
    args = parser.parse_args()


    df = pd.read_csv(args.csv)
    texts = df[args.column]
    filename = args.write_prefix

    if args.nopunc:
        print("Stripping punctuation...")
        filename += "-nopunc"
        texts = map(strip_punc, texts)

    if args.nostop:
        print("Stripping stopwords...")
        filename += "-nostop"
        texts = map(strip_stopwords, texts)

    if args.lemma:
        print("Lemmatizing...")
        filename += "-lemma"
        texts = map(lemmatize, texts)

    if args.stem:
        print("Stemming...")
        filename += "-stem"
        texts = map(stem, texts)

    filename += ".csv"

    df[args.column] = texts

    df.to_csv(filename)

def tokenize(text, strategy):
    return nltk.tokenizer.word_tokenize(text)

if __name__ == "__main__":
    main()
