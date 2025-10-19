from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import colorsys

SIZE = (256, 192)

def dominant_color(image_path, k=5):
    image = Image.open(image_path)
    image = image.resize(SIZE)  # bigger SIZE takes longer to process
    pixels = np.array(image).reshape(-1, 3)

    kmeans = KMeans(n_clusters=k, random_state=0).fit(pixels)
    counts = np.bincount(kmeans.labels_)
    dominant = kmeans.cluster_centers_[np.argmax(counts)]
    
    return tuple(map(int, dominant))

def adjust_palette(image_path, target_rgb, saturation_multiplier=1.0, brightness_multiplier=1.0):
    # Load image
    img = Image.open(image_path)

    if img.mode != "P":
        raise ValueError("Image must be in palette (P) mode with ≤16 colors.")

    # Get the current palette
    palette = img.getpalette()[:48]  # Only first 16 colors (16 x 3 = 48)
    new_palette = [255, 0, 255] # SKIP THE FIRST COLOR WHICH IS ALWAYS MAGENTA (BG transparency)

    # Convert target color to HSV
    target_h, target_s, target_v = colorsys.rgb_to_hsv(*[x/255.0 for x in target_rgb])

    for i in range(3, 48, 3):  # Process each RGB triplet from the second slot in the new palete
        r, g, b = palette[i], palette[i+1], palette[i+2]
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)

        # Blend hue towards target hue
        h = target_h

        # Adjust saturation and brightness
        s = min(max(s * saturation_multiplier, 0), 1)
        v = min(max(v * brightness_multiplier, 0), 1)

        # Convert back to RGB
        r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
        new_palette.extend([int(r_new*255), int(g_new*255), int(b_new*255)])
    # Apply the new palette to the image
    img.putpalette(new_palette)

    return img

def adjust_palette_4c(image_path, target_rgb, saturation_multiplier=1.0, brightness_multiplier=1.0):
    # Load image
    img = Image.open(image_path)

    if img.mode != "P":
        raise ValueError("Image must be in palette (P) mode with ≤16 colors.")

    # Get the current palette
    palette = img.getpalette()[:12]  # Only first 4 colors (4 x 3 = 12)
    new_palette = [255, 0, 255] # SKIP THE FIRST COLOR WHICH IS ALWAYS MAGENTA (BG transparency)

    # Convert target color to HSV
    target_h, target_s, target_v = colorsys.rgb_to_hsv(*[x/255.0 for x in target_rgb])

    for i in range(3, 12, 3):  # Process each RGB triplet from the second slot in the new palete
        r, g, b = palette[i], palette[i+1], palette[i+2]
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)

        # Blend hue towards target hue
        h = target_h

        # Adjust saturation and brightness
        s = min(max(s * saturation_multiplier, 0), 1)
        v = min(max(v * brightness_multiplier, 0), 1)

        # Convert back to RGB
        r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
        new_palette.extend([int(r_new*255), int(g_new*255), int(b_new*255)])
    # Apply the new palette to the image
    img.putpalette(new_palette)

    return img

def adjust_palette_png(image_path, target_rgb, saturation_multiplier=1.0, brightness_multiplier=1.0):
    """
    Adjust the hue of all pixels in a PNG (RGB or RGBA) image to match target_rgb hue,
    while scaling saturation and brightness.

    Args:
        image_path (str): Path to PNG image.
        target_rgb (tuple): Target (R, G, B) color to match hue to.
        saturation_multiplier (float): Factor to multiply saturation by.
        brightness_multiplier (float): Factor to multiply brightness by.

    Returns:
        Image: Modified Pillow Image object.
    """
    # Load image
    img = Image.open(image_path).convert("RGBA")
    pixels = img.load()

    # Convert target color to HSV
    target_h, _, _ = colorsys.rgb_to_hsv(*[x / 255.0 for x in target_rgb])

    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 0:  # Skip transparent pixels
                continue

            # Convert to HSV
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

            # Replace hue, adjust saturation and brightness
            h = target_h
            s = min(max(s * saturation_multiplier, 0), 1)
            v = min(max(v * brightness_multiplier, 0), 1)

            # Convert back to RGB
            r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
            pixels[x, y] = (
                int(r_new * 255),
                int(g_new * 255),
                int(b_new * 255),
                a
            )

    return img

if __name__=="__main__":
  # img = adjust_palette("folder.bmp", (255, 0, 0), saturation_multiplier=2, brightness_multiplier=3)
  # img.save("f_ad.bmp")

  log(dominant_color("profile_colors.png"))