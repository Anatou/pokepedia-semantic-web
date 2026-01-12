import json

with open("rdf/weaknesses.json", "r", encoding="utf-8") as f:
    weaknesses = json.load(f)

with open("rdf/add_types_tuples.txt", "w", encoding="utf-8") as output:
    for advantaged_type, types in weaknesses.items():
        output.write(f"""    <swivt:Subject rdf:about="wiki:{advantaged_type}">\n""")
        output.write(f"""        <rdf:type rdf:resource="&wiki;Type"/>\n""")
        for type, multiplicator in types.items():
            if multiplicator == 2:
                output.write(f"""        <wiki:force rdf:resource="&wiki;{type}"/>\n""")    #question de vocabulaire
                output.write(f"""        <wiki:avantage rdf:resource="&wiki;{type}"/>\n""")
        output.write(f"""    </swivt:Subject>\n""")