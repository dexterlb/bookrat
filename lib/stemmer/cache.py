from collections import deque

class _Miss:
    pass

class BulkCall:
    '''BulkCall is constructed using ``pipe_func`` which transforms
    a list of items all at once. Then, when called with an iterator,
    the BulkCall object will call ``pipe_func`` each time it accumulates
    ``at_once`` number of items, and yield the results from the call.

    The ``cache`` can be any dict-like object. Results from all calls to
    ``pipe_func`` are cached in it, and when an item appears a second
    time in the input iterator, the result is retreived from the cache
    instead of being passed to ``pipe_func``. Hence, if using a cache,
    it is assumed that ``pipe_func`` is pure.

    Any words in stop_words are skipped (and replaced by None)
    '''

    def __init__(self, pipe_func, at_once=1000, cache=None, stop_words=set()):
        self.pipe_func = pipe_func
        self.cache = cache
        self.at_once = at_once
        self.stop_words = stop_words

    def __call__(self, iterator):
        iterator = iter(iterator)
        hits = deque()
        misses = deque()

        while True:
            try:
                item = next(iterator)
                if item in self.stop_words:
                    hits.appendleft(None)
                elif self.cache and item in self.cache:
                    hits.appendleft(self.cache[item])
                else:
                    hits.appendleft(_Miss)
                    misses.appendleft(item)

            except StopIteration:
                if not hits:
                    return
                item = None

            if len(misses) >= self.at_once or not item:
                results = list(self.pipe_func(misses))
                while hits:
                    result = hits.pop()

                    if result is not _Miss:
                        yield result
                    else:
                        result = results.pop()
                        item = misses.pop()
                        if self.cache is not None:
                            self.cache[item] = result
                        yield result

class LimitedCache:
    def __init__(self, limit=200000):
        self.a = {}
        self.b = {}
        self.dict_limit = limit // 2

    def __contains__(self, item):
        return item in self.a or item in self.b

    def __getitem__(self, key):
        if key in self.a:
            return self.a[key]
        return self.b[key]

    def __setitem__(self, key, value):
        if len(self.a) >= self.dict_limit:
            self.b = self.a
            self.a = {}

        self.a[key] = value

    def __len__(self):
        return len(self.a) + len(self.b)

    def __dict__(self):
        full_cache = self.a.copy()
        full_cache.update(self.b)
        return full_cache
