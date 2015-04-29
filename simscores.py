import logging
from bs4 import BeautifulSoup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig()

def _extract_classes_ids(soup):
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

    from pprint import pformat
    return ids, classes

def css_jaccard(source1, source2):
    logger.debug('css_jaccard')
    score = 0

    s1 = BeautifulSoup(source1)
    s2 = BeautifulSoup(source2)

    i1, c1 = _extract_classes_ids(s1)
    i2, c2 = _extract_classes_ids(s2)

    logger.debug('i1: {}, c1: {}, i2: {}, c2: {}'.format(len(i1),
        len(c1), len(i2), len(c2)))
    jaccard_ids = len(i1.intersection(i2)) / float(len(i1.union(i2)))
    logger.debug('Ids: {}'.format(jaccard_ids))

    jaccard_classes = len(c1.intersection(c2)) / float(len(c1.union(c2)))
    logger.debug('Classes: {}'.format(jaccard_classes))

    return jaccard_ids, jaccard_classes
