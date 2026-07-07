<h1 align="center">
  🐱 Catppuccin for Team+
</h1>

<p align="center">
  <b>Soothing pastel themes for Team+ (team.kfsyscc.org) — a Chrome extension</b><br>
  Dark mode & light mode for the Team+ enterprise messenger, powered by the
  <a href="https://catppuccin.com/palette/">Catppuccin palette</a> in all four flavors.
</p>

<p align="center">
  <a href="https://github.com/htlin222/catppuccin-teamplus/releases/latest"><img alt="GitHub release" src="https://img.shields.io/github/v/release/htlin222/catppuccin-teamplus?colorA=1e1e2e&colorB=fab387&style=flat-square"></a>
  <a href="https://github.com/htlin222/catppuccin-teamplus/blob/main/LICENSE"><img alt="License MIT" src="https://img.shields.io/badge/license-MIT-a6e3a1?colorA=1e1e2e&style=flat-square"></a>
  <a href="https://catppuccin.com/palette/"><img alt="Catppuccin" src="https://img.shields.io/badge/palette-Catppuccin-cba6f7?colorA=1e1e2e&style=flat-square"></a>
</p>

---

**Catppuccin for Team+** restyles the Team+ web messenger (即時交談、動態消息、團隊互動、
個人設定) with the community-loved [Catppuccin](https://github.com/catppuccin/catppuccin)
color palette. Pick your flavor from the toolbar popup — changes apply instantly, no reload
needed.

## 🍨 Flavors

| Flavor | Vibe |
| --- | --- |
| ☀️ **Latte** | Our lightest theme harmoniously inverting the essence of Catppuccin's dark themes |
| 🪴 **Frappé** | A less vibrant alternative using subdued colors for a muted aesthetic |
| 🌺 **Macchiato** | Medium contrast with gentle colors creating a soothing atmosphere |
| 🌿 **Mocha** | The Original — our darkest variant offering a cozy feeling with color-rich accents |

## ✨ Features

- 🎨 **All four Catppuccin flavors** — Latte, Frappé, Macchiato, Mocha
- ⚡ **Instant switching** — pick a flavor in the popup, the page restyles live
- 🌙 **Full coverage** — chat, message walls, team pages, contacts, settings, popups
- 🔘 **One-click on/off** — master toggle with an `OFF` badge, state is remembered
- 🧩 **Zero tracking, zero network calls** — pure CSS injection, everything runs locally
- 🤖 **Regenerable** — themes are generated from the site's own CSS bundles by a
  property-aware color mapper, so upstream restyles are a one-command rebuild away

## 📦 Install

### From release (recommended)

1. Download the latest `catppuccin-teamplus-vX.Y.Z.zip` from
   [Releases](https://github.com/htlin222/catppuccin-teamplus/releases/latest) and unzip it
2. Open `chrome://extensions`, enable **Developer mode**
3. Click **Load unpacked** and select the unzipped folder

### From source

```bash
git clone https://github.com/htlin222/catppuccin-teamplus.git
```

Then load the `extension/` folder via `chrome://extensions` → **Load unpacked**.

## 🔧 How it works

Team+ ships ~20 minified CSS bundles that mix `--color_XXXXXX` custom properties with raw
hex fallbacks. `tools/generate_theme_css.py` parses every rule in those bundles and emits
2100+ override rules per flavor with **property-aware color mapping**:

- the same gray maps to a *light* color as text, a *dark* color as background, and a
  *mid* color as border (Text/Subtext/Overlay vs Base/Mantle/Surface hierarchies)
- brand orange → **Peach**, badges → **Red**, presence → **Green**
- when a background becomes an accent color, white text in the same rule flips to
  **Crust** (the Catppuccin convention of dark-on-accent)

Because the site's own rules carry `!important`, the content script re-appends the theme
stylesheet after all site CSS once the DOM is ready — with equal specificity and
importance, document order decides, and the theme wins.

### Regenerate after an upstream update

```bash
./tools/fetch_bundles.sh /tmp/bundles
python3 tools/generate_theme_css.py /tmp/bundles/*.css extension/css/
```

## 🗺️ Palette mapping

| Team+ original | Role | Catppuccin |
| --- | --- | --- |
| `#fff` | main surface | Base |
| `#f5f5f5` | recessed panels | Mantle |
| `#ebebeb` | hover / incoming bubbles | Surface0 |
| `#dcdcdc` | borders, selected state | Surface1 |
| `#ffb793` | own message bubble | Surface2 |
| `#373737` | primary text | Text |
| `#5b5b5b` | secondary text | Subtext1 |
| `#919191` | muted text | Overlay1 |
| `#ff8a4f` / `#ff6416` | brand accent | Peach |
| `#ff5252` | badges / errors | Red |
| `#6de339` | online presence | Green |

## 🙋 FAQ

**Why not just use a generic dark-mode extension?**
Generic filters (invert/hue-rotate) wash out avatars, stickers and photos. This extension
maps each color semantically, so images stay untouched and the UI stays crisp.

**Does it work on other Team+ deployments?**
The generator is deployment-agnostic, but this build targets `team.kfsyscc.org`. Fork it,
point `tools/fetch_bundles.sh` at your host, regenerate, and adjust `manifest.json`.

## 💝 Credits

- Palette by [Catppuccin](https://github.com/catppuccin/catppuccin) (MIT)
- Not affiliated with team+ / 互動資通 or Koo Foundation Sun Yat-Sen Cancer Center

## 📄 License

[MIT](LICENSE) — theme CSS is generated; the Catppuccin palette is used under MIT.
