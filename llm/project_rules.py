PROJECT_RULES: list[tuple[tuple[str, ...], str]] = [
    (("fitclub",), "projects.fitclub"),
    (("rishtey",), "projects.rishtey"),
    (
        (
            "thai tourism customer",
            "booking site",
            "customer site",
            "supplier portal",
            "agent portal",
            "110 routes",
        ),
        "projects.thai-tourism-customer",
    ),
    (
        ("thai tourism crm", "thai api", "taxi transfer", "partner portal"),
        "projects.thai-tourism-api",
    ),
    (("thai tourism", "travel platform", "booking platform"), "projects.thai-tourism"),
    (("gold rates", "live gold", "react native app"), "projects.live-gold-rates"),
    (
        (
            "portfolio assistant",
            "this assistant",
            "this site",
            "ai assistant",
            "chatbot",
        ),
        "projects.portfolio-assistant",
    ),
    (("jobradar", "job radar"), "projects.jobradar"),
    (("justmyfare", "flight booking project"), "projects.flight-book"),
    (
        (
            "quick watch",
            "terminal portfolio",
            "ascii art",
        ),
        "projects.personal",
    ),
]

__all__ = ["PROJECT_RULES"]
