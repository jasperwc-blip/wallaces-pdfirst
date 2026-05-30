from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from app.services.pdf_ops import remove_pdf_annotations

LEGAL_NOTICE = (
    "Only remove watermarks from files you own or are authorized to modify. "
    "This feature must not be used to remove copyright, ownership, anti-piracy, "
    "or third-party attribution watermarks unlawfully."
)


def remove_pdf_watermark_best_effort(input_pdf: str | Path, output_pdf: str | Path) -> Path:
    """Best-effort local PDF cleanup: remove annotation/object overlays only."""
    return remove_pdf_annotations(input_pdf, output_pdf)


def remove_image_watermark_rectangles(
    input_image: str | Path,
    output_image: str | Path,
    rectangles: list[tuple[int, int, int, int]],
) -> Path:
    """Best-effort image cleanup using OpenCV inpainting when available, otherwise blur/fill."""
    source = Path(input_image)
    output = Path(output_image)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        import cv2  # type: ignore
        import numpy as np

        img = cv2.imread(str(source))
        if img is None:
            raise ValueError("Unsupported image file.")
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        for x1, y1, x2, y2 in rectangles:
            cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
        result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
        cv2.imwrite(str(output), result)
    except Exception:
        with Image.open(source).convert("RGB") as img:
            result = img.copy()
            draw = ImageDraw.Draw(result)
            for rect in rectangles:
                crop = result.crop(rect).filter(ImageFilter.GaussianBlur(12))
                result.paste(crop, rect)
                draw.rectangle(rect, outline=(230, 230, 230))
            result.save(output)
    return output
