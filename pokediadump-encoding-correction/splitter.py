N_PARTS = 3
data = [[] for _ in range(N_PARTS)]

with open("pokepedia-fr_rdfdump20150715.rdf", "r") as file:
    lines = file.readlines()
    sep = len(lines)/N_PARTS
    for i, line in enumerate(lines):
        for part in range(N_PARTS):
            if i < sep*(part+1):
                data[part].append(line)
                break

for part in range(N_PARTS):
    with open(f"pokepedia-fr_rdfdump20150715-part{part+1}.rdf", "w") as file:
        file.writelines(data[part])