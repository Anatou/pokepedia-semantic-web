N_PARTS = 3

permutations = {
    "-C2-A0": " ",
    "-C3-80": "À",
    "-C3-81": "Á",
    "-C3-82": "Â",
    "-C3-83": "Ã",
    "-C3-84": "Ä",
    "-C3-87": "Ç",
    "-C3-88": "È",
    "-C3-89": "É",
    "-C3-8A": "Ê",
    "-C3-8B": "Ë",
    "-C3-8E": "Î",
    "-C3-8F": "Ï",
    "-C3-94": "Ô",
    "-C3-99": "Ù",
    "-C3-A0": "à",
    "-C3-A2": "â",
    "-C3-A7": "ç",
    "-C3-A8": "è",
    "-C3-A9": "é",
    "-C3-AA": "ê",
    "-C3-AB": "ë",
    "-C3-AE": "î",
    "-C3-AF": "ï",
    "-C3-B3": "ó",
    "-C3-B4": "ô",
    "-C3-B9": "ù",
    "-C3-BB": "û",
}

for part in range(N_PARTS):
    corrected_data = []
    with open(f"pokepedia-fr_rdfdump20150715-part{part+1}.rdf", "r") as file:
        lines = file.readlines()
        for line in lines:
            for word, permut in permutations.items():
                line = line.replace(word, permut)
            corrected_data.append(line)


    with open(f"pokepedia-fr_rdfdump20150715-part{part+1}-corrected.rdf", "w") as file:
        file.writelines(corrected_data)