
#1. generate type advantages triplets
from add_types_tuples_query_builder import generate_types_triplets
generate_types_triplets()


#2. add them to the graph
with open("rdf/pokepedia-fr_rdfdump20150715.rdf", "r", encoding="utf-8") as source:
    graph_string = source.read()

#remove end of file mark
graph_string = graph_string[0 : len(graph_string) - len("</rdf:RDF>")]

#add type triplets
with open("rdf/types_triplets.txt", "r", encoding="utf-8") as triplets:
    triplets_string = triplets.read()
graph_string += triplets_string
del triplets_string

#add end of file mark
graph_string += "</rdf:RDF>"


#3. replace string type properties by corresponding URIs
graph_string = graph_string.replace("""property:Premier_type rdf:datatype="http://www.w3.org/2001/XMLSchema#string">""", """property:Premier_type rdf:resource="&wiki;""")
graph_string = graph_string.replace("""</property:Premier_type>""", """"/>""")
graph_string = graph_string.replace("""property:Second_type rdf:datatype="http://www.w3.org/2001/XMLSchema#string">""", """property:Second_type rdf:resource="&wiki;""")
graph_string = graph_string.replace("""</property:Second_type>""", """"/>""")


# save graph
with open("rdf/modified_graph.rdf", "w", encoding="utf-8") as output:
    output.write(graph_string)