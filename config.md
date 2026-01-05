# Anki Theme Configuration

This addon supports customization through Anki's addon config dialog.

**To access:** Tools → Add-ons → Select "anki_theme" → Config

## Example: Custom Theme

```json
{
    "table_max_width": 900,
    "row_padding_vertical": 12,
    "row_spacing": 8,
    "count_pill_height": 24,
    "border_radius": 8,
    
    "light": {
        "background": "#fafafa",
        "surface": "#ffffff",
        "accent": "#6366f1",
        "new": "#3b82f6",
        "learn": "#eab308",
        "due": "#22c55e"
    },
    
    "dark": {
        "background": "#0f0f0f",
        "surface": "#1a1a1a",
        "accent": "#818cf8",
        "new": "#60a5fa",
        "learn": "#fbbf24",
        "due": "#4ade80"
    }
}
```

**Note:** After changing the config, restart Anki or use Tools → Add-ons → View Files to reload.
