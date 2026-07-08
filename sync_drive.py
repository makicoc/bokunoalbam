#!/usr/bin/env python3
import html
import io
import json
import os
import re
import shutil
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
IMAGES = SITE / "images"
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; VRChatDriveAlbum/1.0)"}
SUPPORTED = {".jpg", ".jpeg", ".png", ".webp"}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


def list_public_folder(folder_url: str):
    if not folder_url.startswith("https://drive.google.com/drive/folders/"):
        raise RuntimeError("config.jsonのdrive_folder_urlへGoogle Drive共有フォルダURLを設定してください。")
    page = fetch(folder_url).decode("utf-8", errors="replace")
    patterns = [
        re.compile(r'data-id="([^"]+)"[^>]*data-tooltip="([^"]+)\s+Image"', re.IGNORECASE),
        re.compile(r'\["([A-Za-z0-9_-]{20,})","([^"]+\.(?:jpe?g|png|webp))"', re.IGNORECASE),
    ]
    files, seen = [], set()
    for pattern in patterns:
        for file_id, name in pattern.findall(page):
            name = html.unescape(name.replace("\\u0027", "'").replace("\\u003d", "="))
            if file_id in seen or Path(name).suffix.lower() not in SUPPORTED:
                continue
            seen.add(file_id)
            files.append((name, file_id))
    files.sort(key=lambda value: value[0].casefold())
    if not files:
        raise RuntimeError("画像が見つかりません。フォルダを『リンクを知っている全員・閲覧者』で共有してください。")
    return files


def convert_image(source: bytes, destination: Path):
    max_size = max(256, min(4096, int(CONFIG.get("max_size", 2048))))
    quality = max(60, min(95, int(CONFIG.get("jpeg_quality", 88))))
    with Image.open(io.BytesIO(source)) as original:
        image = ImageOps.exif_transpose(original).convert("RGB")
        image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        image.save(destination, "JPEG", quality=quality, optimize=True, progressive=True)


def main():
    owner, repo = os.environ.get("GITHUB_REPOSITORY", "YOUR_NAME/YOUR_REPO").split("/", 1)
    base_url = f"https://{owner}.github.io/{repo}"
    files = list_public_folder(CONFIG["drive_folder_url"])
    if IMAGES.exists():
        shutil.rmtree(IMAGES)
    IMAGES.mkdir(parents=True, exist_ok=True)
    manifest = {"images": []}
    for index, (name, file_id) in enumerate(files, start=1):
        query = urllib.parse.urlencode({"id": file_id, "export": "download", "confirm": "t"})
        output_name = f"{index:04d}.jpg"
        convert_image(fetch("https://drive.usercontent.google.com/download?" + query), IMAGES / output_name)
        manifest["images"].append({"url": f"{base_url}/images/{output_name}", "caption": Path(name).stem})
        print(f"同期: {name} -> {output_name}")
    SITE.mkdir(parents=True, exist_ok=True)
    (SITE / "album.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    (SITE / "index.html").write_text(
        "<!doctype html><meta charset='utf-8'><title>Drive Album</title>"
        f"<h1>Drive Album 公開完了</h1><p>写真 {len(files)} 枚</p>"
        f"<p>Unityへ貼るURL：<code>{base_url}</code></p>", encoding="utf-8")
    print(f"Unityへ貼るURL: {base_url}")


if __name__ == "__main__":
    main()
