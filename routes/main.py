"""Routes that render HTML pages (the parts people see and Google indexes)."""
from flask import Blueprint, render_template, abort, Response, url_for

from config import BRAND_NAME, BRAND_TAGLINE, SITE_URL
from utils.blog_content import POSTS, POSTS_BY_SLUG

main = Blueprint("main", __name__)

# The three tools, described once and reused on the homepage.
TOOLS = [
    {
        "name": "Background Remover",
        "url": "/background-remover",
        "tagline": "Erase the background, keep the subject.",
        "detail": "Get a clean transparent PNG in seconds.",
        "tag": "PNG · transparent",
        "icon": "scissors",
    },
    {
        "name": "Image Compressor",
        "url": "/image-compressor",
        "tagline": "Shrink file size, keep it sharp.",
        "detail": "See the before-and-after size as you go.",
        "tag": "JPG · PNG · WebP",
        "icon": "minimize",
    },
    {
        "name": "Image Resizer",
        "url": "/image-resizer",
        "tagline": "Resize and convert in one step.",
        "detail": "Exact sizes or presets, any format.",
        "tag": "px · format",
        "icon": "resize",
    },
]


@main.route("/")
def home():
    return render_template(
        "index.html",
        page_title=f"{BRAND_NAME} — {BRAND_TAGLINE}",
        meta_description=(
            "Free online image tools: remove backgrounds, compress photos, "
            "and resize or convert images. No signup, no watermark, works in "
            "your browser."
        ),
        tools=TOOLS,
        posts=POSTS,
    )


@main.route("/background-remover")
def background_remover():
    return render_template(
        "tool_background_remover.html",
        page_title=f"Free Background Remover — {BRAND_NAME}",
        meta_description=(
            "Remove the background from any image for free. Upload a JPG or "
            "PNG and download a clean transparent PNG in seconds — no signup."
        ),
    )


@main.route("/image-compressor")
def image_compressor():
    return render_template(
        "tool_image_compressor.html",
        page_title=f"Free Image Compressor — {BRAND_NAME}",
        meta_description=(
            "Compress JPG, PNG, and WebP images to a smaller file size while "
            "keeping quality. See the before-and-after size instantly."
        ),
    )


@main.route("/image-resizer")
def image_resizer():
    return render_template(
        "tool_image_resizer.html",
        page_title=f"Free Image Resizer & Converter — {BRAND_NAME}",
        meta_description=(
            "Resize images to exact dimensions or presets and convert between "
            "JPG, PNG, and WebP. Free, fast, and no signup required."
        ),
    )


@main.route("/blog")
def blog():
    return render_template(
        "blog.html",
        page_title=f"Guides & Tutorials — {BRAND_NAME} Blog",
        meta_description=(
            "Beginner-friendly guides on removing backgrounds, compressing "
            "images, and resizing or converting photos."
        ),
        posts=POSTS,
    )


@main.route("/blog/<slug>")
def blog_post(slug):
    post = POSTS_BY_SLUG.get(slug)
    if post is None:
        abort(404)
    return render_template(
        "blog_post.html",
        page_title=f"{post['title']} — {BRAND_NAME}",
        meta_description=post["meta"],
        post=post,
    )


# ---- SEO extras -------------------------------------------------------------
@main.route("/robots.txt")
def robots():
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {SITE_URL}/sitemap.xml",
    ]
    return Response("\n".join(lines), mimetype="text/plain")


@main.route("/sitemap.xml")
def sitemap():
    urls = ["/", "/background-remover", "/image-compressor", "/image-resizer", "/blog"]
    urls += [f"/blog/{p['slug']}" for p in POSTS]
    items = "".join(
        f"<url><loc>{SITE_URL}{u}</loc></url>" for u in urls
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{items}</urlset>"
    )
    return Response(xml, mimetype="application/xml")
