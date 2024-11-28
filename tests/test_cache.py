from __future__ import annotations, unicode_literals

import pytest

from textual.cache import FIFOCache, LRUCache


def test_discard():
    cache = LRUCache(maxsize=3)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")

    assert len(cache) == 3
    assert cache.get("key1") == "value1"

    cache.discard("key1")

    assert len(cache) == 2
    assert cache.get("key1") is None

    cache.discard("key4")  # key that does not exist

    assert len(cache) == 2  # size should not change


def test_discard_regression():
    """Regression test for https://github.com/Textualize/textual/issues/3537"""

    cache = LRUCache(maxsize=3)
    cache[1] = "foo"
    cache[2] = "bar"
    cache[3] = "baz"
    cache[4] = "egg"

    assert cache.keys() == {2, 3, 4}

    cache.discard(2)
    assert cache.keys() == {3, 4}

    cache[5] = "bob"
    assert cache.keys() == {3, 4, 5}

    cache.discard(5)
    assert cache.keys() == {3, 4}

    cache.discard(4)
    cache.discard(3)

    assert cache.keys() == set()
