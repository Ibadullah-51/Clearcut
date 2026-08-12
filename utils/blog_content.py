"""Blog posts stored as plain data.

Keeping posts here (rather than as separate HTML files) means one template
renders all of them, and adding a post is just adding a dict. Each post's
`body` is a list of blocks the template knows how to render.

Block types:
  {"type": "p", "text": "..."}                     paragraph
  {"type": "h2", "text": "..."}                    section heading
  {"type": "steps", "items": ["...", "..."]}       numbered how-to list
  {"type": "list", "items": ["...", "..."]}        bulleted list
  {"type": "cta", "text": "...", "url": "/..."}    button linking to a tool
"""

POSTS = [
    {
        "slug": "how-to-remove-image-backgrounds",
        "title": "How to Remove the Background From an Image (Free, No Signup)",
        "meta": (
            "Learn how to remove the background from any photo for free in "
            "seconds. Step-by-step guide to getting a clean transparent PNG "
            "with no design skills needed."
        ),
        "keywords": "remove background, transparent png, background remover, cut out image",
        "tool": "Background Remover",
        "tool_url": "/background-remover",
        "read_time": "3 min read",
        "excerpt": (
            "Get a clean, transparent cutout from any photo in seconds — no "
            "Photoshop, no signup, no watermark."
        ),
        "body": [
            {"type": "p", "text": "A transparent background is one of the most useful things you can do to a photo. It lets you drop a product onto any colour, build a clean logo, make a profile picture that isn't stuck in a box, or design a thumbnail that pops. The problem is that doing it by hand — tracing around hair, edges, and fuzzy outlines — is slow and fiddly."},
            {"type": "p", "text": "The Clearcut Background Remover does it automatically. It looks at your image, works out what the main subject is, and erases everything else, leaving you with a PNG that has a see-through background."},
            {"type": "h2", "text": "What the tool does"},
            {"type": "p", "text": "You give it a photo. It gives you back the same photo with the background gone — saved as a PNG, which is the image format that supports transparency. The checkerboard pattern you see behind the result is just how transparency is shown on screen; it isn't part of the file."},
            {"type": "h2", "text": "How to use it, step by step"},
            {"type": "steps", "items": [
                "Open the Background Remover and drag your image onto the upload area (or click to browse). JPG, PNG, and WebP all work.",
                "Wait a few seconds while it processes. The first run can take a little longer.",
                "Compare the original and the cutout side by side. The result sits on a checkerboard so you can see exactly what became transparent.",
                "Click Download to save your transparent PNG.",
            ]},
            {"type": "h2", "text": "Common use cases"},
            {"type": "list", "items": [
                "Product photos for online shops, so items sit cleanly on any background.",
                "Profile and team headshots with a consistent look.",
                "Logos and graphics you want to reuse without a white box around them.",
                "YouTube thumbnails and social posts where the subject needs to stand out.",
            ]},
            {"type": "p", "text": "Tip: results are best when your subject is clearly separated from the background. Busy or low-contrast backgrounds are harder, so a bit of contrast between the subject and what's behind it goes a long way."},
            {"type": "cta", "text": "Try the Background Remover", "url": "/background-remover"},
        ],
    },
    {
        "slug": "how-to-compress-images-without-losing-quality",
        "title": "How to Compress Images Without Losing Quality",
        "meta": (
            "Compress JPG and PNG images to a smaller file size while keeping "
            "them sharp. Free online image compressor with a before-and-after "
            "size comparison."
        ),
        "keywords": "compress image, reduce file size, image compressor, shrink jpg png",
        "tool": "Image Compressor",
        "tool_url": "/image-compressor",
        "read_time": "4 min read",
        "excerpt": (
            "Shrink your images so pages load faster and files fit under upload "
            "limits — while keeping them looking sharp."
        ),
        "body": [
            {"type": "p", "text": "Big image files slow down websites, eat storage, and bump into email and upload limits. Compression fixes that by removing data the eye barely notices, making the file smaller while keeping the picture looking almost the same."},
            {"type": "h2", "text": "What the tool does"},
            {"type": "p", "text": "The Clearcut Image Compressor takes your photo and re-saves it more efficiently. You control how hard it squeezes with a single quality slider, and the tool shows you the before and after file size so you can see exactly how much you saved."},
            {"type": "h2", "text": "How to use it, step by step"},
            {"type": "steps", "items": [
                "Upload your image on the Image Compressor page.",
                "Drag the quality slider. Higher keeps more detail; lower makes a smaller file.",
                "Click Compress and check the new file size next to the original.",
                "Happy with it? Click Download. Want smaller? Lower the slider and compress again.",
            ]},
            {"type": "h2", "text": "How much should you compress?"},
            {"type": "list", "items": [
                "Photos for the web: around 70–80% quality is usually invisible to the eye and cuts size dramatically.",
                "Images that will be viewed large or printed: stay above 85% to keep detail.",
                "When you just need it under a size limit: drop the slider until it fits, then check it still looks fine.",
            ]},
            {"type": "p", "text": "A quick note on formats: JPG compresses photographs really well. PNG is better for graphics with flat colours or transparency, and it compresses in a different way — so a PNG won't always shrink as much as a JPG of the same picture."},
            {"type": "cta", "text": "Try the Image Compressor", "url": "/image-compressor"},
        ],
    },
    {
        "slug": "how-to-resize-and-convert-images",
        "title": "How to Resize and Convert Images (JPG, PNG, WebP)",
        "meta": (
            "Resize images to exact dimensions or presets, and convert between "
            "JPG, PNG, and WebP for free. Simple step-by-step guide for "
            "beginners."
        ),
        "keywords": "resize image, convert image, jpg to png, png to webp, image dimensions",
        "tool": "Image Resizer",
        "tool_url": "/image-resizer",
        "read_time": "4 min read",
        "excerpt": (
            "Set exact dimensions or pick a preset, and switch between JPG, "
            "PNG, and WebP — all in one step."
        ),
        "body": [
            {"type": "p", "text": "Resizing changes an image's dimensions — how many pixels wide and tall it is. Converting changes its format — whether it's a JPG, PNG, or WebP. You often need both at once: a photo that's the right size and the right format for wherever it's going."},
            {"type": "h2", "text": "What the tool does"},
            {"type": "p", "text": "The Clearcut Image Resizer lets you type in an exact width and height, or pick a common preset. It can lock the aspect ratio so your image doesn't stretch, and it can save the result as JPG, PNG, or WebP."},
            {"type": "h2", "text": "How to use it, step by step"},
            {"type": "steps", "items": [
                "Upload your image on the Image Resizer page.",
                "Enter a width and height, or choose a preset size.",
                "Keep 'Lock aspect ratio' ticked so the image stays in proportion (untick it only if you want an exact size and don't mind stretching).",
                "Pick your output format: JPG, PNG, or WebP.",
                "Click Resize, preview the result, and download it.",
            ]},
            {"type": "h2", "text": "Which format should you pick?"},
            {"type": "list", "items": [
                "JPG: best for photographs. Small files, but no transparency.",
                "PNG: best for logos, screenshots, and anything with transparency or sharp edges.",
                "WebP: a modern format that's usually smaller than both — great for websites, though a few older apps don't support it.",
            ]},
            {"type": "h2", "text": "Common use cases"},
            {"type": "list", "items": [
                "Shrinking a huge camera photo down to a web-friendly size.",
                "Making a square version of an image for a profile picture.",
                "Converting a PNG to WebP to speed up a website.",
                "Turning a transparent PNG into a JPG with a solid background.",
            ]},
            {"type": "cta", "text": "Try the Image Resizer", "url": "/image-resizer"},
        ],
    },
]

# Quick lookup by slug for the individual post route.
POSTS_BY_SLUG = {p["slug"]: p for p in POSTS}
