"""Central configuration for the Clearcut app.

Everything you'd want to tweak (brand name, file-size limit, allowed
formats) lives here so you don't have to hunt through the code.
"""
import os

# ---- Branding ---------------------------------------------------------------
# Change this one line to rename the whole site.
BRAND_NAME = "Clearcut"
BRAND_TAGLINE = "Quick, free image tools that run in your browser tab."
SITE_URL = "https://example.com"  # used for SEO canonical tags + sitemap

# ---- Uploads / limits -------------------------------------------------------
# Maximum upload size in megabytes. Flask rejects anything larger with a 413
# *before* our code runs, which protects the server from huge files.
MAX_UPLOAD_MB = 12
MAX_CONTENT_LENGTH = MAX_UPLOAD_MB * 1024 * 1024

# File extensions we accept as input. We still verify the real image content
# with Pillow later — extensions alone can be faked.
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# Formats the resizer/converter can output.
OUTPUT_FORMATS = {"jpg", "png", "webp"}

# A temp folder is created for any on-disk work. The tools below process
# images fully in memory, so nothing normally lands here — but the folder and
# the cleanup helper exist for when you extend the app.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Delete anything left in the temp folder older than this many minutes.
TEMP_FILE_MAX_AGE_MIN = 15


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH
    UPLOAD_FOLDER = UPLOAD_FOLDER
