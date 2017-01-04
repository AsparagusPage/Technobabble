#!/usr/bin/env python3

import sys
import re

import pysrt

def main():
    # text of subtitles
    subtitles = []

    # For each argument passed to this script (paths)
    for filename in sys.argv[1:]:
        # For each sub-title object in that file
        for sub in pysrt.open(filename):
            # Add a clean version of our text to our subtitle collection
            subtitles.append(clean(sub.text))

    save(subtitles)

def clean(text):
    return text

def save(subs):
    for text in subs:
        print("---- BEGIN ---- ")
        print(text)
        print("---- END ----")

if __name__ == "__main__":
    main()
