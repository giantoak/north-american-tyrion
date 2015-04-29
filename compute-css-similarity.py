import sys
import argparse
from simscores import css_jaccard
import logging

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser(prog='Compute Jaccard similarities between\
the CSS classes and ids between two HTML documents')

parser.add_argument('file1', help='Path to file that contains HTML source')
parser.add_argument('file2', help='Path to file that contains HTML source')

args = parser.parse_args()

with open(args.file1) as f1, open(args.file2) as f2:
    src1 = f1.read()
    src2 = f2.read()

    similarity = css_jaccard(src1, src2)
