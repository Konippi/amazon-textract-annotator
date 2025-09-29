# Amazon Textract Annotator

A Python CLI tool that uses Amazon Textract to detect text in documents and images, then annotates them with red bounding boxes around detected text areas.

## Features

- **Multi-format support**: Process PDF documents and images
- **Amazon Textract integration**: Leverages AWS Textract for accurate text detection
- **Visual annotation**: Draws red bounding boxes around detected text

## Installation

### Prerequisites

- Python 3.10 or higher
- AWS credentials configured
- Required permissions for Amazon Textract service

## Usage

1. Install depedencies

    ```bash
    $ uv sync
    ```

2. Run the app

    ```bash
    # PDF
    $ uv run app assets/statement.pdf

    # JPEG
    $ uv run app assets/statement.jpg
    ```