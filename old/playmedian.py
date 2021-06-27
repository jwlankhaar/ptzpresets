import statistics
import timeit


def median_without_sort(lst):
    data = lst[:]
    n = len(data)
    upper = n // 2 + n % 2
    for _ in range(0, upper):
        p = None
        i = 0
        for i, k in enumerate(data):
            if not p:
                p = k
                i_min = i
            elif k < p:
                q = p
                p = k
                i_min = i
        data.pop(i_min)
    if n % 2:
        return p
    else:
        return (p + q) / 2 


def test(median_func):
    lists = [
        [6, 3, 9, 2, 5],
        [6, 3, 9, 2, 5, 4],
        [6, 3, 3, 9, 2, 5, 5, 5, 4]
    ]
    for lst in lists:
        median_func(lst)

    # for lst in lists:
    #     print(lst)
    #     print(f'sorted: {sorted(lst)}')
    #     print(f'{median_without_sort(lst)=}, {statistics.median(lst)=}\n')

print(timeit.timeit('test(median_without_sort)', setup='from __main__ import median_without_sort, test', number=1000))
print(timeit.timeit('test(median)', setup='from statistics import median; from __main__ import test', number=1000))