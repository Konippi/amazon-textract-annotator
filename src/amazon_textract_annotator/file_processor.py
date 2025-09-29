"""File processing logic and format detection."""

from pathlib import Path
from typing import Optional, Protocol

import click

from amazon_textract_annotator.annotators import ImageAnnotator, PDFAnnotator
from amazon_textract_annotator.textract_client import TextractClient


class Annotator(Protocol):
    """Protocol for annotators."""

    def annotate(self, file_path: str, output_path: str) -> None:
        """Annotate file with detected text boxes."""
        ...


class FileProcessor:
    """Handles file format detection and processing coordination."""

    SUPPORTED_FORMATS = {".pdf": "PDF", ".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG"}

    def __init__(self):
        """Initialize FileProcessor with TextractClient and annotators."""
        self.textract_client = TextractClient()
        self.pdf_annotator = PDFAnnotator(self.textract_client)
        self.image_annotator = ImageAnnotator(self.textract_client)

    def get_output_path(self, file_path: Path, output: Optional[Path]) -> Path:
        """Generate appropriate output path based on file type."""
        if output:
            return output
        return file_path.with_stem(f"{file_path.stem}.annotated")

    def get_annotator(self, file_suffix: str) -> Annotator:
        """Get appropriate annotator based on file format."""
        if file_suffix == ".pdf":
            return self.pdf_annotator
        elif file_suffix in [".png", ".jpg", ".jpeg"]:
            return self.image_annotator
        else:
            supported = ", ".join(self.SUPPORTED_FORMATS.keys())
            raise ValueError(f"Unsupported file format: {file_suffix}. Supported formats: {supported}")

    def process_file(self, file_path: Path, output: Optional[Path]) -> None:
        """Process file with appropriate annotator."""
        file_suffix = file_path.suffix.lower()

        if file_suffix not in self.SUPPORTED_FORMATS:
            click.echo(f"Unsupported file format: {file_suffix}")
            click.echo(f"Supported formats: {', '.join(self.SUPPORTED_FORMATS.keys())}")
            raise click.Abort()

        output_path = self.get_output_path(file_path, output)
        annotator = self.get_annotator(file_suffix)

        file_type = self.SUPPORTED_FORMATS[file_suffix]
        click.echo(f"Processing {file_type}: {file_path}")

        annotator.annotate(str(file_path), str(output_path))

        click.echo(f"Annotated {file_type.lower()} saved to: {output_path}")
