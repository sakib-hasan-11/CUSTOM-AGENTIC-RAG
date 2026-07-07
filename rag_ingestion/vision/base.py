from pathlib import Path

from abc import ABC, abstractmethod

class VisionProvider(ABC):

    @abstractmethod
    def summarize(
        self,
        image_path: Path,
        context: str | None = None,
    ) -> str:
        """Generate a summary for an image."""