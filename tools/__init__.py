import importlib
import pkgutil
from pathlib import Path

TOOL_REGISTRY: dict[str, dict] = {}


def load_tools():
    tools_path = Path(__file__).parent
    for finder, name, ispkg in pkgutil.iter_modules([str(tools_path)]):
        if name == "__init__":
            continue
        module = importlib.import_module(f"tools.{name}")
        if hasattr(module, "TOOL_DEFINITION") and hasattr(module, "run"):
            TOOL_REGISTRY[module.TOOL_DEFINITION["function"]["name"]] = {
                "definition": module.TOOL_DEFINITION,
                "run": module.run,
            }


load_tools()


def get_tool_definitions() -> list[dict]:
    return [t["definition"] for t in TOOL_REGISTRY.values()]


async def dispatch_tool(name: str, arguments: dict) -> str:
    if name not in TOOL_REGISTRY:
        return f"Unknown tool: {name}"
    return await TOOL_REGISTRY[name]["run"](**arguments)
