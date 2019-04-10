#!/usr/bin/env python

import sys
import json
from collections import defaultdict
from datetime import datetime, timedelta
import pandas as pd

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
    return data, tunes


def tunes_stats(tunes, start='1970-01-01'):
    freqs = defaultdict(list)
    for tune in tunes.values():
        nbtimes = len([r for r in tune['rehearsals'] if r >= start])
        freqs[nbtimes].append(tune['name'])
    for freq in sorted(freqs.keys(), reverse=True):
        print('{}:'.format(freq))
        for name in sorted(freqs[freq]):
            print('    - {}'.format(name))
    print()

def rehearsals_stats(rehearsals):
    session_nbs = [ (r['date'], len(r['tunes'])) for r in rehearsals ]
    df = pd.DataFrame.from_records(session_nbs, columns=('date', 'nbtunes'))
    print('Min tunes: {}, max: {}, mean: {}'.format(df['nbtunes'].min(),
                                              df['nbtunes'].max(),
                                              df['nbtunes'].mean()))


def main(json_path):
    data, tunes = load(json_path)
    monthago = (datetime.now() - timedelta(days=28))\
                                     .strftime('%Y-%m-%d')
    print('Monthly stats (after {}):'.format(monthago))
    print('--------------')
    tunes_stats(tunes, monthago)
    print('All-time stats:')
    print('---------------')
    tunes_stats(tunes)

    print('Rehearsal stats:')
    print('----------------')
    rehearsals_stats(data['rehearsals'])

    print('Last rehearsal:')
    print('---------------')
    print('{}'.format(', '.join(data['rehearsals'][-1]['tunes'])))
    
    print('All tunes:')
    print('----------')
    for t in sorted(tunes.keys()):
        print('- {}'.format(t))
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        usage()


