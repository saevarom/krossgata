# -*- coding: utf-8 -*-
import re
import time
import logging


def timing(func):
    def inside(*args):
        t1 = time.time()
        res = func(*args)
        t2 = time.time()
        logging.info( '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0) )
        return res
    return inside

def to_unicode_or_bust(
    obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj

def read_file(filename):
    f = open(filename)
    return [to_unicode_or_bust(l.strip()) for l in list(f)]

words = read_file('wordlist.txt')

def permutations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in permutations(items[:i]+items[i+1:],n-1):
                yield [items[i]]+cc

def all_perms(str):
    if len(str) <=1:
        yield str
    else:
        for perm in all_perms(str[1:]):
            for i in range(len(perm)+1):
                yield perm[:i] + str[0:1] + perm[i:]

def regex_search(regex):
    rmatched = []
    errors = []
    for word in words:
        m = re.match(regex, word)
        if m:
            rmatched.append(m.group(0))
    return {'matches':rmatched,'errors':errors}

@timing
def perm_search(string):
    pmatched = []
    errors = []
    if len(string) > 6:
        errors.append(u"Af tæknilegum ástæðum er ekki hægt að finna stafarugl sem er lengra en 6 stafir.")
    else:
        #perms = list(set([u''.join(p) for p in permutations(list(string), len(string))]))
        perms = list(set(list(all_perms(to_unicode_or_bust(string)))))

        for word in words:
            for p in perms:
                if p == word:
                    pmatched.append(word)

    return {'matches':pmatched,'errors':errors}

