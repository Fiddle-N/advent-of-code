freq_changes = []

with open("input.txt", "r") as f:
    for freq in f:
        freq_changes.append(int(freq))

print(sum(freq_changes))
