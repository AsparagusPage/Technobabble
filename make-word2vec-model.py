#!/usr/bin/env python3

import argparse
import logging

from gensim.models import word2vec

def main():

    parser = argparse.ArgumentParser(description="Save a word2vec model")
    parser.add_argument("training_corpus", help="preprocessed file of sentences separated by \n")
    parser.add_argument("--num_features", default=100, type=int, help="word vector dimensionality")
    parser.add_argument("--min_word_count", default=10, type=int, help="minimum word count")
    parser.add_argument("--num_workers", default=4, type=int, help="num threads to run in parallel")
    parser.add_argument("--context", default=5, type=int, help="context window size")
    parser.add_argument("--downsample", default=1e-3, type=float, help="frequent word downsampling setting")
    parser.add_argument("--iter", type=int, help="how many times to iterate over corpus in training")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',\
                            level=logging.INFO)

    with open(args.training_corpus) as file:
        sentences = file.read().splitlines()
    sentences = [sentence.split() for sentence in sentences]

    print("Training model...")
    model = word2vec.Word2Vec(sentences, workers=args.num_workers, \
        size=args.num_features, \
        min_count=args.min_word_count, \
        window=args.context, sample=args.downsample, sg=1, iter=args.iter)
    # Don't plan on continuing to train the model, save memory
    model.init_sims(replace=True)

    model_name = "%dFeatures_%dMinWords_%dContext" % (args.num_features, \
        args.min_word_count, \
        args.context)

    model.save(model_name)

if __name__ == "__main__":
    main()
