from groq.types.chat.chat_completion_tool_param import ChatCompletionToolParam


def get_info() -> str:
    return """
    I'm a full-stack engineer with ~3 years of experience building and operating production applications. My work covers backend services and REST APIs, relational and NoSQL data modelling, JWT authentication and role-based access control, payment integrations and production performance work.
    I've taken features from requirements to release across web, mobile and browser extensions — including Chrome extensions used by 15,000+ people every month. I care about measurable outcomes: faster dashboards, fewer redundant API calls and systems that stay reliable under real traffic.
    """


TOOLS_SCHEMA: list[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "get_info",
            "description": "Get Ritik's background, experience, skills, and project highlights. Use for any question about his qualifications.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    }
]
__all__ = ["get_info"]
