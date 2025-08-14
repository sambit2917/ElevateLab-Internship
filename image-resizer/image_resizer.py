# image_resizer.py
# Batch image resizer & converter using os + Pillow (PIL)

import os
import argparse
from PIL import Image, ImageOps

# Allowed input image extensions
ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".gif"}

def is_image_file(path):
    _, ext = os.path.splitext(path.lower())
    return ext in ALLOWED_EXTS

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def compute_new_size(orig_w, orig_h, width, height, max_size, keep_aspect, no_upscale):
    """
    Decide target (w, h).
    Priority (while keeping aspect unless explicitly disabled):
      - If width & height given and keep_aspect=False → exact size
      - If width & height given → scale to fit inside the box
      - Else width-only or height-only → scale accordingly
      - Else max_size → longest side becomes max_size
      - Else return original size
    """
    # No size provided → keep original
    if not any([width, height, max_size]):
        return orig_w, orig_h

    if width and height and not keep_aspect:
        # Force exact size
        new_w, new_h = width, height
    else:
        # Keep aspect ratio
        if width and height:
            # Fit inside (width x height) box
            scale = min(width / orig_w, height / orig_h)
        elif width:
            scale = width / orig_w
        elif height:
            scale = height / orig_h
        else:  # max_size only
            # Make the longest side == max_size
            longest = max(orig_w, orig_h)
            scale = max_size / longest

        if no_upscale and scale > 1:
            scale = 1.0

        new_w = max(1, int(round(orig_w * scale)))
        new_h = max(1, int(round(orig_h * scale)))

    return new_w, new_h

def target_format_and_ext(fmt_arg, src_path):
    """
    Decide output format & extension.
    If fmt_arg is None: keep original extension/format.
    """
    if fmt_arg:
        f = fmt_arg.lower()
        if f in ("jpg", "jpeg"):
            return "JPEG", ".jpg"
        elif f == "png":
            return "PNG", ".png"
        elif f == "webp":
            return "WEBP", ".webp"
        elif f == "bmp":
            return "BMP", ".bmp"
        else:
            raise ValueError(f"Unsupported format: {fmt_arg}")
    else:
        # Keep source extension
        _, ext = os.path.splitext(src_path)
        ext_lower = ext.lower()
        # Map extension to Pillow format name
        if ext_lower in (".jpg", ".jpeg"):
            return "JPEG", ext_lower
        elif ext_lower == ".png":
            return "PNG", ext_lower
        elif ext_lower == ".webp":
            return "WEBP", ext_lower
        elif ext_lower == ".bmp":
            return "BMP", ext_lower
        elif ext_lower in (".tif", ".tiff"):
            return "TIFF", ext_lower
        elif ext_lower == ".gif":
            return "GIF", ext_lower
        else:
            # Default safe fallback
            return "PNG", ".png"

def process_image(src_path, dst_path, width, height, max_size, fmt, quality, keep_aspect, no_upscale):
    try:
        with Image.open(src_path) as im:
            # Fix orientation using EXIF
            im = ImageOps.exif_transpose(im)
            orig_w, orig_h = im.size

            # Decide new size
            new_w, new_h = compute_new_size(orig_w, orig_h, width, height, max_size, keep_aspect, no_upscale)

            # Resize if needed
            if (new_w, new_h) != (orig_w, orig_h):
                im = im.resize((new_w, new_h), Image.LANCZOS)

            # Decide target format + extension
            out_format, out_ext = target_format_and_ext(fmt, src_path)

            # Build output path (ensure extension matches)
            base, _ = os.path.splitext(dst_path)
            final_out = base + out_ext
            ensure_dir(os.path.dirname(final_out))

            # JPEG/WebP need RGB (no alpha)
            save_kwargs = {}
            if out_format in ("JPEG", "WEBP"):
                if im.mode in ("RGBA", "LA", "P"):
                    im = im.convert("RGB")
                # Quality (0-100). WebP also uses quality.
                save_kwargs["quality"] = quality
                # smaller file size optimizations
                save_kwargs["optimize"] = True
            elif out_format == "PNG":
                # Optimize PNG size a bit
                save_kwargs["optimize"] = True

            im.save(final_out, format=out_format, **save_kwargs)
            return True, final_out
    except Exception as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(description="Batch Image Resizer & Converter (Pillow)")
    parser.add_argument("-i", "--input", required=True, help="Input folder containing images")
    parser.add_argument("-o", "--output", required=True, help="Output folder to write resized/converted images")

    # Size options
    parser.add_argument("--width", type=int, help="Target width (px)")
    parser.add_argument("--height", type=int, help="Target height (px)")
    parser.add_argument("--max-size", type=int, help="Longest side will be this size (px)")

    # Aspect & upscale
    parser.add_argument("--no-keep-aspect", action="store_false", dest="keep_aspect",
                        help="Do NOT keep aspect ratio (only applies if width & height are both given)")
    parser.add_argument("--no-upscale", action="store_true", help="Never enlarge small images")

    # Conversion options
    parser.add_argument("-f", "--format", choices=["jpg", "jpeg", "png", "webp", "bmp"],
                        help="Convert to this format (default: keep original)")
    parser.add_argument("-q", "--quality", type=int, default=85,
                        help="Quality for JPEG/WEBP (0-100, default=85)")

    args = parser.parse_args()

    in_dir = args.input
    out_dir = args.output
    ensure_dir(out_dir)

    total = 0
    ok = 0
    failed = 0

    # Walk input folder (includes subfolders)
    for root, _, files in os.walk(in_dir):
        for name in files:
            src_path = os.path.join(root, name)
            if not is_image_file(src_path):
                continue

            # Build mirrored relative path under output
            rel_path = os.path.relpath(src_path, in_dir)
            dst_path = os.path.join(out_dir, rel_path)

            total += 1
            success, info = process_image(
                src_path=src_path,
                dst_path=dst_path,
                width=args.width,
                height=args.height,
                max_size=args.max_size,
                fmt=args.format,
                quality=args.quality,
                keep_aspect=args.keep_aspect if args.keep_aspect is not None else True,
                no_upscale=args.no_upscale,
            )

            if success:
                ok += 1
                print(f"[OK]  {src_path}  ➜  {info}")
            else:
                failed += 1
                print(f"[ERR] {src_path}  ➜  {info}")

    print(f"\nDone. Processed: {total}, Success: {ok}, Failed: {failed}")

if __name__ == "__main__":
    main()
