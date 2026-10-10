# dev-icons

A skill that gives Claude about 190 tech and brand logos (languages, frameworks, cloud,
databases, DevOps, AI tools and more) as ready-made tiles, plus scripts to turn them into
tech-stack banners, slide-ready PNGs and animated intros.

![A sample of the icons](gallery/preview.svg)

**[See all 189 icons in every theme →](gallery/README.md)**

## What you can ask Claude

Once the skill is installed, ask in plain language. Claude looks up the icons, runs the
right script and gives you the file.

- "Make a tech stack banner for my README: React, TypeScript, Node and Postgres."
- "I need Docker, Kubernetes and Terraform logos as PNGs for my slides."
- "Create an animated intro showing Python, FastAPI and Redis for my video."
- "Add a skills section with my stack to my portfolio site."

## Features

- **3 themes:** `dark` (the familiar dark tile), `light`, and `brand` (filled with the brand colour).
  Logo colours switch automatically when they'd be hard to see, such as black logos on dark tiles.
- **Banners and grids:** any set of icons in one SVG or PNG, with your choice of size, spacing and row length.
- **Single files:** SVG, or PNG at any size, ready for slides, documents and websites.
- **Animated HTML:** 4 styles (pop, slide, float, wave), ready to screen-record into a video.
- **Forgiving names:** `k8s`, `postgres`, `Next.js` and `node` all work, and typos get a "did you mean".
- **Works offline:** everything is inside the skill. Nothing is downloaded when it runs.
- **Licence-aware:** Claude warns you when a logo has a restrictive licence (for example, non-commercial only).

## Install

### claude.ai

You need **Code execution and file creation** turned on in Settings.

1. Build the skill zip from a copy of this repo (you need Python 3):
   ```bash
   git clone https://github.com/Hirusha-Nikson/pro-icons-skill.git
   cd pro-icons-skill
   python -c "import shutil; shutil.make_archive('dev-icons', 'zip', root_dir='skills', base_dir='dev-icons')"
   ```
2. In claude.ai, go to **Settings → Capabilities → Skills**, click **Upload skill** and
   choose `dev-icons.zip`.
3. Make sure the skill is switched on, then start a new chat.

### Claude Code

Copy the skill folder into your personal skills folder:

```bash
git clone https://github.com/Hirusha-Nikson/pro-icons-skill.git
mkdir -p ~/.claude/skills
cp -r pro-icons-skill/skills/dev-icons ~/.claude/skills/
```

On Windows (PowerShell):

```powershell
git clone https://github.com/Hirusha-Nikson/pro-icons-skill.git
New-Item -ItemType Directory -Force "$HOME\.claude\skills"
Copy-Item -Recurse pro-icons-skill\skills\dev-icons "$HOME\.claude\skills\"
```

To share it with a team, put it in a project's `.claude/skills/` folder instead. Start a
new Claude Code session afterwards so the skill is loaded.

## Using the scripts yourself

The scripts also work without Claude. They need Python 3.8 or newer; PNG banners and
PNGs at custom sizes also need Pillow (`pip install pillow`).

```bash
cd skills/dev-icons
python scripts/find.py --list                                   # all icon ids
python scripts/find.py k8s postgres                             # look up names
python scripts/compose.py react,ts,nodejs,postgres -o stack.svg # banner
python scripts/export.py docker,kubernetes --size 256 -o icons  # single PNGs
python scripts/animate.py react,ts,nodejs --style wave -o intro.html
```

Run any script with `--help` to see all its options.

## Missing a logo?

Some well-known brands asked Simple Icons to remove their logos, so these are **not
included**: AWS, Azure, DynamoDB, VS Code, Windows, C#, PowerShell, Playwright, Heroku,
Slack and OpenAI. Claude will tell you when an icon isn't available rather than drawing
a substitute.

To request another logo, [open an issue](https://github.com/Hirusha-Nikson/pro-icons-skill/issues).
It has to exist on [simpleicons.org](https://simpleicons.org).

## Adding icons (for contributors)

You need Node.js 20 or newer.

1. Find the logo on [simpleicons.org](https://simpleicons.org) and note its slug
   (the name in the URL or the download filename).
2. Add an entry to [`source/icons.json`](source/icons.json):
   ```json
   { "id": "zod", "slug": "zod", "name": "Zod", "category": "backend", "aliases": [] }
   ```
   `id` is what people type, so keep it short and lowercase.
3. Rebuild everything:
   ```bash
   npm install
   npm run build
   ```
   This regenerates the tiles (`skills/dev-icons/tiles.bin`), the icon list, the
   [gallery](gallery/README.md) and [`NOTICE.md`](skills/dev-icons/NOTICE.md).
   Don't edit those generated files by hand.

### How the repo is laid out

| Path | What it is |
|---|---|
| `skills/dev-icons/` | **The skill itself.** This is the only folder users install. |
| `source/` | The icon list and the build script. Not part of the skill. |
| `gallery/` | Browsable icon previews for GitHub. Not part of the skill. |

All the tiles are packed into one file (`tiles.bin`) because claude.ai skill uploads
allow at most 200 files and no archives inside the upload.

## Licence

- **Code and tile designs:** [MIT](LICENSE).
- **Logos:** **not** covered by the MIT licence. They come from
  [Simple Icons](https://simpleicons.org); some have their own licences, a few of them
  non-commercial (Vue, Sass, Tauri). See [NOTICE.md](skills/dev-icons/NOTICE.md) for
  every logo's licence and source.
- **Trademarks:** all logos are trademarks of their owners. Use them only to refer to
  the product (for example, "built with React"). Including them here does not imply any
  endorsement.

This project is not affiliated with Anthropic or with any of the brands shown.
