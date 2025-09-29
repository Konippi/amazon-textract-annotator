"""Textract Document Annotator."""

from pathlib import Path
from typing import Optional

import click

from amazon_textract_annotator.file_processor import FileProcessor


@click.command()
@click.argument(
    "file_path",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--output-path",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to save the annotated document.",
)
def main(file_path: Path, output_path: Optional[Path]):
    """Extract text from document/image using Amazon Textract and annotate with red boxes around detected text."""
    try:
        processor = FileProcessor()
        processor.process_file(file_path, output_path)
    except Exception as e:
        click.echo(f"Error processing file: {e}", err=True)
        raise click.Abort() from e


if __name__ == "__main__":
    main()
