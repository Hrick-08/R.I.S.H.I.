import json
from openai.types.chat import ChatCompletionMessageParam
from agent.llm_router import get_llm
from agent.prompt import SYSTEM_PROMPT
from tools import get_tool_definitions, dispatch_tool

MAX_TURNS = 8


async def run_agent(messages: list[ChatCompletionMessageParam]) -> str:
    client, model = get_llm()
    tools = get_tool_definitions()

    full_messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *messages,
    ]

    for _ in range(MAX_TURNS):
        response = await client.chat.completions.create(
            model=model, messages=full_messages, tools=tools, tool_choice="auto"
        )
        msg = response.choices[0].message

        if msg.tool_calls:
            full_messages.append(msg)
            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments)
                result = await dispatch_tool(tc.function.name, args)
                full_messages.append(
                    {"role": "tool", "tool_call_id": tc.id, "content": result}
                )
        else:
            return msg.content or ""

    return "I ran into a loop. Please try rephrasing."
