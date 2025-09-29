"""Document and image annotators."""

import click
import fitz
from PIL import Image, ImageDraw

from .geometry import convert_bbox_to_absolute
from .textract_client import TextractClient


class PDFAnnotator:
    """PDF annotation using PyMuPDF."""

    def __init__(self, textract_client: TextractClient):
        """Initialize PDFAnnotator with TextractClient.

        Args:
            textract_client: TextractClient instance for API calls
        """
        self.textract_client = textract_client

    def annotate(self, pdf_path: str, output_path: str) -> None:
        """Extract text from PDF using Textract and annotate with red boxes."""
        # Read PDF file as bytes
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        response = self.textract_client.detect_document_text(pdf_bytes)
        word_blocks = self.textract_client.extract_word_blocks(response)

        click.echo(f"Textract detected {len(response.get('Blocks', []))} blocks")

        # Open PDF and get page dimensions with proper resource management
        with fitz.open(pdf_path) as doc:
            if len(doc) == 0:
                raise ValueError("PDF file is empty or corrupted")

            page = doc[0]
            page_rect = page.rect
            width = page_rect.width
            height = page_rect.height

            # Annotate PDF with bounding boxes
            for block in word_blocks:
                bbox_data = block["Geometry"]["BoundingBox"]
                left, top, right, bottom = convert_bbox_to_absolute(bbox_data, width, height)

                # Create rectangle annotation
                rect = fitz.Rect(left, top, right, bottom)
                annot = page.add_rect_annot(rect)
                annot.set_colors(stroke=(1, 0, 0))  # Red color
                annot.set_border(width=2)
                annot.update()

            click.echo(f"Annotated {len(word_blocks)} words")
            doc.save(output_path)


class ImageAnnotator:
    """Image annotation using Pillow."""

    def __init__(self, textract_client: TextractClient):
        """Initialize ImageAnnotator with TextractClient.

        Args:
            textract_client: TextractClient instance for API calls
        """
        self.textract_client = textract_client

    def annotate(self, image_path: str, output_path: str) -> None:
        """Extract text from image using Textract and annotate with red boxes."""
        # Read image file as bytes
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        response = self.textract_client.detect_document_text(image_bytes)
        word_blocks = self.textract_client.extract_word_blocks(response)

        click.echo(f"Textract detected {len(response.get('Blocks', []))} blocks")

        # Open image and get dimensions with proper resource management
        with Image.open(image_path) as image:
            width, height = image.size

            # Create a copy to avoid modifying the original image object
            image_copy = image.copy()
            draw = ImageDraw.Draw(image_copy)

            # Annotate image with bounding boxes
            for block in word_blocks:
                bbox_data = block["Geometry"]["BoundingBox"]
                left, top, right, bottom = convert_bbox_to_absolute(bbox_data, width, height)

                # Draw rectangle
                draw.rectangle([left, top, right, bottom], outline="red", width=2)

            click.echo(f"Annotated {len(word_blocks)} words")
            image_copy.save(output_path)
