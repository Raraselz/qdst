from sys import prefix
import PIL.Image
from module import *
from zcolors import zcolors
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

PREFIX = " <qdst> "

def log(content: str = "", end: str = None):
    global PREFIX

    if content == "":
        print()
        return

    if end != None:
        print(PREFIX + content, end=end)
        return

    print(PREFIX + content)

def hex_to_rgb(hex: str) -> tuple[int, int, int]:
    global args

    # check for auto top / bottom
    if (hex == "at"):
        return "at"         # <- in these cases we leave the dominant color processing to the main qdst() function for proper error handling
    elif (hex == "ab"):
        return "ab"
    
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

def convert_to_4bit_bitmap(path: str, op_path: str, verbose: bool = False) -> bool:
    # Check if 'magick' is installed and in PATH
    if shutil.which("magick") is None:
        log("❌ ImageMagick (magick) is not installed or not found in PATH.")
        return False

    output_path = op_path  # You can modify this or make it a parameter

    try:
        result = subprocess.run(
            ['magick', path, '-verbose', '-depth', '4', f'BMP3:{output_path}'],
            check=True,
            capture_output=True,
            text=True
        )

        output_string = zcolors.FG_LIGHTGREEN + "Conversion successful." + zcolors.X
        if verbose: output_string += zcolors.FG_DARKGREY + " "+ result.stdout.strip() + zcolors.X

        log(output_string)
        return True

    except subprocess.CalledProcessError as e:
        log("Failed to run bit depth conversion with magick!")
        log(f"Return code: {e.returncode}")
        log(f"STDERR:\n{e.stderr}")
        return False

    except FileNotFoundError:
        log("❌ 'magick' command not found. Make sure ImageMagick is installed and in PATH.")
        return False
    
def abort():
    global args # have access to global args variable
    shutil.rmtree(args.name)

# top -> address for the 256x192 top image
# bottom -> address for the 256x192 bottom image

### RETURN CODES
# -1 -> invalid size for top / bottom
# -5 -> invalid top / bottom image path
# -3 -> failed to load static overlays, reinstall the program
# -4 -> failed to load overlays, reinstall the program
# -6 -> failed to load grf
# -7 -> failed to copy static grf
# -8 -> failed to copy static template elements

def qdst(theme_name: str, top_path: str, bottom: str, color: tuple[int, int, int], 
         lm: float = 1.0, sm: float = 1.0, lmo: float = 1.0, smo: float = 1.0, 
         bgm: str = None, jp: bool = False):
   
    # create directory with team_name

    log(zcolors.FG_WHITE + "Creating folder structure..." + zcolors.X)

    os.makedirs(os.path.join(theme_name, "background"), exist_ok=True)
    os.makedirs(os.path.join(theme_name, "grf"), exist_ok=True)
    os.makedirs(os.path.join(theme_name, "battery"), exist_ok=True)
    os.makedirs(os.path.join(theme_name, "sound"), exist_ok=True)
    os.makedirs(os.path.join(theme_name, "ui"), exist_ok=True)
    os.makedirs(os.path.join(theme_name, "volume"), exist_ok=True)
    
    log(zcolors.FG_WHITE + "Loading top / bottom pictures..." + zcolors.X)

    try:
        bottom_base = PIL.Image.open(bottom).convert("RGBA")
        top = PIL.Image.open(top_path).convert("RGBA")
    except:
        log(zcolors.FG_LIGHTRED + "Failed to load given top / bottom images. Aborting..." + zcolors.X); abort()
        return -5 

    # SIZE VALIDATION

    if bottom_base.size == (256, 192) and top.size == (256, 192):
        log(zcolors.FG_LIGHTGREEN + "Size validation succeeded!" + zcolors.X)
    else:
        log(zcolors.FG_LIGHTRED + "Size of given pictures is not 256x192. Aborting..." + zcolors.X); abort()
        return -1
    
    shutil.copy(top_path, os.path.join(theme_name, "background", "top.png"))

    ### AUTO - COLOR CASE

    if color == "ab":
        color = dominant_color(bottom)    # <- and we process them here after we've made sure the files are valid and existent
    if color == "at":
        color = dominant_color(top_path)

    ### BACKGROUND

    # Load the static overlays into a PIL.Image
    try:
        bottom_bubble_overlay = PIL.Image.open(OVERLAY_BOTTOM_BUBBLE).convert("RGBA")
        bottom_bubble_macro_overlay = PIL.Image.open(OVERLAY_BOTTOM_BUBBLE_MACRO).convert("RGBA")
        top_photo_overlay = PIL.Image.open(OVERLAY_TOP_PHOTO).convert("RGBA")
        log(zcolors.FG_WHITE + "Loaded OVERLAY_BOTTOM_BUBBLE, OVERLAY_BOTTOM_BUBBLE_MACRO, OVERLAY_TOP_PHOTO" + zcolors.X)
    except:
        log(zcolors.FG_LIGHTRED + "Failed to load static overlays from template/overlays/static! Please perform a clean reinstall and try again. Aborting..." + zcolors.X); abort()
        return -3

    try:
        bottom_bar_overlay = adjust_palette_png(OVERLAY_BOTTOM_BAR, color, smo, lmo)
        bottom_moving_overlay = adjust_palette_png(OVERLAY_MOVING, color, smo, lmo)
    except:
        log(zcolors.FG_LIGHTRED + "Failed to load overlays from template/overlays! Please perform a clean reinstall and try again. Aborting..." + zcolors.X); abort()
        return -4

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
    log(zcolors.FG_WHITE + "Combined bottom base with all recolored elements" + zcolors.X)

    ### GRF (BITMAPS)

    try:
        box = adjust_palette(GRF_BOX, color, sm, lm)
        brace = adjust_palette_4c(GRF_BRACE, color, sm, lm)
        folder = adjust_palette(GRF_FOLDER, color, sm, lm)
        log(zcolors.FG_WHITE + "Loaded and recolored graphic bitmaps in 8-bit depth" + zcolors.X)
    except:
        log(zcolors.FG_LIGHTRED + "Failed to load/recolor graphic bitmaps from template/grf! Please perform a clean reinstall and try again. Aborting..." + zcolors.X); abort()
        return -6

    # save these too

    box.save(theme_name + "/grf/box_.bmp")
    brace.save(theme_name + "/grf/brace_.bmp")
    folder.save(theme_name + "/grf/folder_.bmp")

    # Convert them to compatible 4bit bitmaps

    log(zcolors.FG_WHITE + "Starting conversion to compatible 4-bit bitmaps" + zcolors.X)
    convert_to_4bit_bitmap(theme_name + "/grf/box_.bmp", theme_name + "/grf/box.bmp", True)
    convert_to_4bit_bitmap(theme_name + "/grf/brace_.bmp", theme_name + "/grf/brace.bmp", True)
    convert_to_4bit_bitmap(theme_name + "/grf/folder_.bmp", theme_name + "/grf/folder.bmp", True)


    # copy the rest of the static grf elements, except start_text
    try:
        for file in glob.glob("template/grf/static/*.bmp"):
            filename = os.path.basename(file)
            if filename in ("start_text.bmp", "start_text_jp.bmp"):
                continue  # skip these two files

            shutil.copy(file, os.path.join(theme_name, "grf"))
        log(zcolors.FG_WHITE + "Copied all static bitmaps to /" + theme_name + zcolors.X)

    except Exception as e:
        log(zcolors.FG_LIGHTRED + 
            "Failed to copy static graphic bitmaps from template/grf/static! "
            "Please perform a clean reinstall and try again. Aborting..." + 
            zcolors.X)
        abort()
        return -7
    
    # depending on the --jp flag we wil copy the correct start_text.bmp

    if jp:
        shutil.copy(os.path.join("template", "static", "start_text_jp.bmp"), os.path.join(theme_name, "grf", "start_text.bmp"))
    else:
        shutil.copy(os.path.join("template", "static", "start_text.bmp"), os.path.join(theme_name, "grf"))        
    
    # copy battery, ui, quickmenu and volume folders
    try:
        shutil.copytree("template/battery", os.path.join(theme_name, "battery"), dirs_exist_ok=True)
        shutil.copytree("template/ui", os.path.join(theme_name, "ui"), dirs_exist_ok=True)
        shutil.copytree("template/quickmenu", os.path.join(theme_name, "quickmenu"), dirs_exist_ok=True)
        shutil.copytree("template/volume", os.path.join(theme_name, "volume"), dirs_exist_ok=True)
        log(zcolors.FG_WHITE + "Copied template/ battery, ui, quickmenu and volume elements to " + "/" + theme_name + zcolors.X)
    except:
        log(zcolors.FG_LIGHTRED + "Failed to copy template/ battery, ui, quickmenu and volume elements! Please perform a clean reinstall and try again. Aborting..." + zcolors.X); abort()
        return -8

    # Finally, copy the bgm if existent and the theme.ini file
    try: 
        shutil.copy("template/theme.ini", os.path.join(theme_name, "theme.ini"))
        log(zcolors.FG_WHITE + "Copied theme.ini")
    except:
        log(zcolors.FG_LIGHTRED + "Failed to copy theme.ini! Please perform a clean reinstall and try again. Aborting..." + zcolors.X); abort()
        return -9      

    if bgm:
        pass

    return 0

# ERROR CODES
# -2 -> invalid color

if __name__ == "__main__":
    print(zcolors.FG_LIGHTMAGENTA + "qdst | Quick DSi Theme Maker | unknown GitHub version | Raraselz" + zcolors.X)
    print(f"Check out {zcolors.FG_LIGHTCYAN}https://github.com/Raraselz/qdst{zcolors.X}")
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--top", help="path to the top 256x192 png image", required=True)
    parser.add_argument("-b", "--bottom", help="path to the bottom 256x192 png image", required=True)
    parser.add_argument("-c", "--color", help="paint color (eg. #FFFFFF) / at / ab (auto top/bottom)", required=True)
    parser.add_argument('--lm', help="luminosity multiplier: float", type=float)
    parser.add_argument('--sm', help="saturation multiplier: float", type=float)
    parser.add_argument('--lmo', help="saturation multiplier for bottom background elements: float", type=float)
    parser.add_argument('--smo', help="saturation multiplier for bottom background elements: float", type=float)
    parser.add_argument('--bgm', help='path to bgm (16bit mono)')
    parser.add_argument('--jp', action="store_true", help="Simple way to turn START text into japanese! (for weebs ^-^)")
    parser.add_argument("name", help="name of your theme")
    args = parser.parse_args()

    try: color_rgb = hex_to_rgb(args.color)
    except: log(zcolors.FG_LIGHTRED + "Invalid color! Aborting..." + zcolors.X); exit(-2)

    exit(qdst(args.name, args.top, args.bottom, color_rgb, args.lm, args.sm, args.lmo, args.smo, args.bgm, args.jp))