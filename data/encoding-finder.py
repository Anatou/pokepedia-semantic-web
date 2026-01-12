import re

N_PARTS = 3

encoding = set()

for part in range(N_PARTS):
    corrected_data = []
    with open(f"pokepedia-fr_rdfdump20150715-part{part+1}.rdf", "r") as file:
        lines = file.read()
        res = re.findall(r"-C3-.{2,2}", lines)
        encoding = encoding.union(set(res))

print("Special chars are:")
for char in encoding:
    print(char)