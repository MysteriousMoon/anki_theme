# -*- coding: utf-8 -*-

from __future__ import annotations

from aqt import mw, gui_hooks
from aqt.utils import tooltip
from aqt.theme import theme_manager

from aqt.deckbrowser import DeckBrowser
from aqt.reviewer import Reviewer
from aqt.overview import Overview


# ============================================================
# 0) Configuration
# ============================================================

def get_config():
    """Get user config with defaults fallback."""
    default = {
        "table_max_width": 820,
        "row_padding_vertical": 9,
        "row_padding_horizontal": 12,
        "row_spacing": 10,
        "count_pill_height": 22,
        "border_radius": 10,
        "light": {
            "background": "#f6f6f7",
            "surface": "#ffffff",
            "surface_2": "#fbfbfc",
            "border": "#e7e7ea",
            "text": "#1f2328",
            "muted": "#6b7280",
            "accent": "#4f6ef7",
            "new": "#3b82f6",
            "learn": "#f59e0b",
            "due": "#10b981"
        },
        "dark": {
            "background": "#1c1c1f",
            "surface": "#242427",
            "surface_2": "#2a2a2e",
            "border": "#34343a",
            "text": "#e6e6e8",
            "muted": "#a0a0aa",
            "accent": "#7aa2ff",
            "new": "#7aa2ff",
            "learn": "#ffcc66",
            "due": "#57d39a"
        }
    }
    
    user_config = mw.addonManager.getConfig(__name__) or {}
    
    # Merge user config with defaults
    config = default.copy()
    for key, value in user_config.items():
        if key in ("light", "dark") and isinstance(value, dict):
            config[key] = {**default[key], **value}
        else:
            config[key] = value
    
    return config


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Convert hex color to rgba."""
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


# ============================================================
# 1) Theme tokens (CSS variables) - Generated from config
# ============================================================

def generate_tokens_light(cfg: dict) -> str:
    c = cfg["light"]
    layout = cfg
    return f"""
:root{{
  --ui-bg: {c['background']};
  --ui-surface: {c['surface']};
  --ui-surface-2: {c['surface_2']};
  --ui-border: {c['border']};
  --ui-border-subtle: rgba(0,0,0,0.06);
  --ui-text: {c['text']};
  --ui-muted: {c['muted']};

  --ui-accent: {c['accent']};

  --ui-new:   {c['new']};
  --ui-learn: {c['learn']};
  --ui-due:   {c['due']};

  --ui-new-bg:   {hex_to_rgba(c['new'], 0.12)};
  --ui-learn-bg: {hex_to_rgba(c['learn'], 0.14)};
  --ui-due-bg:   {hex_to_rgba(c['due'], 0.14)};

  --ui-radius: {layout['border_radius']}px;
  --ui-radius-sm: {max(layout['border_radius'] - 2, 4)}px;

  --ui-shadow: 0 1px 3px rgba(0,0,0,0.06);
  --ui-shadow-hover: 0 2px 10px rgba(0,0,0,0.08);

  --ui-hover: rgba(0,0,0,0.035);
  --ui-active: rgba(0,0,0,0.06);

  /* Map to Anki-ish vars (some add-ons use these) */
  --canvas: var(--ui-bg);
  --fg: var(--ui-text);
  --border: var(--ui-border);
  --border-subtle: var(--ui-border-subtle);
  --border-radius: var(--ui-radius-sm);
}}
"""


def generate_tokens_dark(cfg: dict) -> str:
    c = cfg["dark"]
    layout = cfg
    return f"""
  --ui-bg: {c['background']};
  --ui-surface: {c['surface']};
  --ui-surface-2: {c['surface_2']};
  --ui-border: {c['border']};
  --ui-border-subtle: rgba(255,255,255,0.06);
  --ui-text: {c['text']};
  --ui-muted: {c['muted']};

  --ui-accent: {c['accent']};

  --ui-new:   {c['new']};
  --ui-learn: {c['learn']};
  --ui-due:   {c['due']};

  --ui-new-bg:   {hex_to_rgba(c['new'], 0.16)};
  --ui-learn-bg: {hex_to_rgba(c['learn'], 0.16)};
  --ui-due-bg:   {hex_to_rgba(c['due'], 0.16)};

  --ui-shadow: 0 1px 3px rgba(0,0,0,0.35);
  --ui-shadow-hover: 0 2px 14px rgba(0,0,0,0.45);

  --ui-hover: rgba(255,255,255,0.045);
  --ui-active: rgba(255,255,255,0.075);

  --canvas: var(--ui-bg);
  --fg: var(--ui-text);
  --border: var(--ui-border);
  --border-subtle: var(--ui-border-subtle);
  --border-radius: var(--ui-radius-sm);
"""


def generate_css_variables(cfg: dict) -> str:
    return (
        generate_tokens_light(cfg)
        + """
/* Night mode variants (Anki / add-ons differ) */
html.nightMode, body.nightMode, .nightMode,
html.night_mode, body.night_mode, .night_mode,
html.night-mode, body.night-mode, .night-mode,
:root[class*="night-mode"], html[class*="night-mode"], body[class*="night-mode"]{
"""
        + generate_tokens_dark(cfg)
        + """
}
"""
    )


# ============================================================
# 2) DeckBrowser CSS - Generated from config
# ============================================================

def generate_deck_browser_css(cfg: dict) -> str:
    layout = cfg
    return generate_css_variables(cfg) + f"""
html, body {{
  background: var(--ui-bg) !important;
  color: var(--ui-text) !important;
  font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
  font-size: 14px !important;
}}

/* Center embedded elements like heatmaps */
center {{ text-align: center !important; }}

/* Link styling */
a {{ color: var(--ui-accent) !important; text-decoration: none !important; }}
a:hover {{ text-decoration: underline !important; }}

/*
  MAIN LAYOUT TABLE
  - Max width constrained for readability
  - Centered horizontally
*/
table {{
  width: 100% !important;
  max-width: {layout['table_max_width']}px !important;
  margin: 18px auto 0 !important;
  border-collapse: separate !important;
  border-spacing: 0 {layout['row_spacing']}px !important;
  table-layout: fixed !important;
  text-align: left !important;
}}

/* Header styling */
tbody > tr:first-child th {{
  display: table-cell !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  color: var(--ui-muted) !important;
  letter-spacing: 0.2px !important;
  padding: 6px 10px !important;
  border: none !important;
  background: transparent !important;
  white-space: nowrap !important;
}}

/* Deck name header alignment */
tbody > tr:first-child th[colspan="5"] {{
  text-align: left !important;
  padding-left: 16px !important;
}}
/* Reserve space for collapse icon so text aligns nicely */
tbody > tr:first-child th[colspan="5"]::before{{
  content: "";
  display: inline-block;
  width: 22px;
}}

/* Column widths */
tbody > tr:first-child th.count {{
  width: 92px !important;
  text-align: center !important;
  padding: 6px 0 !important;
}}
tbody > tr:first-child th.optscol {{
  width: 44px !important;
}}

/* Hide drag helper row */
tr.top-level-drag-row {{ display: none !important; }}

/*
  DECK ROWS
  - Card-like appearance
  - Compact padding
*/
tr.deck td {{
  background: var(--ui-surface) !important;
  border-top: 1px solid var(--ui-border) !important;
  border-bottom: 1px solid var(--ui-border) !important;
  padding: {layout['row_padding_vertical']}px {layout['row_padding_horizontal']}px !important;
  vertical-align: middle !important;
  transition: background-color 120ms ease, box-shadow 120ms ease, transform 120ms ease;
}}

/* Rounded corners for the row "card" */
tr.deck td:first-child {{
  border-left: 1px solid var(--ui-border) !important;
  border-radius: var(--ui-radius) 0 0 var(--ui-radius) !important;
  padding-left: 14px !important;
}}
tr.deck td:last-child {{
  border-right: 1px solid var(--ui-border) !important;
  border-radius: 0 var(--ui-radius) var(--ui-radius) 0 !important;
}}

/* Hover effects */
tr.deck:hover td {{
  background: var(--ui-surface-2) !important;
  border-top-color: var(--ui-border) !important;
  border-bottom-color: var(--ui-border) !important;
}}
/* Remove segmented shadows on hover */
tr.deck:hover td:first-child,
tr.deck:hover td:last-child {{
  box-shadow: none !important;
}}
tr.deck:hover td:first-child {{ border-left-color: var(--ui-border) !important; }}
tr.deck:hover td:last-child  {{ border-right-color: var(--ui-border) !important; }}

/* Current deck indicator (active selection) */
tr.deck.current td:first-child {{
  position: relative !important;
}}
tr.deck.current td:first-child:before {{
  content: "";
  position: absolute;
  left: 8px;
  top: 12px;
  bottom: 12px;
  width: 3px;
  border-radius: 999px;
  background: var(--ui-accent);
  opacity: 0.8;
}}

/* Deck Name Text */
td.decktd {{
  color: var(--ui-text) !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
}}
a.deck {{
  color: var(--ui-text) !important;
  font-weight: 650 !important;
  font-size: 15px !important;
  letter-spacing: 0.1px !important;
}}

/* Collapse/Expand Icon */
.collapse {{ margin-right: 6px !important; opacity: 0.75; }}

/*
  COUNT PILLS
  - Configurable height
  - Centered in columns
*/
tr.deck td:nth-child(2),
tr.deck td:nth-child(3),
tr.deck td:nth-child(4) {{
  width: 92px !important;
  text-align: center !important;
  padding-left: 0 !important;
  padding-right: 0 !important;
}}

tr.deck td:nth-child(2) span.count,
tr.deck td:nth-child(2) span.zero-count,
tr.deck td:nth-child(3) span.count,
tr.deck td:nth-child(3) span.zero-count,
tr.deck td:nth-child(4) span.count,
tr.deck td:nth-child(4) span.zero-count {{
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  min-width: 40px !important;
  height: {layout['count_pill_height']}px !important;
  line-height: {layout['count_pill_height']}px !important;
  padding: 0 8px !important;
  border-radius: 999px !important;
  font-size: 11px !important;
  font-weight: 800 !important;
  border: 1px solid var(--ui-border-subtle) !important;
}}

/* Count Colors (New / Learn / Due) */
tr.deck td:nth-child(2) span.count,
tr.deck td:nth-child(2) span.zero-count {{ color: var(--ui-new) !important; background: var(--ui-new-bg) !important; }}

tr.deck td:nth-child(3) span.count,
tr.deck td:nth-child(3) span.zero-count {{ color: var(--ui-learn) !important; background: var(--ui-learn-bg) !important; }}

tr.deck td:nth-child(4) span.count,
tr.deck td:nth-child(4) span.zero-count {{ color: var(--ui-due) !important; background: var(--ui-due-bg) !important; }}

span.zero-count {{ opacity: 0.35 !important; }}

/* Options Column (Gear Icon) */
td.opts {{
  width: 44px !important;
  text-align: center !important;
  padding-left: 0 !important;
  padding-right: 0 !important;
}}

.gears {{
  opacity: 0.55 !important;
  width: 16px !important;
  height: 16px !important;
  transition: opacity 120ms ease !important;
}}
tr.deck:hover .gears {{ opacity: 1 !important; }}
/* Invert gear icon for dark mode since it's an image usually */
html.nightMode .gears, body.nightMode .gears, .nightMode .gears,
html.night_mode .gears, body.night_mode .gears, .night_mode .gears,
html.night-mode .gears, body.night-mode .gears, .night-mode .gears,
:root[class*="night-mode"] .gears {{ filter: invert(1) !important; }}

/*
  FOOTER / EXTRA BLOCKS
  - Aligned to the same max-width as the table
*/
#studiedToday {{
  max-width: {layout['table_max_width']}px !important;
  margin: 18px auto 0 !important;
  color: var(--ui-muted) !important;
  font-size: 13px !important;
  text-align: left !important;
}}

.rh-container {{
  max-width: {layout['table_max_width']}px !important;
  margin: 16px auto 0 !important;
  text-align: center !important;
}}

"""


# ============================================================
# 3) Reviewer CSS
# ============================================================

def generate_reviewer_css(cfg: dict) -> str:
    return generate_css_variables(cfg) + r"""
html, body {
  background: var(--ui-bg) !important;
  color: var(--ui-text) !important;
}

.bottom-area {
  background: var(--ui-surface) !important;
  border-top: 1px solid var(--ui-border) !important;
  box-shadow: var(--ui-shadow) !important;
}

#answer-buttons button,
.bottom-area button {
  -webkit-appearance: none !important;
  background: var(--ui-surface) !important;
  color: var(--ui-text) !important;
  border: 1px solid var(--ui-border) !important;
  border-radius: var(--ui-radius-sm) !important;
  padding: 7px 12px !important;
  box-shadow: 0 1px 3px var(--ui-border-subtle) !important;
  font-weight: 650 !important;
  transition: background-color 120ms ease, transform 120ms ease, box-shadow 120ms ease !important;
}

#answer-buttons button:hover,
.bottom-area button:hover {
  background: var(--ui-surface-2) !important;
}

#answer-buttons button:active,
.bottom-area button:active {
  background: var(--ui-active) !important;
  transform: translateY(1px) !important;
}

a { color: var(--ui-accent) !important; }
"""


# ============================================================
# 4) Overview CSS
# ============================================================

def generate_overview_css(cfg: dict) -> str:
    return generate_css_variables(cfg) + r"""
html, body {
  background: var(--ui-bg) !important;
  color: var(--ui-text) !important;
}
a { color: var(--ui-accent) !important; }
"""


# ============================================================
# 5) Qt QSS (conservative)
# ============================================================

def _qt_qss(cfg: dict, is_dark: bool) -> str:
    c = cfg["dark"] if is_dark else cfg["light"]
    
    surface = c["surface"]
    border = c["border"]
    text = c["text"]
    muted = c["muted"]
    
    # Calculate hover/active colors
    if is_dark:
        hover = "#303036"
        active = "#363640"
    else:
        hover = "#f2f3f5"
        active = "#e9ecf2"

    radius = cfg["border_radius"]

    return f"""
/* -------------------------------------------------
   QMenu: The popup menu after clicking the gear icon
--------------------------------------------------*/
QMenu {{
  background: {surface};
  color: {text};
  border: 1px solid {border};
  border-radius: {radius}px;
  padding: 6px;
  margin: 2px;
}}

QMenu::item {{
  padding: 8px 12px;
  border-radius: {max(radius - 2, 4)}px;
  margin: 2px 2px;
  background: transparent;
}}

QMenu::item:selected {{
  background: {hover};
}}

QMenu::item:pressed {{
  background: {active};
}}

QMenu::separator {{
  height: 1px;
  background: {border};
  margin: 6px 8px;
}}

QMenu::icon {{
  padding-left: 6px;
}}

QMenu::item:disabled {{
  color: {muted};
}}
"""


# ============================================================
# 6) Injection logic
# ============================================================

_STYLE_IDS = {
    DeckBrowser: "anki-ui-obsidian-deckbrowser",
    Reviewer: "anki-ui-obsidian-reviewer",
    Overview: "anki-ui-obsidian-overview",
}

def _inject_once(web_content, style_id: str, css: str) -> None:
    if f'id="{style_id}"' in web_content.head:
        return
    web_content.head += f'<style id="{style_id}">{css}</style>'

def on_webview_will_set_content(web_content, context) -> None:
    cfg = get_config()
    if isinstance(context, DeckBrowser):
        _inject_once(web_content, _STYLE_IDS[DeckBrowser], generate_deck_browser_css(cfg))
    elif isinstance(context, Reviewer):
        _inject_once(web_content, _STYLE_IDS[Reviewer], generate_reviewer_css(cfg))
    elif isinstance(context, Overview):
        _inject_once(web_content, _STYLE_IDS[Overview], generate_overview_css(cfg))

def apply_qt_skin(*_args) -> None:
    cfg = get_config()
    mw.app.setStyleSheet(_qt_qss(cfg, bool(theme_manager.night_mode)))


# ============================================================
# 7) Hooks
# ============================================================

gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
gui_hooks.profile_did_open.append(apply_qt_skin)

if hasattr(gui_hooks, "theme_did_change"):
    gui_hooks.theme_did_change.append(apply_qt_skin)

tooltip("UI skin loaded", period=900)
