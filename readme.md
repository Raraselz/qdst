
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