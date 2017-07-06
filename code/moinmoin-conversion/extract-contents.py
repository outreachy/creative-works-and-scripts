#!/usr/bin/env python
#
# Released under CC0 by Jamey Sharp <jamey@minilop.net>
#
# The person who associated a work with this deed has dedicated the work to the
# public domain by waiving all of his or her rights to the work worldwide under
# copyright law, including all related and neighboring rights, to the extent
# allowed by law.
#
# You can copy, modify, distribute and perform the work, even for commercial
# purposes, all without asking permission. See Other Information below.
#
# A copy of the CC0 legalcode can be found at
# http://creativecommons.org/publicdomain/zero/1.0/

import codecs
import json
from pandocfilters import walk, Link
import sys

def extract_contents(blocks):
    for block in blocks:
        if block["t"] == "Div":
            if block["c"][0][0] == "content":
                for child in block["c"][1]:
                    yield child
            else:
                for result in extract_contents(block["c"][1]):
                    yield result

def remove_moin(key, value, format, meta):
    if key == "Span" and "anchor" in value[0][1]:
        return []
    if key == "Div" and "table-of-contents" in value[0][1]:
        return []
    if key == "Link":
        if "nonexistent" in value[0][1]:
            return value[1]
        value[0][1] = [c for c in value[0][1] if c not in ("http", "https")]
        return {"t": key, "c": value}

if __name__ == "__main__":
    doc = json.load(codecs.getreader("utf-8")(sys.stdin))
    doc["blocks"] = list(extract_contents(doc["blocks"]))
    doc = walk(doc, remove_moin, "", {})
    json.dump(doc, codecs.getwriter("utf-8")(sys.stdout))
