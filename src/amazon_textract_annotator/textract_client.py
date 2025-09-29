"""Textract API client with retry logic."""

import time
from typing import Any, Dict, List

import boto3
import click
from botocore.exceptions import ClientError

MAX_RETRIES = 3
BASE_DELAY = 2.0


class TextractClient:
    """Textract client with retry logic and response processing."""

    def __init__(self, max_retries: int = MAX_RETRIES, base_delay: float = BASE_DELAY):
        """Initialize TextractClient with retry configuration.

        Args:
            max_retries: Maximum number of retry attempts for throttled requests
            base_delay: Base delay in seconds for exponential backoff
        """
        self.textract = boto3.client("textract")
        self.max_retries = max_retries
        self.base_delay = base_delay

    def detect_document_text(self, file_bytes: bytes) -> Dict[str, Any]:
        """Get Textract response with retry logic."""
        for attempt in range(self.max_retries):
            try:
                response = self.textract.detect_document_text(Document={"Bytes": file_bytes})
                return response
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "ThrottlingException" and attempt < self.max_retries - 1:
                    delay = self.base_delay * (2**attempt)
                    click.echo(
                        f"Rate limited, waiting {delay} seconds before retry {attempt + 1}/{self.max_retries}..."
                    )
                    time.sleep(delay)
                    continue
                else:
                    raise

    def extract_word_blocks(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract WORD blocks with geometry from Textract response."""
        blocks = response.get("Blocks", [])
        return [block for block in blocks if block["BlockType"] == "WORD" and "Geometry" in block]
