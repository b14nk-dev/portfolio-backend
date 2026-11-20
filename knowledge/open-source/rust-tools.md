# Open Source — Rust Tools

## better-cd

<https://github.com/b14nk-dev/better-cd> · Rust, sled

A `cd` replacement that bookmarks directories: save a path under a name, jump
back with it, list/delete/clear bookmarks, optionally create missing
directories. Persistence in a `sled` embedded database; designed to be aliased
over `cd`. Shows stateful CLI design, argument parsing and packaging a daily-use
tool.

## wc-clone-rust

<https://github.com/b14nk-dev/wc-clone-rust> · Rust

`rwc`, a clone of Unix `wc` supporting byte (`-c`), line (`-l`), word (`-w`) and
character (`-m`) counts, including multibyte UTF-8. Split into `error`, `file`,
`path` and `scanner` modules, with path validation before processing.

## keypress-sound

<https://github.com/b14nk-dev/keypress-sound> · Rust, `evdev`, `rodio`

A daemon that finds keyboards under `/dev/input`, reads key events with `evdev`
and plays one of six embedded mechanical-key sounds through `rodio`, compiled in
with `include_bytes!`.

## leetcode-with-rust

<https://github.com/b14nk-dev/leetcode-with-rust> · Rust

29 solutions, one module per problem (`p1021_...`, `p1108_...`), with shell
helpers to scaffold and push new ones.
