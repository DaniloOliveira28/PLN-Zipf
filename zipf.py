from collections import defaultdict
from nltk.corpus import genesis
from unidecode import unidecode
import numpy as np
import matplotlib.pyplot as plt
import string

def powerLaw(y, x):
    """
    'When the frequency of an event varies as power of some attribute of that
    event the frequency is said to follow a power law.' (wikipedia)
    This is represented by the following equation, where c and alpha are
    constants:
    y = c . x ^ alpha
    Args
    --------
    y: array with frequency of events >0
    x: numpy array with attribute of events >0
    Output
    --------
    (c, alpha)
    c: the maximum frequency of any event
    alpha: defined by (Newman, 2005 for details):
        alpha = 1 + n * sum(ln( xi / xmin )) ^ -1
    """
    c = 0
    alpha = .0

    if len(y) and len(y) == len(x):
        c = max(y)
        xmin = float(min(x))
        alpha = 1 + len(x) * pow(sum(np.log(x/xmin)), -1)

    return (c, alpha)


def plotPowerLaws(y, x, c=[], alpha=[]):
    """
    Plots the relationship between x and y and a fitted power law on LogLog
    scale.
    Args
    --------
    y: array with frequency of events >0
    x: array with attribute of events >0
    c: array of cs for various power laws
    alpha: array of alphas for various power laws
    """
    plt.figure()
    plt.loglog()
    plt.plot(x,
             y,
             'r+')
    for _c, _alpha in zip(c, alpha):
        plt.plot((1, max(x)), (_c, _c * pow(max(x), _alpha)),
                 label='~x^%.2f' % _alpha)
        plt.legend()
    plt.show()



"""
Checking Zipfs law, where the frequency and rank of a word follow a
specific power law, using the article generated by article generator.
"""

articleFile = open("./artigo.txt", "r")
print "OK"
article = articleFile.read()
print article

## remove pontuations..
replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
article = article.translate(replace_punctuation)

## remove numbers..
article = ''.join([i for i in article if not i.isdigit()])

## remove \n
article = " ".join(article.split("\n"))

# put in lower case
article = article.lower()

# remove accents
article = unidecode(article)

# remove references
article = article.split('references')[0]

print article
words = article.split(' ')

# remove empty strings
words = filter(None, words)
print words
y = defaultdict(int)
for i in words:
    y[i] += 1
y = sorted(y.values(), reverse=True)
x = np.array(xrange(1, len(y)+1))

c, alpha = powerLaw(y, x)
print 'According to Zipfs law %.2f should be close to 1.' % alpha
plotPowerLaws(y, x, [c, c], [-1, -alpha])
