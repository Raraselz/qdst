import argparse
import os
from sys import prefix
from qdst import log, hex_to_rgb
from module import adjust_palette_png
from zcolors import zcolors
import PIL
from PIL import Image
import shutil, glob, subprocess

PREFIX = " <qdst> "

PROFILE_COLORS = [ 
    "#4a809c", "#ae532b", "#ee3738", "#c890c1", "#f79638", "#f0ea2b", "#9fce4a", "#5aba4b",
    "#06a450", "#55bf8f", "#07b2e8", "#1f6ab3", "#2d3c73", "#6b4a9f", "#9355a2", "#ef3791"
]

prompt = ""
prompt_selected_color = -1


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

    # Validate the arguments
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
            new_data.append((255, 0, 255, 0))  # transparent
        else:
            new_data.append(item)
    image.putdata(new_data)
    return image


def main():
    global prompt
    bottom_preview = Image.open(os.path.join(prompt, "background", "bottom.png"))

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
        os.path.join("preview", "user_color_sprite.png"), 
        hex_to_rgb(PROFILE_COLORS[prompt_selected_color]),
        2.1, 1.6
    )
    bottom_preview.paste(user_color_sprite, (0,0), user_color_sprite)

    mario_kart_ds_sprite = Image.open(os.path.join("preview", "mario_kart_ds_sprite.png"))
    bottom_preview.paste(mario_kart_ds_sprite, (0,0), mario_kart_ds_sprite)

    top_preview = Image.open(os.path.join(prompt, "background", "top.png"))
    top_sprite  = Image.open(os.path.join("preview", "top_sprite.png"))
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
