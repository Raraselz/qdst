
<div align="center">

  <h1 align="center">qdst - Quick DSi Theme Maker</h3>

  <p align="center">
A simple yet efficient command-line utility for quickly creating <b>custom Nintendo DSi themes</b> for use with <b>TWiLight Menu++</b>.
    <br />
    <a href="https://github.com/raraselz/qdst/issues/new?labels=bug&template=bug_report.md">Report Bug</a>
    &middot;
    <a href="https://github.com/raraselz/qdst/issues/new?labels=enhancement&template=feature_request.md">Request Feature</a>
    &middot;
    <a href="https://github.com/raraselz/qdst/blob/main/CHANGELOG.md">Changelog</a>
  </p>
</div>


## 🧭 Overview

qdst helps you build personalized DSi themes in minutes without the need for manual bitmap editing.\
It automates the process of combining assets like background images, icons, and music into a ready-to-use theme folder.

## ⚙️ Usage

### Prerequisites

**Windows**

```sh
winget install ImageMagick.Q8
```

**macOS**
```sh
brew install imagemagick
```

**Linux**

Idk but I know you're smart if you use it so figure it out :))

***ImageMagick*** is required for conversion to 4-bit bitmaps compatible with TWiLight Menu++

### Example Usage

```sh
qdst -t "TOP.png" -b "BOTTOM.png" -c "#FF00FF" --lm 2 --sm 2 --lmo 2 --smo 2 --bgm "BGM.wav" --jp "My Cool Theme"
``` 

### Parameters

| Flag    | Description                                               |
|---------|-----------------------------------------------------------|
| `-t`    | path to 256x192 top PNG                                   |
| `-b`    | path to 256x192 bottom PNG                                |
| `-c`    | HEX for accent color / ab / at (auto-detect top/bottom)   |
| `--lm`  | luminosity multiplier for folders, boxes and brace        |
| `--sm`  | saturation multiplier for folders, boxes and brace        |
| `--lmo` | luminosity multiplier for bottom overlays                 |
| `--smo` | saturation multiplier for bottom overlays                 |
| `--bgm` | optional: path to 16-bit mono WAV bgm file                |
| `--jp`  | optional: have the START text in japanese (for weebs ^v^) |

### Quick Start

The easiest way to get going is to download the latest release from [Releases](https://github.com/Raraselz/qdst/releases). \

1. Unzip the archive to a known location
2. Add that location to path (for ease of use) (don't know how? see [this guide](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/))
3. You're set! In the place where you have saved the top and bottom images, right click and *Open in Terminal*.
4. Run `qdst` with your desired settings.

💡 **TIP** | After your theme is done, you can easily preview it using:

```sh
    qdsp -c 1-15 "Theme Name"
```

`-c` represents the profile color index (see [color-indexes.png](https://github.com/Raraselz/qdst/blob/main/color-indexes.png)) try picking the closest one to your accent color

## ⚠️ Things You Should Know

* The release method is somewhat inefficient (and slow) due to PyInstaller and the nature of Python executables. If you’re comfortable with Python, working directly with the source code is recommended.
* **BGM flag does nothing for now** — I plan to implement proper audio conversion via ffmpeg first.
* Currently, your theme’s colors are mostly limited by the profile colors available in the DSi system settings. (if you want it to look good)
* You still need to crop the backgrounds yourself. **Paint** works fine, but if you have **Photoshop / GIMP**, I highly recommend using it instead.

## 🎨 Purpose

I’ve noticed a lack of high-quality TWiLight Menu++ DSi themes — most come from the [twlmenu-extras GitHub repository](https://github.com/DS-Homebrew/twlmenu-extras), but options are still limited. \
Creating a theme from scratch is tricky: designing icons, folder frames, and other bitmaps can be time-consuming and unintuitive.

That’s where **qdst** comes in.

Building upon the work of BlakCake and DVDo and their beautiful “Relaxing Space” theme, qdst provides a streamlined way to:
* Recolor existing assets to your liking
* Choose custom top / bottom backgrounds
* Add your own menu music

With these simple adjustments, you can create your own (mostly) custom theme in just a few minutes.

## 🧰 Credits

* BlakCake and DVDo — Original theme assets (Relaxing Space)
* TWiLight Menu++ Team — For enabling theme customization support
* You, the user — for making your DSi feel truly yours

## 📜 License

See [LICENSE.txt](https://github.com/Raraselz/qdst/blob/main/LICENSE)