from app.retrieval import retrieve_facts


results = retrieve_facts(
    "who is sathish crush?"
)

for result in results:
    print(result)