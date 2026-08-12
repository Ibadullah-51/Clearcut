# Clearcut — free image tools

🔗 Live demo: https://clearcut-1.onrender.com/

Hosted on Render's free tier — if the app hasn't been used in a while, the first load may take 30–50 seconds while the server wakes up.

A small Flask website with three image utilities and a blog:

- **Background Remover** (`/background-remover`) — transparent PNG cutouts, powered by `rembg`
- **Image Compressor** (`/image-compressor`) — shrink file size with a quality slider, powered by Pillow
- **Image Resizer & Converter** (`/image-resizer`) — resize to exact/preset sizes and convert JPG/PNG/WebP, powered by Pillow
- **Blog** (`/blog`) — a guide for each tool

Images are processed **in memory** and streamed straight back to the browser — nothing is written to disk, so uploads can't pile up on the server.

---

## Setup (step by step)

You need **Python 3.10 or newer**. Check with `python --version`.

**1. Open a terminal in this folder** (the one containing `app.py`).

**2. Create a virtual environment** (keeps this project's packages separate):

```bash
python -m venv .venv
```

**3. Activate it:**

- macOS / Linux: `source .venv/bin/activate`
- Windows (PowerShell): `.venv\Scripts\Activate.ps1`

You'll know it worked when your prompt starts with `(.venv)`.

**4. Install the packages:**

```bash
pip install -r requirements.txt
```

> **Heads up about `rembg`:** it pulls in `onnxruntime` and, the *first time you
> remove a background*, downloads a ~170 MB AI model. That first run is slow;
> every run after is fast. If installing `rembg` gives you trouble, you can skip
> it for now — the Compressor and Resizer work without it, and the Background
> Remover will show a friendly "not available yet" message until it's installed.

**5. Run the app:**

```bash
python app.py
```

**6. Open** http://127.0.0.1:5000 in your browser.

To stop the server, press `Ctrl + C`.

---

## Project structure

```
clearcut/
├── app.py                  # entry point: creates the Flask app, error handlers
├── config.py               # all settings (brand name, size limits, formats)
├── requirements.txt
├── routes/
│   ├── main.py             # page routes (home, tools, blog, sitemap, robots)
│   └── tools.py            # /api endpoints that process images
├── utils/
│   ├── image_processing.py # the actual Pillow / rembg work (bytes in, bytes out)
│   ├── blog_content.py     # blog posts stored as data
│   └── cleanup.py          # temp-folder sweeper (safety net)
├── templates/              # Jinja2 HTML (base + one file per page)
├── static/
│   ├── css/style.css
│   ├── js/main.js          # nav + footer
│   └── js/tools.js         # reusable upload/preview/download engine
└── uploads/                # temp folder (stays empty in normal use)
```

## Common tweaks

- **Rename the site:** change `BRAND_NAME` in `config.py`.
- **Change the upload limit:** change `MAX_UPLOAD_MB` in `config.py`.
- **Add a blog post:** add a dict to `POSTS` in `utils/blog_content.py`.
- **Set your real domain** (for SEO tags/sitemap): change `SITE_URL` in `config.py`.

## Before going live

- Set `debug=False` in `app.py` and run behind a real server (e.g. `gunicorn app:app`).
- Set a real `SECRET_KEY` environment variable.
