#!/usr/bin/env python3

import argparse
import csv
import re
import sys

import pysrt

def main():
    parser = argparse.ArgumentParser(description="Extract subtitles")
    parser.add_argument("--write", type=argparse.FileType('w'),
            default="subtitles.csv", help="csv file to write to")
    parser.add_argument("--series_tag", default="", help="episode tag prefix")
    parser.add_argument("--encoding", default="ISO-8859-2",
            help="character encoding of subtitle files")
    parser.add_argument("subtitles", nargs="+",
            help="list of subtitle files")
    parser.add_argument("--by_time", action="store_true",
            help="Divide by an additional 'start' column")
    args = parser.parse_args()

    print("Extracting data from subtitles and writing CSV")

    if args.by_time:
        head = ["episode", "text", "start"]
    else:
        head = ["episode", "text"]
    writer = csv.DictWriter(args.write, head, delimiter="\t")
    writer.writeheader()

    for path in args.subtitles:
        episode = get_episode(path, args.series_tag)
        scriptSubs = []
        subTimes = []
        for sub in pysrt.open(path, encoding=args.encoding):
            scriptSubs.append(clean(sub.text))
            if args.by_time:
                subTimes.append(sub.start.ordinal)
        if args.by_time:
            for sub, time in zip(scriptSubs, subTimes):
                row = {"episode": episode, "text": sub, "start": time}
                writer.writerow(row)
        else:
            row = {"episode": episode, "text": " ".join(scriptSubs)}
            writer.writerow(row)

def clean(text):
    # Remove leading "- " and join lines
    text =  " ".join(re.sub("^- ", "", line) for line in text.split("\n"))
    # Remove HTML
    text = re.sub("<.*>", "", text)

    return text

def get_episode(filename, series_tag):
    # Find the season and episode numbers in the filename
    nums = re.search("(\d{1,2})x(\d{2}(?:-\d{2})?)", filename)
    # If the numbers are found
    if nums:
        # Create the episode label
        episode = series_tag + "S%sE%s" % (nums.group(1), nums.group(2))
    # Otherwise
    else: episode = "n/a"

    return episode

if __name__ == "__main__":
    main()
