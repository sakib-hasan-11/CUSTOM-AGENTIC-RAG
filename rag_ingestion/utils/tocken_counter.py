import tiktoken


class TokenCounter:

    def __init__(
        self,
        model: str = "text-embedding-3-small",
    ):
        self.encoder = tiktoken.encoding_for_model(model)

    def count(
        self,
        text: str | None,
    ) -> int:

        if not text:
            return 0

        return len(self.encoder.encode(text))


_counter = TokenCounter()


def count_tokens(text: str | None) -> int:
    return _counter.count(text)