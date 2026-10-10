---
name: dev-icons
description: Tech and brand logo icons (React, TypeScript, Python, Docker, Cloudflare, databases, AI tools and more) as ready-made rounded tiles in dark, light and brand-colour themes, with scripts to search them, combine them into tech-stack banners, export SVG/PNG files and make animated HTML. Use whenever the user wants logos or icons for technologies, frameworks, languages, tools or companies, for example a "tech stack" or "built with" section in a README, icons on slides or in a document, a skills section on a portfolio or CV, a website footer, or an animated logo intro for a video. Use it instead of drawing logos by hand or linking to external icon services.
---

# Dev Icons

Pre-built logo tiles for about 190 developer tools, plus four Python scripts. Every logo
comes from [Simple Icons](https://simpleicons.org) in its official brand colour.

All paths below are relative to this skill's folder. Run scripts with `python3`
(`python` on Windows). They only need the standard library; PNG strips and PNGs at custom
sizes also need Pillow (`pip install pillow`).

## What's in the skill

| Path | Contents |
|---|---|
| `icons/<theme>/<id>.svg` | 256×256 SVG tile per icon |
| `png/<theme>/128/<id>.png`, `png/<theme>/512/<id>.png` | Pre-rendered PNG tiles |
| `manifest.json` | Every icon: `id`, `name`, `category`, `aliases`, brand `hex`, `license`, `guidelines` |
| `scripts/` | `find.py`, `compose.py`, `export.py`, `animate.py` |

**Themes**
- `dark`: dark tile with the logo in its brand colour. The default, and the skillicons look.
- `light`: light cream tile with the logo in its brand colour.
- `brand`: tile filled with the brand colour and a white or black logo.

Choose the theme that contrasts with where the icons will appear: `dark` on light
pages and GitHub READMEs, `light` on dark slides, `brand` for bold, colourful layouts.
If you don't know the background, use `dark`.

## Workflow

### 1. Always check icon names first

Users type names loosely ("postgres", "k8s", "Next.js", "node"). Resolve them before
doing anything else:

```bash
python3 scripts/find.py react k8s "next.js" pg      # look up specific names
python3 scripts/find.py --list                      # everything available
python3 scripts/find.py --category database         # one category
python3 scripts/find.py --categories                # category names and counts
```

Any script given an unknown name stops with an error and a "did you mean" suggestion.
If an icon really isn't in the set, tell the user which ones are missing and carry on
with the rest. **Never draw, trace or invent a brand logo** to fill the gap, and never
substitute a different brand's logo.

Some well-known brands are deliberately absent because their owners had them removed from
Simple Icons: AWS, Azure, DynamoDB, VS Code, Windows, C#, PowerShell, Playwright, Heroku,
Slack and OpenAI. Say so plainly and suggest the user get them from the brand's official
press or media kit.

### 2. Pick the script for the job

| The user wants | Script | Output |
|---|---|---|
| One image with several logos (README stack banner, "built with" row, skills grid) | `compose.py` | `.svg` or `.png` |
| Individual logo files (slides, docs, website assets) | `export.py` | `.svg` and/or `.png` per icon |
| Logos that animate in (video intro, landing page, demo) | `animate.py` | one self-contained `.html` |

Write output into the user's project or working directory, not into this skill's folder.

### compose.py: stack banners and grids

```bash
python3 scripts/compose.py react,ts,nodejs,postgres,docker -o assets/stack.svg
python3 scripts/compose.py html css js react vue svelte --perline 3 --size 96 --theme light -o grid.png
```

Options: `--theme dark|light|brand` (default dark), `--size` px per icon (default 48),
`--gap` px (default size/6), `--perline` icons per row before wrapping (default 15).
The output type comes from the `-o` extension.

For a **GitHub README**, write an SVG into the repo and reference it with a relative path.
GitHub renders committed SVGs:

```markdown
![Tech stack: React, TypeScript, Node.js, PostgreSQL, Docker](assets/stack.svg)
```

### export.py: individual files

```bash
python3 scripts/export.py react,ts,nodejs -o icons                  # dark, 512px PNG
python3 scripts/export.py docker --theme light --format svg -o icons
python3 scripts/export.py react,vue --size 256 --format both -o icons
python3 scripts/export.py react,vue --theme all -o icons            # icons/dark/, icons/light/, icons/brand/
```

128px and 512px are copied as they are; other sizes are resized from 512px (this needs
Pillow, and without it the script falls back to the nearest size and prints a warning).
Above 512px a PNG goes soft, so use SVG for anything that large.

### animate.py: animated HTML

```bash
python3 scripts/animate.py react,ts,nodejs,postgres -o stack.html
python3 scripts/animate.py react ts nodejs --style wave --size 140 --title "My stack" -o intro.html
```

Styles:
- `pop`: icons pop in one by one (the default).
- `slide`: icons slide up and fade in.
- `float`: icons pop in, then bob gently.
- `wave`: a continuous ripple.

Other options: `--theme`, `--size` (default 120), `--perline` (default 8), `--duration`,
`--stagger`, `--bg` (any CSS colour, or `transparent`) and `--title`.
The page fills the browser window with the icons centred, and clicking it replays the
animation. To use it in a **video**, tell the user to open the file in a browser and
screen-record it, or to load it as an HTML/web layer in their video tool.

## Format guide

| Destination | Use |
|---|---|
| GitHub README, website, Markdown | SVG (sharp at every size, small files) |
| PowerPoint, Keynote, Google Slides | 512px PNG |
| Word, Google Docs, PDF | 128px PNG for inline, 512px for large |
| Video editors | 512px PNG, or `animate.py` |
| Another skill building .pptx/.docx/.pdf | PNG from `export.py`, then insert the file |

## Licences and trademarks

Licences vary by logo. Each icon's `license` field in `manifest.json` holds its licence
(`find.py` shows it), and `null` means Simple Icons has no data, which does **not** mean the
logo is free to use. When an icon the user picked has a restrictive licence, mention it
once: `*-NC-*` licences (Vue, Sass, Tauri) are non-commercial only, `*-ND-*` (Tauri)
forbids modified versions, `CC-BY-*` licences require credit, `*-SA-*` licences require
sharing under the same licence, and `custom` (webpack, Fedora) means the brand's own terms
apply, so point to its `guidelines` link. If the user's project is
commercial, flag non-commercial logos before using them. The `guidelines` field links to
the brand's own usage rules where one exists.

The logos are trademarks of their owners. Use them only to refer to the product or
company (for example, "built with React"), never in a way that suggests the owner
endorses the user's project. Don't recolour or distort the logos beyond the three
built-in themes. If the user asks to use a logo as their own product's logo or
branding, point out that it's someone else's trademark.
