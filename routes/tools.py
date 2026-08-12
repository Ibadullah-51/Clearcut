"""API endpoints that do the image processing.

Each endpoint accepts a multipart form upload, processes the bytes in memory,
and streams the result straight back to the browser as a file download. The
frontend turns that into a preview and a Download button. Nothing is stored.

Errors are returned as JSON with a friendly `error` message and a 4xx/5xx
status, so the frontend can show it in the interface.
"""
import io

from flask import Blueprint, request, jsonify, send_file

from config import ALLOWED_EXTENSIONS
from utils.image_processing import (
    ImageError,
    allowed_file,
    remove_background,
    compress_image,
    resize_convert,
)

tools = Blueprint("tools", __name__, url_prefix="/api")


def _get_upload():
    """Pull the uploaded file out of the request and validate the basics.

    Returns the raw bytes. Raises ImageError with a user-friendly message
    on any problem.
    """
    if "image" not in request.files:
        raise ImageError("No file was uploaded. Please choose an image.")
    file = request.files["image"]
    if not file or file.filename == "":
        raise ImageError("No file was selected. Please choose an image.")
    if not allowed_file(file.filename):
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS)).upper()
        raise ImageError(f"That file type isn't supported. Please use: {allowed}.")
    data = file.read()
    if not data:
        raise ImageError("That file seems to be empty.")
    return data


def _send(data: bytes, ext: str, download_name: str):
    """Send image bytes back as a downloadable file."""
    mime = {
        "jpg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
    }.get(ext, "application/octet-stream")
    return send_file(
        io.BytesIO(data),
        mimetype=mime,
        as_attachment=True,
        download_name=download_name,
    )


@tools.route("/remove-background", methods=["POST"])
def api_remove_background():
    data = _get_upload()
    result = remove_background(data)
    return _send(result, "png", "clearcut-no-background.png")


@tools.route("/compress", methods=["POST"])
def api_compress():
    data = _get_upload()
    try:
        quality = int(request.form.get("quality", 75))
    except (TypeError, ValueError):
        raise ImageError("Quality must be a number between 1 and 100.")
    result, ext = compress_image(data, quality)
    return _send(result, ext, f"clearcut-compressed.{ext}")


@tools.route("/resize", methods=["POST"])
def api_resize():
    data = _get_upload()

    def _int_or_none(name):
        raw = request.form.get(name, "").strip()
        if raw == "":
            return None
        try:
            value = int(raw)
        except ValueError:
            raise ImageError("Width and height must be whole numbers.")
        if value <= 0:
            raise ImageError("Width and height must be greater than zero.")
        return value

    width = _int_or_none("width")
    height = _int_or_none("height")
    keep_aspect = request.form.get("keep_aspect", "true").lower() != "false"
    out_format = request.form.get("format", "png")

    if width is None and height is None:
        raise ImageError("Enter a width, a height, or pick a preset size.")

    result, ext = resize_convert(data, width, height, keep_aspect, out_format)
    return _send(result, ext, f"clearcut-resized.{ext}")


# ---- Error handling for this blueprint -------------------------------------
@tools.errorhandler(ImageError)
def handle_image_error(err):
    """Anything the user did wrong -> 400 with a readable message."""
    return jsonify(error=str(err)), 400


@tools.errorhandler(Exception)
def handle_unexpected(err):
    """Last-resort catch so the frontend always gets JSON, never an HTML page."""
    return jsonify(error="Something went wrong while processing your image."), 500
