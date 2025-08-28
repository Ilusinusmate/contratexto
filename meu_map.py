def meu_map(func, seq):
    for item in seq:
        yield func(item)


print(meu_map(int, ["1", "2", "3"]))
print(tuple(meu_map(int, ["1", "2", "3"])))

