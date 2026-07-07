from embedding.openai_provider import OpenAIEmbeddingProvider
from schemas.chunk import DocumentChunk
from schemas.vector_record import VectorRecord
from utils.markdown_renderer import MarkdownRenderer


class EmbeddingProcessor:
    def __init__(
        self,
        provider: OpenAIEmbeddingProvider,
        renderer: MarkdownRenderer,
    ):
        self.provider = provider
        self.renderer = renderer

    def embed(
        self,
        chunk: DocumentChunk,
    ) -> VectorRecord:
        markdown = self.renderer.render(chunk)

        vector = self.provider.embed(markdown)

        metadata = dict(chunk.metadata)
        metadata["text"] = markdown

        return VectorRecord(
            id=chunk.chunk_id,
            values=vector,
            metadata=metadata,
        )

    def embed_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> list[VectorRecord]:
        markdowns = [self.renderer.render(chunk) for chunk in chunks]

        vectors = self.provider.embed_batch(markdowns)

        records: list[VectorRecord] = []

        for chunk, markdown, vector in zip(chunks, markdowns, vectors):
            metadata = dict(chunk.metadata)
            metadata["text"] = markdown

            records.append(
                VectorRecord(
                    id=chunk.chunk_id,
                    values=vector,
                    metadata=metadata,
                )
            )

        return records
