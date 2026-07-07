from __future__ import annotations

import logging
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Bootstrap:

    def __init__(self):

        load_dotenv()

        self.failed = False

    
    # Public
    

    def run(self):

        logger.info("=" * 65)
        logger.info("Running startup validation...")
        logger.info("=" * 65)

        self.python()

        self.environment()

        self.poppler()

        self.tesseract()

        self.filesystem()

        self.summary()

    
    # Helpers
    

    def ok(self, message: str):

        logger.info("✓ %s", message)

    def warn(self, message: str):

        logger.warning("⚠ %s", message)

    def fail(self, message: str):

        self.failed = True

        logger.error("✗ %s", message)

    
    # Python
    

    def python(self):

        version = sys.version_info

        if version < (3, 11):

            self.fail(
                f"Python 3.11+ required. Current: {platform.python_version()}"
            )

        else:

            self.ok(
                f"Python {platform.python_version()}"
            )

    
    # Environment Variables
    

    def environment(self):

        required = {
            "OPENAI_API_KEY": True,
            "PINECONE_API": True,
            "INDEX_NAME": True,
            "HF_TOKEN": False,
        }

        for env, required_value in required.items():

            value = os.getenv(env)

            if value:

                self.ok(f"{env}")

            else:

                if required_value:

                    self.fail(f"{env} missing")

                else:

                    self.warn(f"{env} missing")

    
    # Poppler
    

    def poppler(self):

        exe = shutil.which("pdfinfo")

        if exe is None:

            self.fail("Poppler not installed")

            return

        try:

            subprocess.run(
                ["pdfinfo", "-v"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )

            self.ok(f"Poppler ({exe})")

        except Exception as e:

            self.fail(f"Poppler broken : {e}")

    
    # Tesseract
    

    def tesseract(self):

        exe = shutil.which("tesseract")

        if exe is None:

            self.fail("Tesseract not installed")

            return

        self.ok(f"Tesseract ({exe})")

        try:

            subprocess.run(
                ["tesseract", "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )

            self.ok("Tesseract executable")

        except Exception as e:

            self.fail(f"Tesseract broken : {e}")

        try:

            result = subprocess.run(
                ["tesseract", "--list-langs"],
                capture_output=True,
                text=True,
                check=True,
            )

            if "eng" not in result.stdout:

                self.fail("English OCR model missing")

            else:

                self.ok("OCR language : eng")

        except Exception as e:

            self.fail(f"OCR language check failed : {e}")

    
    # Filesystem
    

    def filesystem(self):

        folders = [
            "docs",
            "temp",
            "temp/images",
            "temp/temp_batches",
        ]

        for folder in folders:

            Path(folder).mkdir(
                parents=True,
                exist_ok=True,
            )

            self.ok(folder)

        pdf = Path("docs/sample.pdf")

        if pdf.exists():

            self.ok("sample.pdf")

        else:

            self.warn("docs/sample.pdf not found")

    
    # Summary
    

    def summary(self):

        logger.info("=" * 65)

        if self.failed:

            logger.error("Startup validation FAILED")

            logger.info("=" * 65)

            raise RuntimeError(
                "Bootstrap validation failed."
            )

        logger.info("Startup validation completed successfully.")

        logger.info("=" * 65)