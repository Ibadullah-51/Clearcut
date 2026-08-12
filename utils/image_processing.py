"""All the actual image work lives here.

Design choice: every function takes raw bytes in and returns raw bytes out,
working entirely in memory (io.BytesIO). Nothing is written to disk, so there
are no files to clean up and no way for uploads to pile up on the server.
That's the simplest way to guarantee the "don't let files accumulate"
requirement.
"""
import io
from PIL import Image, ImageOps

from config import ALLOWED_EXTENSIONS, OUTPUT_FORMATS


class ImageError(Exception):
    """Raised for anything the user did wrong (bad file, bad options).

    Routes catch this and turn the message into a friendly 400 response.
    """


# Map our short format names to what Pillow expects.
_PIL_FORMAT = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "webp": "WEBP"}


def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def _open_image(data: bytes) -> Image.Image:
    """Open bytes as an image, verifying it's really an image.

    Pillow raises if the bytes aren't a valid image, which is our real
    defence against someone renaming a .exe to .png. We also apply EXIF
    orientation so phone photos aren't rotated sideways.
    """
    try:
        img = Image.open(io.BytesIO(data))
        img.load()  # force decode now so errors surface here
    except Exception:
        raise ImageError("That file doesn't look like a valid image.")
    # exif_transpose returns a NEW image and drops the .format attribute,
    # so remember the format and re-attach it — the compressor relies on it.
    fmt = img.format
    img = ImageOps.exif_transpose(img)
    img.format = fmt
    return img


def _flatten_to_rgb(img: Image.Image, bg=(255, 255, 255)) -> Image.Image:
    """JPEG has no transparency. Paste onto a white background instead."""
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        canvas = Image.new("RGB", img.size, bg)
        canvas.paste(img, mask=img.split()[-1])
        return canvas
    return img.convert("RGB")


# ---- Background removal -----------------------------------------------------
# Uses the remove.bg API instead of a locally-loaded ML model. Running rembg's
# u2net/u2netp model in-process needs more RAM than a free-tier host usually
# has (it was getting OOM-killed on Render's 512 MB plan). Offloading the
# actual model inference to remove.bg's servers means our server only ever
# holds one small image in memory at a time.
import os

import requests

REMOVEBG_API_URL = "https://api.remove.bg/v1.0/removebg"


def remove_background(data: bytes) -> bytes:
    """Return a PNG (with transparency) that has the background removed."""
    _open_image(data)  # validate input first

    api_key = os.environ.get("REMOVEBG_API_KEY")
    if not api_key:
        raise ImageError(
            "Background removal isn't configured on this server yet. "
            "Set the REMOVEBG_API_KEY environment variable."
        )

    try:
        response = requests.post(
            REMOVEBG_API_URL,
            files={"image_file": ("image.png", data)},
            data={"size": "auto"},
            headers={"X-Api-Key": api_key},
            timeout=30,
        )
    except requests.RequestException:
        raise ImageError("Couldn't reach the background removal service. Please try again.")

    if response.status_code != 200:
        try:
            detail = response.json()["errors"][0]["title"]
        except Exception:
            detail = "Background removal failed."
        if response.status_code == 402:
            detail = "Background removal quota reached for this month."
        raise ImageError(detail)

    out = Image.open(io.BytesIO(response.content)).convert("RGBA")
    buf = io.BytesIO()
    out.save(buf, format="PNG", optimize=True)
    return buf.getvalue()

# ---- Compression ------------------------------------------------------------
def compress_image(data: bytes, quality: int) -> tuple[bytes, str]:
    """Compress an image. Returns (bytes, extension).

    `quality` is 1–100. For JPEG/WebP it maps straight to the encoder's
    quality. PNG ignores quality, so for PNGs we quantise the colour palette
    more aggressively as quality drops, which is what actually shrinks them.
    """
    quality = max(1, min(100, int(quality)))
    img = _open_image(data)
    fmt = (img.format or "PNG").upper()
    buf = io.BytesIO()

    if fmt in ("JPEG", "MPO"):
        _flatten_to_rgb(img).save(
            buf, format="JPEG", quality=quality, optimize=True, progressive=True
        )
        return buf.getvalue(), "jpg"

    if fmt == "WEBP":
        img.save(buf, format="WEBP", quality=quality, method=6)
        return buf.getvalue(), "webp"

    # PNG (and anything else) -> PNG. Quantise colours based on quality.
    work = img.convert("RGBA") if img.mode in ("RGBA", "LA", "P") else img.convert("RGB")
    colors = max(8, int(256 * quality / 100))  # fewer colours = smaller file
    try:
        work = work.quantize(colors=colors, method=Image.MEDIANCUT)
    except Exception:
        pass  # if quantise fails, fall back to plain optimised PNG
    work.save(buf, format="PNG", optimize=True)
    return buf.getvalue(), "png"


# ---- Resize / convert -------------------------------------------------------
def resize_convert(
    data: bytes,
    width: int | None,
    height: int | None,
    keep_aspect: bool,
    out_format: str,
) -> tuple[bytes, str]:
    """Resize and/or convert an image. Returns (bytes, extension)."""
    out_format = (out_format or "png").lower()
    if out_format not in OUTPUT_FORMATS:
        raise ImageError("Choose a valid output format: JPG, PNG, or WebP.")

    img = _open_image(data)
    orig_w, orig_h = img.size

    # Work out the target size.
    if width or height:
        if keep_aspect:
            # Scale to fit inside whichever dimension(s) were given.
            target_w = width or orig_w
            target_h = height or orig_h
            ratio = min(target_w / orig_w, target_h / orig_h)
            new_size = (max(1, round(orig_w * ratio)), max(1, round(orig_h * ratio)))
        else:
            new_size = (width or orig_w, height or orig_h)
            if new_size[0] < 1 or new_size[1] < 1:
                raise ImageError("Width and height must be positive numbers.")
        if new_size[0] > 10000 or new_size[1] > 10000:
            raise ImageError("That's too large — keep dimensions under 10000px.")
        img = img.resize(new_size, Image.LANCZOS)

    buf = io.BytesIO()
    pil_fmt = _PIL_FORMAT[out_format]
    if pil_fmt == "JPEG":
        _flatten_to_rgb(img).save(buf, format="JPEG", quality=90, optimize=True)
        ext = "jpg"
    elif pil_fmt == "WEBP":
        img.save(buf, format="WEBP", quality=90, method=6)
        ext = "webp"
    else:  # PNG
        img.save(buf, format="PNG", optimize=True)
        ext = "png"
    return buf.getvalue(), ext
