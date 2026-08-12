// Reusable engine for all three tool pages.
//
// Each page calls Clearcut.setupTool({...}) with:
//   endpoint       -> API URL to POST to
//   maxMB          -> upload size limit (matches the server)
//   buildFormData  -> (file) => FormData with any extra fields
//   originalLabel  -> label above the "before" preview
//   resultLabel    -> label above the "after" preview
//   actionText     -> button text (e.g. "Remove background")
//   onFile         -> optional callback(file) when a file is picked
//
// The engine handles drag/drop, client-side validation, the loading spinner,
// the fetch, error messages, before/after previews, and the download button.

window.Clearcut = (function () {
  const ALLOWED = ["image/jpeg", "image/png", "image/webp"];

  function formatBytes(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(2) + " MB";
  }

  function setupTool(cfg) {
    const root = document.querySelector("[data-tool]");
    if (!root) return;

    const dropzone = root.querySelector(".dropzone");
    const fileInput = root.querySelector('input[type="file"]');
    const controls = root.querySelector("[data-controls]");
    const runBtn = root.querySelector("[data-run]");
    const overlay = root.querySelector(".overlay");
    const msg = root.querySelector(".msg");
    const result = root.querySelector("[data-result]");

    const origImg = root.querySelector("[data-original-img]");
    const origMeta = root.querySelector("[data-original-meta]");
    const resImg = root.querySelector("[data-result-img]");
    const resMeta = root.querySelector("[data-result-meta]");
    const downloadBtn = root.querySelector("[data-download]");

    let currentFile = null;
    let lastObjectUrl = null;

    // ---- messages ----------------------------------------------------------
    function showError(text) {
      msg.textContent = text;
      msg.className = "msg msg--error is-show";
    }
    function clearMessage() {
      msg.className = "msg";
      msg.textContent = "";
    }

    // ---- file selection ----------------------------------------------------
    function handleFile(file) {
      clearMessage();
      if (!ALLOWED.includes(file.type)) {
        showError("That file type isn't supported. Please use JPG, PNG, or WebP.");
        return;
      }
      if (file.size > cfg.maxMB * 1024 * 1024) {
        showError("That file is too big. The limit is " + cfg.maxMB + " MB.");
        return;
      }
      currentFile = file;

      // show the original straight away
      if (lastObjectUrl) URL.revokeObjectURL(lastObjectUrl);
      lastObjectUrl = URL.createObjectURL(file);
      origImg.src = lastObjectUrl;
      origMeta.textContent = formatBytes(file.size);

      // reveal controls, reset any previous result
      controls.hidden = false;
      result.hidden = true;
      resImg.removeAttribute("src");
      resMeta.textContent = "";
      runBtn.disabled = false;

      // update the dropzone text to show the chosen file
      const label = dropzone.querySelector("[data-dz-text]");
      if (label) label.textContent = file.name;

      if (typeof cfg.onFile === "function") cfg.onFile(file);
    }

    // click to browse
    dropzone.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", (e) => {
      if (e.target.files.length) handleFile(e.target.files[0]);
    });

    // drag & drop
    ["dragenter", "dragover"].forEach((ev) =>
      dropzone.addEventListener(ev, (e) => {
        e.preventDefault();
        dropzone.classList.add("is-drag");
      })
    );
    ["dragleave", "drop"].forEach((ev) =>
      dropzone.addEventListener(ev, (e) => {
        e.preventDefault();
        dropzone.classList.remove("is-drag");
      })
    );
    dropzone.addEventListener("drop", (e) => {
      if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
    });

    // ---- processing --------------------------------------------------------
    async function run() {
      if (!currentFile) {
        showError("Please choose an image first.");
        return;
      }
      clearMessage();
      overlay.classList.add("is-active");
      runBtn.disabled = true;

      try {
        const formData = cfg.buildFormData(currentFile);
        const response = await fetch(cfg.endpoint, { method: "POST", body: formData });

        if (!response.ok) {
          // errors come back as JSON with an `error` field
          let text = "Something went wrong. Please try again.";
          try {
            const data = await response.json();
            if (data && data.error) text = data.error;
          } catch (_) {}
          showError(text);
          return;
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        resImg.src = url;
        result.hidden = false;

        // before/after size, with a "saved X%" note when it got smaller
        const origSize = currentFile.size;
        const newSize = blob.size;
        let metaText = formatBytes(newSize);
        if (newSize < origSize) {
          const saved = Math.round((1 - newSize / origSize) * 100);
          metaText += '  ·  <span class="saved">−' + saved + "%</span>";
        }
        resMeta.innerHTML = metaText;

        // wire up the download button, giving it the right extension for
        // whatever format the server actually returned
        var extByType = { "image/jpeg": "jpg", "image/png": "png", "image/webp": "webp" };
        var ext = extByType[blob.type] || "png";
        downloadBtn.href = url;
        downloadBtn.download = (cfg.downloadName || "clearcut-image") + "." + ext;

        result.scrollIntoView({ behavior: "smooth", block: "nearest" });
      } catch (err) {
        showError("Couldn't reach the server. Check your connection and try again.");
      } finally {
        overlay.classList.remove("is-active");
        runBtn.disabled = false;
      }
    }

    runBtn.addEventListener("click", run);
  }

  return { setupTool, formatBytes };
})();
