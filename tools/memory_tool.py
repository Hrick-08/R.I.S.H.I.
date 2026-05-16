from memory.store import store_fact, get_facts, store_summary, get_summary

TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "memory",
        "description": "Store or retrieve persistent user facts and conversation summaries. Use to remember important information about the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform: 'store_fact', 'get_facts', 'store_summary', 'get_summary'",
                    "enum": ["store_fact", "get_facts", "store_summary", "get_summary"],
                },
                "key": {
                    "type": "string",
                    "description": "Key for storing a fact (required for store_fact)",
                },
                "value": {
                    "type": "string",
                    "description": "Value for storing a fact (required for store_fact)",
                },
                "user_id": {
                    "type": "integer",
                    "description": "User ID for storing/retrieving facts",
                },
            },
            "required": ["action"],
        },
    },
}


async def run(
    action: str, key: str = None, value: str = None, user_id: int = None
) -> str:
    if action == "store_fact":
        if not key or not value or not user_id:
            return "store_fact requires key, value, and user_id"
        await store_fact(user_id, key, value)
        return f"Stored: {key} = {value}"

    elif action == "get_facts":
        if not user_id:
            return "get_facts requires user_id"
        facts = await get_facts(user_id)
        if not facts:
            return "No facts stored for this user."
        return "Stored facts:\n" + "\n".join([f"- {k}: {v}" for k, v in facts])

    elif action == "store_summary":
        if not value or not user_id:
            return "store_summary requires value and user_id"
        await store_summary(user_id, value)
        return "Conversation summary stored."

    elif action == "get_summary":
        if not user_id:
            return "get_summary requires user_id"
        summary = await get_summary(user_id)
        if not summary:
            return "No summary stored for this user."
        return f"Summary: {summary}"

    return f"Unknown action: {action}"
