CORE_RULES: list[tuple[tuple[str, ...], str]] = [
    (
        (
            "bangalore",
            "bengaluru",
            "delhi",
            "noida",
            "gurugram",
            "gurgaon",
            "remote",
            "hybrid",
            "office",
            "relocat",
            "location",
            "full-time",
        ),
        "core.availability",
    ),
    (
        ("contact", "email", "phone", "resume", "linkedin", "portfolio", "reach you"),
        "core.contact",
    ),
    (("why hire", "hire you", "why should we"), "faq.why-hire"),
    (
        ("who are you", "who is ritik", "your name", "introduce yourself", "handle"),
        "core.identity",
    ),
    (
        (
            "metrics",
            "how many users",
            "scale",
            "transactions",
            "records",
            "measurable",
            "impact numbers",
        ),
        "core.metrics",
    ),
    (
        (
            "callsmaster",
            "current company",
            "current employer",
            "current job",
            "where do you work",
        ),
        "experience.callsmaster",
    ),
]

__all__ = ["CORE_RULES"]
