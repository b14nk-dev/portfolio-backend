START = "<extras>"
END = "</extras>"


class ExtrasFilter:
    def __init__(self) -> None:
        self._pending = ""
        self._extras = ""
        self._capturing = False
        self._done = False

    def feed(self, text: str) -> str:
        if self._done or not text:
            return text

        self._pending += text
        out: list[str] = []

        while True:
            if self._capturing:
                idx = self._pending.lower().find(END)
                if idx == -1:
                    keep = len(END) - 1
                    if len(self._pending) > keep:
                        self._extras += self._pending[:-keep]
                        self._pending = self._pending[-keep:]
                    break
                self._extras += self._pending[:idx]
                self._pending = self._pending[idx + len(END) :]
                self._capturing = False
                self._done = True
                out.append(self._pending)
                self._pending = ""
                break

            idx = self._pending.lower().find(START)
            if idx != -1:
                out.append(self._pending[:idx])
                self._pending = self._pending[idx + len(START) :]
                self._capturing = True
                continue

            keep = len(START) - 1
            if len(self._pending) > keep:
                out.append(self._pending[:-keep])
                self._pending = self._pending[-keep:]
            break

        return "".join(out)

    def finish(self) -> tuple[str, str]:
        if self._done:
            return "", self._extras

        if self._capturing:
            self._pending = ""
            self._extras = ""
            self._capturing = False
            self._done = True
            return "", ""

        tail = self._pending
        self._pending = ""
        self._done = True
        return tail, ""


__all__ = ["END", "START", "ExtrasFilter"]
