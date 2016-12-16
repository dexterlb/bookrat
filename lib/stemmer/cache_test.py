import unittest
from collections import defaultdict
import cache

class TestBulkCall(unittest.TestCase):
    def test_doesnt_break_iterator(self):
        def f(x):
            return x * x

        lambdamapf = lambda l: map(f, l)

        self.assertEqual(
            list(cache.BulkCall(lambdamapf)([1, 2, 3])),
            [1, 4, 9]
        )

    def test_doesnt_call_function_second_time(self):
        calls = defaultdict(int)

        def f(x):
            calls[x] += 1
            return x * x

        lambdamapf = lambda l: map(f, l)

        self.assertEqual(
            list(cache.BulkCall(lambdamapf, 1, {})([1, 2, 3, 3])),
            [1, 4, 9, 9]
        )

        self.assertEqual(dict(calls), {1: 1, 2: 1, 3: 1})

class TestLimitedCache(unittest.TestCase):
    def test_stores_keys(self):
        c = cache.LimitedCache(2)
        c['foo'] = 'bar'
        c['baz'] = 'qux'

        self.assertTrue('foo' in c)
        self.assertTrue('baz' in c)

    def test_stores_values(self):
        c = cache.LimitedCache(2)
        c['foo'] = 'bar'
        c['baz'] = 'qux'

        self.assertEqual(c['foo'], 'bar')
        self.assertEqual(c['baz'], 'qux')

    def test_removes_old_values(self):
        c = cache.LimitedCache(2)
        c['foo'] = 'bar'
        c['baz'] = 'qux'
        c['quux'] = 'waldo'

        self.assertTrue(len(c) <= 2)

    def test_retains_new_values(self):
        c = cache.LimitedCache(2)
        c['foo'] = 'bar'
        c['baz'] = 'qux'
        c['quux'] = 'waldo'

        self.assertEqual(c['quux'], 'waldo')


if __name__ == '__main__':
    unittest.main()
