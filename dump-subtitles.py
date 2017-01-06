#!/usr/bin/env python3

import argparse
import csv
import re
import sys

import pysrt

def main():
    parser = argparse.ArgumentParser(description="Extract subtitles")
    parser.add_argument("csvfile", help="name of csv \
                        file to write")
    parser.add_argument("--encoding", default="ISO-8859-2", help="character \
                        encoding of subtitles")
    parser.add_argument("subtitles", nargs="*", help="list of subtitle file \
                        names")
    args = parser.parse_args()

    print("Extracting subtitles and episode labels")
    subs = get_subtitles(args.subtitles, args.encoding)
    eps = get_episodes(args.subtitles)
    print("Writing csv file")
    with open(args.csvfile, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(zip(eps,subs))
    print("done!")

def get_subtitles(files, encoding):
    # text of subtitles
    subtitles = []
    # For each argument passed to this script (paths)
    for filename in files:
        # text of subtitles in that file
        scriptSubs = []
        # For each sub-title object in the file
        for sub in pysrt.open(filename, encoding=encoding):
        # Add a clean version of our text to the script subtitle collection
            scriptSubs.append(clean(sub.text))
        # Add the clean version to the general subtitle collection
        subtitles.append(" ".join(scriptSubs))

    return subtitles

def clean(text):
    # Remove leading "- " and join lines
    text =  " ".join(re.sub("^- ", "", line) for line in text.split("\n"))
    # Remove HTML
    text = re.sub("<.*>", "", text)

    return text

def get_episodes(files):
    # episode labels
    episodes = []
    # For each sub-title object in the file
    for filename in files:
        # Add the label to the episode label collection
        episodes.append(make_episode(filename))

    return episodes

def make_episode(filename):
    # Find the season and episode numbers in the filename
    nums = re.search("(\d{1,2})x(\d{2}(?:-\d{2})?)", filename)
    # If the numbers are found
    if nums:
        # Create the episode label
        episode = "S%sE%s" % (nums.group(1), nums.group(2))
    # Otherwise
    else: episode = "n/a"

    return episode

if __name__ == "__main__":
    main()
