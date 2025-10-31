import argparse
import os
from sys import prefix
import sys
from zcolors import zcolors
import PIL
from PIL import Image
import shutil, glob, subprocess, colorsys

PREFIX = " <qdst> "

PROFILE_COLORS = [ 
    "#4a809c", "#ae532b", "#ee3738", "#c890c1", "#f79638", "#f0ea2b", "#9fce4a", "#5aba4b",
    "#06a450", "#55bf8f", "#07b2e8", "#1f6ab3", "#2d3c73", "#6b4a9f", "#9355a2", "#ef3791"
]

prompt = ""
prompt_selected_color = -1

# Determine base directory of the running script or executable
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# reused from qdst.py
def hex_to_rgb(hex: str) -> tuple[int, int, int]:
    global args

    if (hex == "at"):
        return "at"
    elif (hex == "ab"):
        return "ab"
    
    hex = hex.lstrip('#')

    if len(hex) != 6:
        raise ValueError(f"Invalid hex color: '{hex}'. Expected format: RRGGBB")

    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)

    return (r, g, b)


# reused from module.py
def adjust_palette_png(image_path, target_rgb, saturation_multiplier=1.0, brightness_multiplier=1.0):
    img = Image.open(image_path).convert("RGBA")
    pixels = img.load()
    target_h, _, _ = colorsys.rgb_to_hsv(*[x / 255.0 for x in target_rgb])

    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            h = target_h
            s = min(max(s * saturation_multiplier, 0), 1)
            v = min(max(v * brightness_multiplier, 0), 1)
            r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
            pixels[x, y] = (int(r_new * 255), int(g_new * 255), int(b_new * 255), a)

    return img


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate preview images from a given prompt folder and color profile."
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="Path to the prompt directory (must contain 'background' and 'grf' subfolders)."
    )
    parser.add_argument(
        "-c", "--profile-color",
        type=int,
        default=0,
        help=f"Index of the profile color (0-{len(PROFILE_COLORS)-1}). Default: 0"
    )
    args = parser.parse_args()

    if not os.path.isdir(args.prompt):
        parser.error(f"Prompt path '{args.prompt}' does not exist or is not a directory.")
    if not (0 <= args.profile_color < len(PROFILE_COLORS)):
        parser.error(f"Profile color index must be between 0 and {len(PROFILE_COLORS)-1}.")
    return args


def transparency(image: Image.Image):
    image = image.convert("RGBA")
    datas = image.getdata()
    new_data = []
    for item in datas:
        if item[0] == 255 and item[1] == 0 and item[2] == 255:
            new_data.append((255, 0, 255, 0))
        else:
            new_data.append(item)
    image.putdata(new_data)
    return image


def main():
    global prompt
    # Use BASE_DIR for preview assets
    bottom_preview = Image.open(os.path.join(prompt, "background", "bottom.png")).convert("RGBA")
    box_full  = Image.open(os.path.join(prompt, "grf", "box.bmp"))
    
    box_empty = box_full.crop((7, 68, 7 + 50, 68 + 60))
    box_game  = box_full.crop((7, 4, 7 + 50, 4 + 60))

    box_empty = transparency(box_empty)
    box_game  = transparency(box_game)

    bottom_preview.paste(box_game, (104-1, 90-1), box_game)
    bottom_preview.paste(box_empty, (168, 89-1), box_empty)
    bottom_preview.paste(box_empty, (226, 89-1), box_empty)

    folder_full    = Image.open(os.path.join(prompt, "grf", "folder.bmp"))
    folder_cropped = folder_full.crop((9, 14, 9 + 46, 14 + 42))
    folder         = transparency(folder_cropped)
    bottom_preview.paste(folder, (40, 96-1), folder)

    brace_full    = Image.open(os.path.join(prompt, "grf", "brace.bmp"))
    brace_cropped = brace_full.crop((1, 1, 1+13, 1+78))
    brace         = transparency(brace_cropped)
    bottom_preview.paste(brace, (15-1, 82-1), brace)

    user_color_sprite = adjust_palette_png(
        os.path.join(BASE_DIR, "preview", "user_color_sprite.png"), 
        hex_to_rgb(PROFILE_COLORS[prompt_selected_color]),
        2.1, 1.6
    )
    bottom_preview.paste(user_color_sprite, (0,0), user_color_sprite)

    mario_kart_ds_sprite = Image.open(os.path.join(BASE_DIR, "preview", "mario_kart_ds_sprite.png"))
    bottom_preview.paste(mario_kart_ds_sprite, (0,0), mario_kart_ds_sprite)

    top_preview = Image.open(os.path.join(prompt, "background", "top.png")).convert("RGBA")
    top_sprite  = Image.open(os.path.join(BASE_DIR, "preview", "top_sprite.png"))
    top_preview.paste(top_sprite, (0,0), top_sprite)
    
    final_preview = Image.new(mode="RGBA", size=(256, 384))
    final_preview.paste(top_preview, (0,0), top_preview)
    final_preview.paste(bottom_preview, (0,192), top_preview)
    final_preview.save(os.path.join(prompt, "preview.png"))
    final_preview.show()


if __name__ == "__main__":
    args = parse_args()
    prompt = args.prompt
    prompt_selected_color = args.profile_color
    main()
