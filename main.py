from encodings.punycode import T
import PIL.Image
from module import *
import PIL
import os, shutil, glob

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
    pass

def generate_and_show_preview():
    pass
 
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

    box.save(theme_name + "/grf/box_.bmp", bits=4)
    brace.save(theme_name + "/grf/brace_.bmp", bits=4)
    folder.save(theme_name + "/grf/folder_.bmp", bits=4)

    images = ["box_.bmp", "brace_.bmp", "folder_.bmp"]
    grf_path = os.path.join(theme_name, "grf")

    for filename in images:
        img_path = os.path.join(grf_path, filename)
        img = Image.open(img_path)

        # Step 1: Convert to 16-color palette
        img_16 = img.convert("P", palette=Image.ADAPTIVE, colors=16)

        # Step 2: Build a new palette array of exactly 16 colors
        palette = img_16.getpalette()[:16*3]  # get first 16 RGB triplets
        # Fill remaining colors to make 256-length palette (required by BMP)
        palette += [0]*(256*3 - len(palette))

        img_16.putpalette(palette)

        # Step 3: Save manually as 4-bit BMP
        new_filename = filename.replace("_", "")
        save_path = os.path.join(grf_path, new_filename)
        img_16.save(save_path, format="BMP", bits=4)

        print(f"Saved {save_path} as true 4-bit BMP")
        
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
    qdst("TEST Theme", "test/top.png", "test/bottom.png", (255, 0, 0), 2, 1.9, 2, 1.5) # test run