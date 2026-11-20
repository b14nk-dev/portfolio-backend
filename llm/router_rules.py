from .core_rules import CORE_RULES
from .open_source_rules import OPEN_SOURCE_RULES
from .project_rules import PROJECT_RULES
from .skill_rules import SKILL_RULES

RULES: list[tuple[tuple[str, ...], str]] = (
    CORE_RULES + PROJECT_RULES + OPEN_SOURCE_RULES + SKILL_RULES
)

__all__ = ["RULES"]
