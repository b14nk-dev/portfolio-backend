from .router_rules import RULES

MAX_UNITS = 3


def route_units(question: str) -> list[str]:
    q = question.lower()

    if any(term in q for term in ("list", "all")) and "project" in q:
        return ["projects.overview"]

    units: list[str] = []
    for terms, unit in RULES:
        if unit not in units and any(term in q for term in terms):
            units.append(unit)
            if len(units) == MAX_UNITS:
                break

    return units or ["core.summary"]


__all__ = ["route_units"]
