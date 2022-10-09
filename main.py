# This is a sample Python script.
# This implementation is based on https://jellis18.github.io/post/2021-11-25-lru-cache/

from typing import TypeVar, Generic, Hashable, NamedTuple
from collections import OrderedDict

T = TypeVar("T")


class LruCache(Generic[T]):
    def __init__(self, capacity: int = 0):
        self.capacity = capacity
        self.__cache: OrderedDict[Hashable, T] = OrderedDict()

    def get(self, key):
        # return the value from internal cache
        # move the key to the bottom
        val = self.__cache.get(key, None)
        if val:
            self.__cache.move_to_end(key)
        return val

    def insert(self, key: Hashable, value: T):
        if len(self.__cache) == self.capacity:
            self.__cache.popitem(last=False)
        self.__cache[key] = value
        self.__cache.move_to_end(key)

    def __len__(self):
        return len(self.__cache)

    def clear(self):
        self.__cache.clear()

    def __str__(self):
        return " ".join([str(key) for key in self.__cache])


class CacheInfo(NamedTuple):
    hits: int
    miss: int
    maxsize: int
    currsize: int


class __LruCacheFunctionWrapper:

    def __init__(self, func, max_size):
        self.wrapped = func
        self.__cache = LruCache(max_size)
        self.__hits = 0
        self.__misses = 0
        self.__maxsize = max_size

    def __call__(self, *args, **kwargs):
        call_args = args + tuple(kwargs.items())
        ret = self.__cache.get(call_args)

        if ret is None:
            self.__misses += 1
            ret = self.wrapped(*args, **kwargs)
            self.__cache.insert(call_args, ret)
        else:
            self.__hits += 1

        return ret

    def cache_info(self):
        return CacheInfo(hits=self.__hits, miss=self.__misses,
                         maxsize=self.__maxsize, currsize=len(self.__cache))

    def cache_clear(self):
        self.__cache.clear()
        self.__hits = 0
        self.__misses = 0


def lru_cache(max_size: int):
    def wrapped(func):
        return __LruCacheFunctionWrapper(func, max_size)

    return wrapped


@lru_cache(100)
def fib(num):
    if num <= 1:
        return num
    return fib(num - 1) + fib(num - 2)


def main():
    lst = [fib(i) for i in range(16)]
    print(fib.cache_info())


if __name__ == '__main__':
    main()
