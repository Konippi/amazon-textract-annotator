"""Geometry utilities for coordinate conversion."""

from typing import Dict, Tuple


def convert_bbox_to_absolute(
    bbox_data: Dict[str, float], width: float, height: float
) -> Tuple[float, float, float, float]:
    """Convert normalized bounding box coordinates to absolute coordinates.

    Args:
        bbox_data: Textract bounding box data with Left, Top, Width, Height
        width: Document/image width
        height: Document/image height

    Returns:
        Tuple of (left, top, right, bottom) in absolute coordinates
    """
    left = bbox_data["Left"] * width
    top = bbox_data["Top"] * height
    right = (bbox_data["Left"] + bbox_data["Width"]) * width
    bottom = (bbox_data["Top"] + bbox_data["Height"]) * height

    return left, top, right, bottom
