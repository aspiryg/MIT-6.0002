# From codereview.stackexchange.com
def partitions(set_):
    if not set_:
        yield []
        return
    for i in range(2**len(set_)//2):  # skip duplicates How?
        parts = [set(), set()]
        for item in set_:
            parts[i & 1].add(item)
            i >>= 1
        for b in partitions(parts[1]):
            yield [parts[0]]+b


def get_partitions(set_):
    for partition in partitions(set_):
        yield [list(elt) for elt in partition]


# For example, the call get_partitions([1,2,3]) would yield the following:

# set_ = [1, 2, 3]
# for partition in get_partitions(set_):
#     print(partition)
