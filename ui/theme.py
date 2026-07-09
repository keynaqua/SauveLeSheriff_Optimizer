from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parents[1]
ICON_PATH = PACKAGE_DIR / "assets" / "icon.ico"
EMOJI_DIR = PACKAGE_DIR / "assets" / "emojis"

BG = "#eef4ff"
SURFACE = "#ffffff"
TEXT = "#111827"
MUTED = "#6b7280"
ACCENT = "#2563eb"
ACCENT_DARK = "#1d4ed8"
SUCCESS = "#0ea5e9"
SUCCESS_DARK = "#0284c7"
DANGER = "#b91c1c"
DANGER_SOFT = "#fee2e2"
HERO = "#172554"
HERO_SOFT = "#1d4ed8"

DISPLAY_NAMES = {
    "sg.ViewDistanceQuality": "Distance d'affichage",
    "sg.AntiAliasingQuality": "Anti-aliasing",
    "sg.ShadowQuality": "Ombres",
    "sg.GlobalIlluminationQuality": "Illumination globale",
    "sg.ReflectionQuality": "Réflexions",
    "sg.PostProcessQuality": "Post-traitement",
    "sg.TextureQuality": "Textures",
    "sg.EffectsQuality": "Effets",
    "sg.FoliageQuality": "Végétation",
    "sg.ShadingQuality": "Shading",
    "sg.LandscapeQuality": "Paysage",
}

QUALITY_LABELS = {
    0: "Bas",
    1: "Moyen",
    2: "Haut",
    3: "Epic",
}
