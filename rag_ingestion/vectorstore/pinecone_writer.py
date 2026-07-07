from pinecone import Pinecone
from schemas.vector_record import VectorRecord
from dotenv import load_dotenv 
load_dotenv(override=True)
import logging
import os


logger = logging.getLogger(__name__)

class PineconeWriter:
    def __init__(
        self,
        api_key: str,
        index_name: str,
        batch_size: int = 100,
    ):
        self.index = Pinecone(api_key=api_key).Index(index_name)

        self.batch_size = batch_size

    def upsert(
        self,
        records: list[VectorRecord],
    ) -> None:
        namespace = os.getenv("PINECONE_NAMESPACE")

        logger.info(
            "step=upsert_start file=%s record_count=%s batch_size=%s namespace=%s",
            __file__.split("\\")[-1].split("/")[-1],
            len(records),
            self.batch_size,
            namespace,
        )

        try:
            for start in range(0, len(records), self.batch_size):
                batch = records[start : start + self.batch_size]

                logger.info(
                    "step=upsert_batch file=%s batch_start=%s batch_count=%s namespace=%s",
                    __file__.split("\\")[-1].split("/")[-1],
                    start,
                    len(batch),
                    namespace,
                )

                self.index.upsert(
                    vectors=[
                        {
                            "id": record.id,
                            "values": record.values,
                            "metadata": record.metadata,
                        }
                        for record in batch
                    ],
                    namespace=namespace,
                )

            logger.info(
                "step=upsert_complete file=%s record_count=%s",
                __file__.split("\\")[-1].split("/")[-1],
                len(records),
            )
        except Exception:
            logger.exception(
                "step=upsert_failed file=%s record_count=%s namespace=%s",
                __file__.split("\\")[-1].split("/")[-1],
                len(records),
                namespace,
            )
            raise
