from langchain_openai import OpenAIEmbeddings


class OpenAIEmbeddingProvider:
    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
    ):
        self.embedding_model = OpenAIEmbeddings(
            model=model,
            api_key=api_key,
        )

    def embed(
        self,
        text: list[str],
    ) -> list[float]:
        return self.embedding_model.embed_query(text)

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return self.embedding_model.embed_documents(texts)
