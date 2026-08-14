from app.retrieval import retrieve_facts


results = retrieve_facts(
    "What is Sathish's favorite programming language?"
)

for result in results:
    print(result)