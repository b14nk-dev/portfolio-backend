OPEN_SOURCE_RULES: list[tuple[tuple[str, ...], str]] = [
    (
        ("terminal monitor", "btop", "openui", "system monitor"),
        "open-source.terminal-ui",
    ),
    (
        ("rust repo", "rust tool", "leetcode", "better-cd", "wc-clone", "keypress"),
        "open-source.rust-tools",
    ),
    (
        ("javascript practice", "tdd repo", "practice repos"),
        "open-source.javascript-practice",
    ),
    (
        ("dotfiles", "nvim", "neovim", "cachyos", "bash scripts", "dev setup"),
        "open-source.environment",
    ),
    (("web repos", "older web", "profile readme"), "open-source.web-projects"),
    (
        ("backend repos", "node template", "blind chat", "assignment tracker"),
        "open-source.backend-tooling",
    ),
    (("open source", "github", "repository", "repo"), "open-source.overview"),
]

__all__ = ["OPEN_SOURCE_RULES"]
