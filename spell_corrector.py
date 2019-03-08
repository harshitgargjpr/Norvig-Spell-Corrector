from collections import Counter
import re

def words(text):
    return re.findall(r'\w+', text.lower())

Counts = Counter(words(open('big.txt').read()))

def Probability(word):
    N = sum(Counts.values())
    return Counts[word]/N

def correction(word):
    return max(chances(word), key = Probability)

def chances(word):
    return (known_words([word]) or known_words(one_correction(word)) or known_words(two_correction(word)) or [word])

def known_words(words):
    return [word for word in words if word in Counts]

def one_correction(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word)+1)]

    Replace = [L + letter + R[1:]  for L, R in splits if R for letter in alphabet]
    Delete = [L + R[1:]  for L, R in splits if R]
    Insert = [L + letter + R  for L, R in splits for letter in alphabet]
    Swap = [L + R[1] + R[0] + R[2:]  for L, R in splits if len(R)>1]

    return set(Replace + Delete + Insert + Swap)

def two_correction(word):
    return set([corr2 for corr1 in one_correction(word) for corr2 in one_correction(corr1)])

def unit_tests():
    assert correction('speling') == 'spelling'              # insert
    assert correction('korrectud') == 'corrected'           # replace 2
    assert correction('bycycle') == 'bicycle'               # replace
    assert correction('inconvient') == 'inconvenient'       # insert 2
    assert correction('arrainged') == 'arranged'            # delete
    assert correction('peotry') =='poetry'                  # transpose
    assert correction('peotryy') =='poetry'                 # transpose + delete
    assert correction('word') == 'word'                     # known
    assert correction('quintessential') == 'quintessential' # unknown
    assert words('This is a TEST.') == ['this', 'is', 'a', 'test']
    assert Counter(words('This is a test. 123; A TEST this is.')) == (
           Counter({'123': 1, 'a': 2, 'is': 2, 'test': 2, 'this': 2}))
    assert Probability('quintessential') == 0
    assert 0.07 < Probability('the') < 0.08
    return 'unit_tests pass'

def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.clock()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in Counts)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, Counts[w], right, Counts[right]))
    dt = time.clock() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))

def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

print(unit_tests())
spelltest(Testset(open('spell-testset1.txt'))) # Development set
spelltest(Testset(open('spell-testset2.txt'))) # Final test set
