import os
from pathlib import Path


GAME_NAME = "SauveLeSherif"

LOCALAPPDATA = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))

CONFIG_PATH = (
    LOCALAPPDATA
    / GAME_NAME
    / "Saved"
    / "Config"
    / "Windows"
    / "GameUserSettings.ini"
)

SLIDER_KEYS = [
    "sg.ViewDistanceQuality",
    "sg.AntiAliasingQuality",
    "sg.ShadowQuality",
    "sg.GlobalIlluminationQuality",
    "sg.ReflectionQuality",
    "sg.PostProcessQuality",
    "sg.TextureQuality",
    "sg.EffectsQuality",
    "sg.FoliageQuality",
    "sg.ShadingQuality",
    "sg.LandscapeQuality",
]

OPTIMIZED_VALUES = {
    "sg.ViewDistanceQuality": 3,
    "sg.AntiAliasingQuality": 0,
    "sg.ShadowQuality": 0,
    "sg.GlobalIlluminationQuality": 3,
    "sg.ReflectionQuality": 3,
    "sg.PostProcessQuality": 0,
    "sg.TextureQuality": 3,
    "sg.EffectsQuality": 0,
    "sg.FoliageQuality": 1,
    "sg.ShadingQuality": 0,
    "sg.LandscapeQuality": 3,
    "bUseVSync": "False",
    "bUseDynamicResolution": "False",
    "ResolutionSizeX": 1920,
    "ResolutionSizeY": 1080,
    "LastUserConfirmedResolutionSizeX": 1920,
    "LastUserConfirmedResolutionSizeY": 1080,
    "FullscreenMode": 0,
    "LastConfirmedFullscreenMode": 0,
    "PreferredFullscreenMode": 0,
    "Version": 5,
    "AudioQualityLevel": 0,
    "LastConfirmedAudioQualityLevel": 0,
    "FrameRateLimit": "0.000000",
    "DesiredScreenWidth": 1920,
    "bUseDesiredScreenHeight": "False",
    "DesiredScreenHeight": 1080,
    "LastUserConfirmedDesiredScreenWidth": 1920,
    "LastUserConfirmedDesiredScreenHeight": 1080,
    "LastRecommendedScreenWidth": "-1.000000",
    "LastRecommendedScreenHeight": "-1.000000",
    "LastCPUBenchmarkResult": "-1.000000",
    "LastGPUBenchmarkResult": "-1.000000",
    "LastGPUBenchmarkMultiplier": "1.000000",
    "bUseHDRDisplayOutput": "False",
    "HDRDisplayOutputNits": 1000,
}

RESTORE_VALUES = {key: 3 for key in SLIDER_KEYS}


STEAM_APP_ID = "4760110"
STEAM_LAUNCH_FLAG = "-dx11"
