from __future__ import print_function
import pandas as pd
import numpy as np
# import locale
import glob
import sys
import os
import requests
import tarfile

"Load and pre-format reviews"
# locale.setlocale(locale.LC_ALL, 'C')

# Convert text to lower-case and strip punctuation/symbols from words
def normalize_text(text):
    norm_text = text.lower()

    # Replace breaks with spaces
    norm_text = norm_text.replace('<br />', ' ')

    # Pad punctuation with spaces on both sides
    for char in ['.', '"', ',', '(', ')', '!', '?', ';', ':']:
        norm_text = norm_text.replace(char, ' ' + char + ' ')

    return norm_text


def collect_reviews(datadirname = "../data/"):
    filename = 'aclImdb_v1.tar.gz'
    filepath = os.path.join(datadirname, filename)
    dirname = filepath.replace("_v1.tar.gz", "")
    if not os.path.isdir(datadirname):
        os.makedirs(datadirname)
    if not os.path.isdir(dirname):
        if not os.path.isfile(filepath):
            print("file 'alldata-id.txt' not found; downloading")
            # Download IMDB archive
            url = 'http://ai.stanford.edu/~amaas/data/sentiment/' + filename
            r = requests.get(url)
            with open(filepath, 'wb') as f:
                f.write(r.content)
        print("directory '%s' not found; extracting" % dirname)
        tar = tarfile.open(filepath, mode='r')
        tar.extractall(path=datadirname)
        tar.close()

    # Concat and normalize test/train data
    folders = ['train/pos', 'train/neg', 'test/pos', 'test/neg', 'train/unsup']
    #     alldata = u''
    alldata = []

    for fol in folders:
        print(fol, file = sys.stderr)
        temp = u''
        output = fol.replace('/', '-') + '.txt'

        # Is there a better pattern to use?
        txt_files = glob.glob('/'.join([dirname, fol, '*.txt']))

        for txtfi in txt_files:
            with open(txtfi, 'r') as t:
                control_chars = [chr(0x85)]
                t_clean = t.read()

                for c in control_chars:
                    t_clean = t_clean.replace(c, ' ')

            id_, stars_ = os.path.basename(txtfi).replace(".txt", "").split("_")

            dset, judgement = fol.split("/")
            alldata.append( 
                (dset, judgement, id_, stars_, normalize_text(t_clean) )
                )
    return alldata
