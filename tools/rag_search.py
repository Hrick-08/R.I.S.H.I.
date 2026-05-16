from rag.embedder import embed_query
from rag.qdrant_client import search_qdrant

TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "rag_search",
        "description": "Search Hrick's personal knowledge base (notes, docs, PDFs). Use when asked about anything that might be in stored documents.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Natural language query to search for.",
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of results to return.",
                    "default": 4,
                },
            },
            "required": ["query"],
        },
    },
}


async def run(query: str, top_k: int = 4) -> str:
    vector = await embed_query(query)
    results = await search_qdrant(vector, top_k=top_k)
    if not results:
        return "No relevant documents found."
    chunks = []
    for r in results:
        src = r.payload.get("source", "unknown")
        text = r.payload.get("text", "")
        chunks.append(f"[{src}]\n{text}")
    return "\n\n---\n\n".join(chunks)
