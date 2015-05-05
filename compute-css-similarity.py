import sys
import argparse
from simscores import ClassJaccarder, extract_classes_ids, jaccard
import logging
import os
from collections import defaultdict
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

def load_all_files(directory):
    logger.debug('load_all_files: {}'.format(directory))

    extractions = {}
    walker = os.walk(directory)
    i = 0
    for w in walker:
        for x in w[2]:
            if not x.endswith('.html'):
                continue

            else:
                fn = os.path.join(w[0], x)

                with open(fn) as f:
                    src = f.read()
                    soup = BeautifulSoup(src)
                    extractions[x] = extract_classes_ids(soup)

                if i % 100 == 0:
                    logger.debug('{}: {}'.format(i, fn))

                i += 1

    return extractions

def compare_all(extractions):
    keys = extractions.keys()
    results = open('simscores.csv', 'w')
    for i in range(len(keys)):
        for j in range(i+1, len(keys)):
            fn_i = keys[i]
            fn_j = keys[j]

            classes_i, ids_i = extractions[fn_i]
            classes_j, ids_j = extractions[fn_j]

            j_c = jaccard(classes_i, classes_j)
            j_i = jaccard(ids_i, ids_j)

            results.write('{},{},{},{}\n'.format(fn_i, fn_j, j_c, j_i))

def compare_files(args):
    with open(args.files[1]) as f1, open(args.files[1]) as f2:
        src1 = f1.read()
        src2 = f2.read()

        cj = ClassJaccarder(src1)
        similarity = cj.compare(src2)

        logger.debug(similarity)

parser = argparse.ArgumentParser(prog='Compute Jaccard similarities between\
the CSS classes and ids between two HTML documents')

parser.add_argument('--files', '-f', nargs=2,
                   help='Path to 2 files that contains HTML source')

parser.add_argument('--directory', '-d', nargs=1,
                    help='Directory to recursively parse for files, and to \
                          compute pairwise similarities between.')
args = parser.parse_args()

if args.files:
    compare_files(args)
elif args.directory:
    extractions = load_all_files(args.directory[0])
    compare_all(extractions)
