from llm.LLM import LLM
from llm.tools import get_info

tools_dict = {"get_info": get_info}

__all__ = ["LLM", "tools_dict"]
