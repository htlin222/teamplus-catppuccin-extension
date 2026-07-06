#!/usr/bin/env python3
"""Generate Catppuccin theme override CSS for Team+ from its light-theme bundles.

Parses the minified CSS bundles and, for every declaration whose value contains
a mappable color, emits an override rule with the palette equivalent and
!important. Mapping is property-aware: the same gray maps differently as text
color vs background vs border. Supports all four Catppuccin flavors:
Latte, Frappé, Macchiato, Mocha — https://catppuccin.com/palette/

Usage:
    python3 tools/generate_theme_css.py <bundles...> <output-dir>
    # writes <output-dir>/theme-{latte,frappe,macchiato,mocha}.css
"""

import re
import sys
from pathlib import Path

PALETTES = {
    "latte": {
        "crust": "#dce0e8", "mantle": "#e6e9ef", "base": "#eff1f5",
        "surface0": "#ccd0da", "surface1": "#bcc0cc", "surface2": "#acb0be",
        "overlay0": "#9ca0b0", "overlay1": "#8c8fa1", "overlay2": "#7c7f93",
        "subtext0": "#6c6f85", "subtext1": "#5c5f77", "text": "#4c4f69",
        "peach": "#fe640b", "red": "#d20f39", "green": "#40a02b",
        "sky": "#04a5e5", "yellow": "#df8e1d", "blue": "#1e66f5",
        "teal": "#179299", "dark": False,
    },
    "frappe": {
        "crust": "#232634", "mantle": "#292c3c", "base": "#303446",
        "surface0": "#414559", "surface1": "#51576d", "surface2": "#626880",
        "overlay0": "#737994", "overlay1": "#838ba7", "overlay2": "#949cbb",
        "subtext0": "#a5adce", "subtext1": "#b5bfe2", "text": "#c6d0f5",
        "peach": "#ef9f76", "red": "#e78284", "green": "#a6d189",
        "sky": "#99d1db", "yellow": "#e5c890", "blue": "#8caaee",
        "teal": "#81c8be", "dark": True,
    },
    "macchiato": {
        "crust": "#181926", "mantle": "#1e2030", "base": "#24273a",
        "surface0": "#363a4f", "surface1": "#494d64", "surface2": "#5b6078",
        "overlay0": "#6e738d", "overlay1": "#8087a2", "overlay2": "#939ab7",
        "subtext0": "#a5adcb", "subtext1": "#b8c0e0", "text": "#cad3f5",
        "peach": "#f5a97f", "red": "#ed8796", "green": "#a6da95",
        "sky": "#91d7e3", "yellow": "#eed49f", "blue": "#8aadf4",
        "teal": "#8bd5ca", "dark": True,
    },
    "mocha": {
        "crust": "#11111b", "mantle": "#181825", "base": "#1e1e2e",
        "surface0": "#313244", "surface1": "#45475a", "surface2": "#585b70",
        "overlay0": "#6c7086", "overlay1": "#7f849c", "overlay2": "#9399b2",
        "subtext0": "#a6adc8", "subtext1": "#bac2de", "text": "#cdd6f4",
        "peach": "#fab387", "red": "#f38ba8", "green": "#a6e3a1",
        "sky": "#89dceb", "yellow": "#f9e2af", "blue": "#89b4fa",
        "teal": "#94e2d5", "dark": True,
    },
}


def build_maps(P):
    """Property-aware color maps (Team+ light-theme color -> palette color)."""
    text_map = {
        "#373737": P["text"], "#333": P["text"], "#3c3c3c": P["text"],
        "#000": P["text"], "#111": P["text"], "#222": P["text"],
        "#101010": P["text"], "#202020": P["text"], "#303030": P["text"],
        "#3f3f3f": P["text"], "#444": P["text"],
        "#5b5b5b": P["subtext1"], "#555": P["subtext1"],
        "#5a5a5a": P["subtext1"], "#5f5f5f": P["subtext1"],
        "#666": P["subtext0"], "#696969": P["subtext0"],
        "#7f7f7f": P["overlay2"], "#888": P["overlay2"],
        "#7b7b7b": P["overlay2"], "#7e7e7e": P["overlay2"],
        "#8a8a8a": P["overlay2"], "#8f8f8f": P["overlay2"],
        "#919191": P["overlay1"], "#999": P["overlay1"],
        "#9a9a9a": P["overlay1"], "#9f9f9f": P["overlay1"],
        "#a1a1a1": P["overlay1"], "#a7a7a7": P["overlay1"],
        "#afafaf": P["overlay1"],
        "#c2c2c2": P["overlay0"], "#c9c9c9": P["overlay0"], "#ccc": P["overlay0"],
        "#baaf94": P["subtext0"], "#b2c1c3": P["subtext0"],
        "#cd4400": P["peach"], "#ff8a4f": P["peach"], "#ff6416": P["peach"],
        "#ffab81": P["peach"], "#ffb793": P["peach"], "#ff6f27": P["peach"],
        "#fb760f": P["peach"], "#fc6e51": P["peach"],
        "#ff5252": P["red"], "#f00": P["red"], "#ff1515": P["red"],
        "#fd3000": P["red"], "#e12a2a": P["red"],
        "#00b900": P["green"], "#6de339": P["green"], "#22b422": P["green"],
        "#01bad4": P["sky"], "#77a1d5": P["blue"], "#4bc7c7": P["teal"],
    }
    bg_map = {
        "#fff": P["base"], "#fefefe": P["base"], "#fdfdfd": P["base"],
        "#fafafa": P["base"], "#f8f8f8": P["base"], "#f7f7f7": P["base"],
        "#f9f9f9": P["base"],
        "#f5f5f5": P["mantle"], "#f4f4f4": P["mantle"], "#f2f2f2": P["mantle"],
        "#f0f0f0": P["mantle"], "#f8f2ef": P["mantle"],
        "#efefef": P["surface0"], "#ededed": P["surface0"],
        "#ebebeb": P["surface0"], "#eee": P["surface0"],
        "#e8e8e8": P["surface0"], "#e5e5e5": P["surface0"],
        "#e9e9e9": P["surface0"],
        "#e0e0e0": P["surface1"], "#dfdfdf": P["surface1"],
        "#dedede": P["surface1"], "#ddd": P["surface1"],
        "#dcdcdc": P["surface1"], "#dadada": P["surface1"],
        "#d5d5d5": P["surface1"], "#d2d2d2": P["surface1"],
        "#d4d4d4": P["surface1"],
        "#ccc": P["surface2"], "#c9c9c9": P["surface2"], "#c2c2c2": P["surface2"],
        "#afafaf": P["overlay0"], "#a7a7a7": P["overlay0"],
        "#a1a1a1": P["overlay0"], "#999": P["overlay0"], "#919191": P["overlay0"],
        # dark surfaces in the light theme (tooltips, toasts) — lift above base
        "#373737": P["surface1"], "#3a3a3a": P["surface1"],
        "#5b5b5b": P["surface2"], "#5f5f5f": P["surface2"],
        "#606060": P["surface2"],
        "#000": P["crust"],
        # brand / semantic
        "#ff8a4f": P["peach"], "#ff6416": P["peach"], "#ffab81": P["peach"],
        "#ff6f27": P["peach"], "#fb9f72": P["peach"], "#cd4400": P["peach"],
        "#ffb793": P["surface2"],   # own message bubble
        "#ffd08a": P["surface2"],
        "#ffe5d9": P["surface1"],   # selected / checked state
        "#ff5252": P["red"], "#f00": P["red"], "#ff1515": P["red"],
        "#e12a2a": P["red"],
        "#00b900": P["green"], "#6de339": P["green"], "#22b422": P["green"],
        "#01bad4": P["sky"],
    }
    border_map = {
        "#fff": P["surface0"],
        "#f5f5f5": P["surface0"], "#f0f0f0": P["surface0"],
        "#ebebeb": P["surface0"], "#eee": P["surface0"],
        "#e8e8e8": P["surface0"], "#e5e5e5": P["surface0"],
        "#e0e0e0": P["surface1"], "#dfdfdf": P["surface1"],
        "#dedede": P["surface1"], "#ddd": P["surface1"],
        "#dcdcdc": P["surface1"], "#dadada": P["surface1"],
        "#d2d2d2": P["surface1"],
        "#ccc": P["surface2"], "#c9c9c9": P["surface2"],
        "#c2c2c2": P["surface2"], "#cfcfcf": P["surface2"],
        "#c5c5c5": P["surface2"],
        "#afafaf": P["overlay0"], "#a7a7a7": P["overlay0"],
        "#a1a1a1": P["overlay0"], "#999": P["overlay0"], "#919191": P["overlay0"],
        "#888": P["overlay1"], "#7f7f7f": P["overlay1"],
        "#ff8a4f": P["peach"], "#ff6416": P["peach"], "#ffab81": P["peach"],
        "#fc6e51": P["peach"],
        "#ffb793": P["surface2"], "#ffe5d9": P["surface1"],
        "#ff5252": P["red"], "#01bad4": P["sky"],
    }
    accent_bgs = {P["peach"], P["red"], P["green"], P["sky"], P["yellow"]}
    return text_map, bg_map, border_map, accent_bgs


# Hand-written base layer appended AFTER the generated rules so that, with
# equal specificity and !important, these fixes win by document order.
BASE_TEMPLATE = """
/* ---- catppuccin-teamplus base layer ({flavor}) ---- */
:root {{ color-scheme: {scheme}; }}
html, body {{ background-color: {base} !important; }}

::-webkit-scrollbar {{ width: 10px; height: 10px; }}
::-webkit-scrollbar-track {{ background: transparent !important; }}
::-webkit-scrollbar-thumb {{ background: {surface1} !important; border-radius: 5px; }}
::-webkit-scrollbar-thumb:hover {{ background: {surface2} !important; }}
::-webkit-scrollbar-corner {{ background: transparent !important; }}

/* jScrollPane: the plugin's own default is a red bar, normally hidden */
.jspVerticalBar, .jspHorizontalBar, .jspTrack {{ background: transparent !important; }}
.jspDrag {{ background: {surface1} !important; }}
.jspDrag:hover, .jspTrack .jspActive, .jspTrack .jspHover {{ background: {surface2} !important; }}

input, textarea, select {{
  background-color: {surface0} !important;
  color: {text} !important;
  border-color: {surface1} !important;
}}
::placeholder {{ color: {overlay0} !important; }}

::selection {{ background: {selection} !important; color: {text} !important; }}

/* Stickers / photos are transparent PNGs with no bubble. The original's
   transparent rules carry no mappable color so the generator never emits
   them, and our generated !important bubble backgrounds would win —
   restate them here at equal-or-higher specificity. */
.chatRoomMainPane .chatRoomMessageMain .messageListMainPane .messageSection .msg .msgContentPane.transparent,
.chatRoomMainPane .chatRoomMessageMain .messageListMainPane .messageSection.my .msg .msgContentPane.transparent,
.chatRoomMainPane .chatRoomMessageMain .messageListMainPane .messageSection.stickerChatMsgContent .msg .msgContentPane,
.chatRoomMainPane .chatRoomMessageMain .messageListMainPane .messageSection.stickerChatMsgContent.my .msg .msgContentPane,
.stickerChatMsgContent, .stickerChatMsgContent .chatMsgContent,
.photoChatMsgContent, .photoChatMsgContent .chatMsgContent,
.broadcastChatMsgContent, .broadcastChatMsgContent .chatMsgContent {{
  background-color: transparent !important;
  background-image: none !important;
}}
{watermark}"""

WATERMARK_DIM = """
/* server-rendered watermark is designed for a white page — dim it on dark */
#watermarkImage { opacity: 0.22 !important; }
"""

TEXT_PROPS = {"color", "-webkit-text-fill-color", "caret-color", "fill", "stroke"}
BG_PROPS = {"background", "background-color"}
BORDER_PREFIXES = ("border", "outline", "box-shadow", "-webkit-box-shadow")

HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
VAR_RE = re.compile(r"var\((--[\w-]+)\)")


def normalize_hex(h):
    h = h.lower()
    if len(h) == 7 and h[1] == h[2] and h[3] == h[4] and h[5] == h[6]:
        h = "#" + h[1] + h[3] + h[5]
    return h


def normalize_hex_in(value):
    """Normalize a value that is a single hex color; '' otherwise."""
    v = value.strip().lower()
    return normalize_hex(v) if re.fullmatch(r"#[0-9a-f]{3,8}", v) else ""


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def parse_rules(css):
    """Yield (media_stack, selector, body) from minified CSS."""
    # @charset / @import are brace-less statements; strip them so they don't
    # get glued onto the following rule's selector.
    css = re.sub(r"@(?:charset|import)\s[^;]*;", "", css)
    i, n = 0, len(css)
    media_stack = []
    while i < n:
        close = css.find("}", i)
        brace = css.find("{", i)
        if brace == -1:
            break
        if close != -1 and close < brace:
            if media_stack:
                media_stack.pop()
            i = close + 1
            continue
        selector = css[i:brace].strip()
        if selector.startswith(("@media", "@supports")):
            media_stack.append(selector)
            i = brace + 1
            continue
        if selector.startswith(("@keyframes", "@-webkit-keyframes", "@font-face", "@page")):
            depth = 1
            j = brace + 1
            while j < n and depth:
                if css[j] == "{":
                    depth += 1
                elif css[j] == "}":
                    depth -= 1
                j += 1
            i = j
            continue
        end = css.find("}", brace)
        if end == -1:
            break
        yield list(media_stack), selector, css[brace + 1 : end]
        i = end + 1


def collect_root_vars(css):
    vars = {}
    for m in re.finditer(r":root\{([^}]*)\}", css):
        for decl in m.group(1).split(";"):
            if decl.strip().startswith("--"):
                k, _, v = decl.partition(":")
                vars[k.strip()] = v.strip()
    return vars


def pick_map(prop, maps):
    text_map, bg_map, border_map = maps
    p = prop.strip().lower()
    if p in TEXT_PROPS:
        return text_map
    if p in BG_PROPS:
        return bg_map
    if p.startswith(BORDER_PREFIXES):
        return border_map
    return None


def map_value(value, cmap, root_vars):
    """Replace mappable colors in a declaration value. Returns (new, changed)."""
    changed = False

    def repl_var(m):
        nonlocal changed
        resolved = root_vars.get(m.group(1), "")
        key = normalize_hex(resolved) if resolved.startswith("#") else resolved
        if key in cmap:
            changed = True
            return cmap[key]
        return m.group(0)

    def repl_hex(m):
        nonlocal changed
        key = normalize_hex(m.group(0))
        if key in cmap:
            changed = True
            return cmap[key]
        return m.group(0)

    value = VAR_RE.sub(repl_var, value)
    value = HEX_RE.sub(repl_hex, value)
    return value, changed


WHITE_TEXT = {"#fff", "#fefefe", "#f5f5f5", "#ebebeb"}


def generate(flavor, css_all, root_vars, out_path):
    P = PALETTES[flavor]
    text_map, bg_map, border_map, accent_bgs = build_maps(P)
    maps = (text_map, bg_map, border_map)

    out = []
    seen = set()
    for media, selector, body in parse_rules(css_all):
        decls_out = []
        accent_bg = False
        white_text_decl = False
        for decl in body.split(";"):
            prop, sep, value = decl.partition(":")
            if not sep:
                continue
            p = prop.strip().lower()
            value = re.sub(r"\s*!\s*important", "", value)
            if p in TEXT_PROPS and normalize_hex_in(value) in WHITE_TEXT:
                white_text_decl = True
                continue
            cmap = pick_map(prop, maps)
            if cmap is None:
                continue
            new_value, changed = map_value(value, cmap, root_vars)
            if changed:
                if p in BG_PROPS and any(a in new_value for a in accent_bgs):
                    accent_bg = True
                decls_out.append(f"{prop.strip()}:{new_value.strip()} !important")
        # Catppuccin convention: dark(ish) text on accent backgrounds
        if accent_bg and white_text_decl:
            decls_out.append(f"color:{P['crust']} !important")
        if decls_out:
            rule = f"{selector}{{{';'.join(decls_out)}}}"
            key = (tuple(media), rule)
            if key in seen:
                continue
            seen.add(key)
            for m in media:
                rule = f"{m}{{{rule}}}"
            out.append(rule)

    r, g, b = hex_to_rgb(P["peach"])
    base_layer = BASE_TEMPLATE.format(
        flavor=flavor,
        scheme="dark" if P["dark"] else "light",
        base=P["base"],
        surface0=P["surface0"],
        surface1=P["surface1"],
        surface2=P["surface2"],
        text=P["text"],
        overlay0=P["overlay0"],
        selection=f"rgba({r}, {g}, {b}, 0.3)",
        watermark=WATERMARK_DIM if P["dark"] else "",
    )
    Path(out_path).write_text("\n".join(out) + "\n" + base_layer)
    print(f"{out_path}: {len(out)} rules, {Path(out_path).stat().st_size} bytes")


def main():
    *css_files, out_dir = sys.argv[1:]
    css_all = "".join(Path(f).read_text(encoding="utf-8-sig") for f in css_files)
    root_vars = collect_root_vars(css_all)
    for flavor in PALETTES:
        generate(flavor, css_all, root_vars, Path(out_dir) / f"theme-{flavor}.css")


if __name__ == "__main__":
    main()
