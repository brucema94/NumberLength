#! /usr/bin/env python3

# dictionary that knows how many syllables are in certain numbers
# all number smaller than or equal to 20 are in here (important for base case)
import itertools as it

LENGTH_DICT = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 2, 8: 1, 9: 2, 10: 1,
               11: 1, 12: 1, 13: 2, 14: 2, 15: 2, 16: 2, 17: 3, 18: 2, 19: 3,
               20: 2, 100: 2, 1000: 2,
               10 ** 6: 2,   # miljoen
               10 ** 9: 2,   # miljard
               10 ** 12: 2,  # biljoen
               10 ** 15: 2,  # biljard
               10 ** 15: 2,  # triljoen
               10 ** 18: 2,  # triljard
               }
BASE_CASE_CAP = 20
BASE_CASE = [LENGTH_DICT[i + 1] for i in range(BASE_CASE_CAP)]


class Counter(object):
    def __init__(self):
        self.cache = {}

    def get_cache(self, value: int):
        if value not in self.cache:
            # save tuple to make sure we don't accidentally edit the cache
            self.cache[value] = tuple(self.get_lengths(value))
        return self.cache[value]

    def get_lengths(self, cap: int):
        """
        Calculate how many syllables are needed to pronounce a number
        """
        if cap <= BASE_CASE_CAP:
            return BASE_CASE[:cap]  # always returns a copy, which is safe

        increment = 10
        prev_cap = 10
        super_cap = prev_cap * increment
        if cap < super_cap:
            # 20 < cap < 100: (approx) <last digit> en <first digit>ig
            # which means `len(last) + len(first) + 2`.
            # However, every 10th is only <first digit>ig
            nine = self.get_cache(increment - 1)
            # ignore first twenty (`nine[1:]`)
            # compensate for the `+2` that should be `+1` at every tenth:
            #   (`+ [-1]`)
            # Note that I'm assuming that `isinstance(nine, tuple)`
            prod = it.product(nine[1:], nine + (-1,))
            res = map(lambda p: sum(p) + 2, prod)
            # PS. the last value is never used, even though it is
            # (coincidentally) correct:
            #   len(['tien', 'tig']) == len(['hon', 'derd'])
            return it.chain(
                BASE_CASE,
                it.islice(res, cap - BASE_CASE_CAP)
            )

        super_cap, prev_cap = super_cap * increment, super_cap
        if cap < super_cap:
            # 100 <= cap < 1000: <first digit> honderd <last two digits>
            nine = self.get_cache(increment - 1)
            # In Dutch we don't say "one-hundred", but "honderd".
            nine = (0,) + nine[1:]
            ninety_nine = self.get_cache(prev_cap - 1)

            # Neither do we say "hundred-zero"
            prod = it.product(nine, it.chain([0], ninety_nine))
            return it.islice(
                it.chain(
                    ninety_nine,
                    map(lambda p: sum(p) + LENGTH_DICT[prev_cap], prod)
                ),
                cap
            )

        increment = 1000
        while prev_cap in LENGTH_DICT and cap >= super_cap:
            super_cap, prev_cap = super_cap * increment, super_cap

        if cap < super_cap:
            incr = self.get_cache(increment - 1)
            prev = self.get_cache(prev_cap - 1)
            # In Dutch we _do_ say "één(m|b|tr)ilj(oen|ard)",
            # but we don't say "one-thousand", but "duizend".
            if prev_cap == 1000:
                incr = it.chain([0], incr[1:])
            # Neither do we say "(één(m|b|tr)ilj(oen|ard)|duizend)nul"
            prod = it.product(incr, it.chain([0], prev))
            return it.islice(
                it.chain(
                    prev,
                    map(lambda p: sum(p) + LENGTH_DICT[prev_cap], prod)
                ),
                cap
            )
        raise ValueError("I didn't feel like implementing numbers this size.")


if __name__ == '__main__':
    # compute the time in years required to pronounce all numbers up to
    # 1 billion
    cap = 10 ** 9 - 1
    lengths = Counter().get_lengths(cap)
    # assert len(lengths) == cap, "len: {}, cap: {}".format(len(lengths), cap)
    # skip = 1000
    # for i in range(0, cap, skip):
    #     print(lengths[i: i + skip])
    # print(len(list(get_lengths(99))))
    print("Finished creating iterator")
    # assuming 5 syllables per second
    print((sum(lengths) + LENGTH_DICT[cap + 1]) / 5.0 / 3600.0 / 24.0 / 365.0)
