#!/usr/bin/env python3

import sys
import re

import pysrt

def main():
    # text of subtitles
    subtitles = []

    # For each argument passed to this script (paths)
    for filename in sys.argv[1:]:
        # text of subtitles in that file
        scriptSubs = []
        # For each sub-title object in the file
        for sub in pysrt.open(filename):
            # Add a clean version of our text to the script subtitle collection
            scriptSubs.append(clean(sub.text))
        # Add the clean version to the general subtitle collection
        subtitles.append(" ".join(scriptSubs))

    save(subtitles)

def clean(text):
    # Remove leading "- " and join lines
    text =  " ".join(re.sub("^- ", "", line) for line in text.split("\n"))
    # Remove HTML
    text = re.sub("<.*>", "", text)

    return text

def save(subs):
    for text in subs:
        print(text)

if __name__ == "__main__":
    main()
