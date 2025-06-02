s = input()
freq = {}

for c in s:
    if c != " " and c not in freq:
        freq[c] = s.count(c)

for c in freq:
    print(f"{c}={freq[c]}")