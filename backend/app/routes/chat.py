from fastapi import APIRouter

from app.schemas import ChatRequest, ChatResponse
from app.retrieval import retrieve_facts
from app.access_control import check_access
from app.llm import generate_response


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    print(request.question)
    print("Chat route called ")

    # 1. Retrieve relevant facts
    results = retrieve_facts(request.question , top_k=5)
    print(results)
    if not results:
        return ChatResponse(
            answer="I don't have enough information to answer that.",
            requires_password=False
        )

    # 2. Check the most relevant fact first
    top_result = results[0]
  
    print("meta data ",top_result)
    top_metadata = top_result["metadata"]
    # print("type checking" , type(top_metadata))
    # 3. If the most relevant fact is private,
    #    authentication is required before revealing anything.
    if top_metadata.get("access") == "private":
  
        if not check_access(top_metadata, request.password):
            return ChatResponse(
                answer="This information is private. Please provide the required password.",
                requires_password=True
            )

    # 4. Build authorized context
    authorized_facts = []

    for result in results:

        metadata = result["metadata"]

        if metadata.get("access") == "public":
            authorized_facts.append(result["text"])

        elif metadata.get("access") == "private":

            if check_access(metadata, request.password):
                authorized_facts.append(result["text"])

    # 5. Nothing authorized
    if not authorized_facts:
        return ChatResponse(
            answer="I don't have enough information to answer that.",
            requires_password=False
        )

    # 6. Send ONLY authorized facts to Gemini
    context = "\n".join(
        f"- {fact}" for fact in authorized_facts
    )

    prompt = f"""
    
You are a chatbot that answers questions about Sathish.

Answer the user's question using ONLY the information provided
in the context below.

Do not invent information.

Context:
{context}

User question:
{request.question}
"""

    # 7. Generate answer
    answer = generate_response(prompt)
    print("Generated answer:", answer)
    return ChatResponse(
        answer=answer,
        requires_password=False
    )