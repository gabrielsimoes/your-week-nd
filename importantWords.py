#!/usr/bin/env python3
import sys
import pandas as pd
import string

stop_words = [line[:-1] for line in open("stopwords.txt", "r")]
raw = pd.read_csv(sys.argv[1])
events = raw.to_dict("list")

test = []
for e in events: 
    description = [w for w in events[e][0].split() if not w in stop_words if not w in string.punctuation]
    events[e][0] = ' '.join(str(w) for w in description)

out = pd.DataFrame.from_dict(events)
out.to_csv('improved_events.csv', index = False)
