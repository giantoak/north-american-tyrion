import logging
from bs4 import BeautifulSoup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig()


def extract_classes_ids(soup):
    ''' Return CSS classes and ids from a beautifulsoup object '''
    ids = set()
    classes = set()

    for tag in soup():
        try:
            i = tag['id']
            ids.add(i)
        except KeyError:
            pass

        try:
            cs = tag['class']
            for c in cs:
                classes.add(c)
        except KeyError:
            pass

    return classes, ids


def jaccard(set1, set2):
    return len(set1.intersection(set2)) / (1 + float(len(set1.union(set2))))


def css_jaccard(source1, source2):
    logger.debug('css_jaccard')
    score = 0

    s1 = BeautifulSoup(source1)
    s2 = BeautifulSoup(source2)

    c1, i1 = extract_classes_ids(s1)
    c2, i2 = extract_classes_ids(s2)

    logger.debug('i1: {}, c1: {}, i2: {}, c2: {}'.format(len(i1),
        len(c1), len(i2), len(c2)))
    jaccard_ids = jaccard(i1, i2)
    logger.debug('Ids: {}'.format(jaccard_ids))

    jaccard_classes = jaccard(c1, c2)
    logger.debug('Classes: {}'.format(jaccard_classes))
    return score


class ClassJaccarder(object):
    def __init__(self, source):
        self.soup = BeautifulSoup(source)
        self.classes, self.ids = extract_classes_ids(self.soup)


    def compare(self, other_source):
        other_soup = BeautifulSoup(other_source)
        other_classes, other_ids = extract_classes_ids(other_soup)

        j_c = jaccard(self.classes, other_classes)
        j_i = jaccard(self.ids, other_ids)

        return j_c, j_i
