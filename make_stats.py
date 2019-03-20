#!/usr/bin/env python

import sys
import json
from collections import defaultdict
from datetime import datetime, timedelta

def usage():
    print("{} <json file>".format(sys.argv[0]))


def load(path):
    tunes = {}
    with open(path, 'r') as dataf:
        data = json.load(dataf)
        for tune in data['tunes']:
            tune['rehearsals'] = set()
            tunes[tune['name']] = tune
        for rehearsal in data['rehearsals']:
            for name in rehearsal['tunes']:
                tunes[name]['rehearsals'].add(rehearsal['date'])
    return tunes
        

def stats(tunes, start='1970-01-01'):

    freqs = defaultdict(list)
    for tune in tunes.values():
        nbtimes = len([r for r in tune['rehearsals'] if r >= start])
        freqs[nbtimes].append(tune['name'])
    for freq in sorted(freqs.keys(), reverse=True):
        print('{}:'.format(freq))
        for name in sorted(freqs[freq]):
            print('    - {}'.format(name))
    print()

    
def main(json_path):
    tunes = load(json_path)
    print('Monthly stats:')
    print('--------------')
    monthago = (datetime.now() - timedelta(days=35))\
                                     .strftime('%Y-%m-%d')
    stats(tunes, monthago)
    print('All-time stats:')
    print('---------------')
    stats(tunes)

        
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        usage()

    
