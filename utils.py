from google.appengine.api import memcache
import time
import logging
import pickle

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


def store(key, value, chunksize=950000):
    serialized = pickle.dumps(value, 2)
    values = {}
    for i in xrange(0, len(serialized), chunksize):
        values['%s.%s' % (key, i//chunksize)] = serialized[i : i+chunksize]
    memcache.set_multi(values)

def retrieve(key):
    result = memcache.get_multi(['%s.%s' % (key, i) for i in xrange(32)])
    logging.debug(result)
    serialized = ''.join([v for k, v in sorted(result.items()) if v is not None])
    if serialized == '':
        return None
    return pickle.loads(serialized)

