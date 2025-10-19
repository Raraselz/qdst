import PIL.Image
from module import *
import PIL
import os, shutil, glob, subprocess, argparse

OVERLAY_BOTTOM_BUBBLE_MACRO = "template/overlays/static/overlay_bottom_bubble_macro.png"
OVERLAY_BOTTOM_BUBBLE       = "template/overlays/static/overlay_bottom_bubble.png"
OVERLAY_TOP_PHOTO           = "template/overlays/static/overlay_top_photo.png"
OVERLAY_BOTTOM_BAR          = "template/overlays/bottom_bar.png"       # these two need
OVERLAY_MOVING              = "template/overlays/moving.png"  #  recoloring

GRF_BOX    = "template/grf/box.bmp"
GRF_BRACE  = "template/grf/brace.bmp"
GRF_FOLDER = "template/grf/folder.bmp"

# top -> address for the 256x192 top image
# bottom -> address for the 256x192 bottom image

def hex_to_rgb(hex: str) -> tuple[int, int, int]:
    global args

    # check for auto top / bottom
    if (hex == "at"):
        return dominant_color(args.top)
    elif (hex == "ab"):
        return dominant_color(args.bottom)
    
    # Remove leading '#' if present
    hex = hex.lstrip('#')

    # Validate length
    if len(hex) != 6:
        raise ValueError(f"Invalid hex color: '{hex}'. Expected format: RRGGBB")

    # Convert to integer tuple
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)

    return (r, g, b)

def generate_and_show_preview():
    pass

def convert_to_4bit_bitmap(path: str, op_path: str) -> bool:
    # Check if 'magick' is installed and in PATH
    if shutil.which("magick") is None:
        print("❌ ImageMagick (magick) is not installed or not found in PATH.")
        return False

    output_path = op_path  # You can modify this or make it a parameter

    try:
        result = subprocess.run(
            ['magick', path, '-depth', '4', f'BMP3:{output_path}'],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Conversion successful.")
        print(f"STDOUT:\n{result.stdout}")
        return True

    except subprocess.CalledProcessError as e:
        print("❌ Failed to run bit depth conversion with magick!")
        print(f"Return code: {e.returncode}")
        print(f"STDERR:\n{e.stderr}")
        return False

    except FileNotFoundError:
        print("❌ 'magick' command not found. Make sure ImageMagick is installed and in PATH.")
        return False
 
def qdst(theme_name: str, top: str, bottom: str, color: tuple[int, int, int], lm: float = 1.0, sm: float = 1.0, lmo: float = 1.0, smo: float = 1.0, bgm: str = None):

    # create directory with team_name
    os.makedirs(os.path.join(theme_name, "background"), exist_ok=True)
    os.makedirs(os.path.join(theme_name, "grf"), exist_ok=True)
    os.makedirs(os.path.join(theme_name, "battery"), exist_ok=True)
    os.makedirs(os.path.join(theme_name, "sound"), exist_ok=True)
    os.makedirs(os.path.join(theme_name, "ui"), exist_ok=True)
    os.makedirs(os.path.join(theme_name, "volume"), exist_ok=True)
    shutil.copy(top, os.path.join(theme_name, "background", "top.png"))
    
    bottom_base = PIL.Image.open(bottom).convert("RGBA")
    top = PIL.Image.open(top).convert("RGBA")

    ### BACKGROUND

    # Load the static overlays into a PIL.Image
    bottom_bubble_overlay = PIL.Image.open(OVERLAY_BOTTOM_BUBBLE).convert("RGBA")
    bottom_bubble_macro_overlay = PIL.Image.open(OVERLAY_BOTTOM_BUBBLE_MACRO).convert("RGBA")
    top_photo_overlay = PIL.Image.open(OVERLAY_TOP_PHOTO).convert("RGBA")

    # adjust_pallete_png() already returns a PIL.Image so we can adjust the colors on the fly
    bottom_bar_overlay = adjust_palette_png(OVERLAY_BOTTOM_BAR, color, smo, lmo)
    bottom_moving_overlay = adjust_palette_png(OVERLAY_MOVING, color, smo, lmo)

    # now we get to combining these elements

    top_photo = PIL.Image.alpha_composite(top, top_photo_overlay) # looks kinda ugly in most cases, I personally don't have any cover art for my games

    bottom_with_bar = PIL.Image.alpha_composite(bottom_base, bottom_bar_overlay)
    bottom_moving = PIL.Image.alpha_composite(bottom_with_bar, bottom_moving_overlay)
    bottom_bubble = PIL.Image.alpha_composite(bottom_with_bar, bottom_bubble_overlay)
    bottom_bubble_macro = PIL.Image.alpha_composite(bottom_with_bar, bottom_bubble_macro_overlay)

    # we will now save all these in theme_name\background

    bottom_with_bar.save(os.path.join(theme_name, "background", "bottom.png"))
    bottom_moving.save(os.path.join(theme_name, "background", "bottom_moving.png"))
    bottom_bubble.save(os.path.join(theme_name, "background", "bottom_bubble.png"))
    bottom_bubble_macro.save(os.path.join(theme_name, "background", "bottom_bubble_macro.png"))

    ### GRF (BITMAPS)

    box = adjust_palette(GRF_BOX, color, sm, lm)
    brace = adjust_palette_4c(GRF_BRACE, color, sm, lm)
    folder = adjust_palette(GRF_FOLDER, color, sm, lm)

    # save these too

    box.save(theme_name + "/grf/box_.bmp")
    brace.save(theme_name + "/grf/brace_.bmp")
    folder.save(theme_name + "/grf/folder_.bmp")

    # Convert them to compatible 4bit bitmaps

    convert_to_4bit_bitmap(theme_name + "/grf/box_.bmp", theme_name + "/grf/box.bmp")
    convert_to_4bit_bitmap(theme_name + "/grf/brace_.bmp", theme_name + "/grf/brace.bmp")
    convert_to_4bit_bitmap(theme_name + "/grf/folder_.bmp", theme_name + "/grf/folder.bmp")


    # copy the rest of the static grf elements
    for file in glob.glob("template/grf/static/*.bmp"):
        shutil.copy(file, os.path.join(theme_name, "grf"))
    
    # copy battery, ui, quickmenu and volume folders
    shutil.copytree("template/battery", os.path.join(theme_name, "battery"), dirs_exist_ok=True)
    shutil.copytree("template/ui", os.path.join(theme_name, "ui"), dirs_exist_ok=True)
    shutil.copytree("template/quickmenu", os.path.join(theme_name, "quickmenu"), dirs_exist_ok=True)
    shutil.copytree("template/volume", os.path.join(theme_name, "volume"), dirs_exist_ok=True)

    # Finally, copy the bgm if existent and the theme.ini file
    shutil.copy("template/theme.ini", os.path.join(theme_name, "theme.ini"))

    if bgm:
        pass


if __name__ == "__main__":
    #qdst("TEST Theme", "test/top.png", "test/bottom.png", (255, 0, 0), 2, 1.9, 2, 1.5) # test run

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--top", help="path to the top 256x192 png image", required=True)
    parser.add_argument("-b", "--bottom", help="path to the bottom 256x192 png image", required=True)
    parser.add_argument("-c", "--color", help="paint color (eg. #FFFFFF) / at / ab (auto top/bottom)", required=True)
    parser.add_argument('--lm', help="luminosity multiplier: float", type=float)
    parser.add_argument('--sm', help="saturation multiplier: float", type=float)
    parser.add_argument('--lmo', help="saturation multiplier for bottom background elements: float", type=float)
    parser.add_argument('--smo', help="saturation multiplier for bottom background elements: float", type=float)
    parser.add_argument('--bgm', help='path to bgm (16bit mono)')
    parser.add_argument("name", help="name of your theme")
    args = parser.parse_args()

    qdst(args.name, args.top, args.bottom, hex_to_rgb(args.color), args.lm, args.sm, args.lmo, args.smo, args.bgm)