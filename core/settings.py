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

ENGINE_CONFIG_PATH = CONFIG_PATH.with_name("Engine.ini")

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
    "FullscreenMode": 1,
    "LastConfirmedFullscreenMode": 1,
    "PreferredFullscreenMode": 1,
    "Version": 5,
    "AudioQualityLevel": 0,
    "LastConfirmedAudioQualityLevel": 0,
    "FrameRateLimit": "60.000000",
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


ENGINE_OPTIMIZATION_PRESETS = [
    {
        "id": "image_cleanup",
        "name": "1 - Netteté",
        "button": "1 - Netteté",
        "description": "Garde TXAA. Coupe flou, bloom et lens flare.",
        "values": {
            "r.MotionBlurQuality": 0,
            "r.DepthOfFieldQuality": 0,
            "r.SceneColorFringeQuality": 0,
            "r.LensFlareQuality": 0,
            "r.BloomQuality": 0,
            "r.MaxAnisotropy": 16,
        },
    },
    {
        "id": "atmosphere",
        "name": "2 - Ambiance + TAA",
        "button": "2 - Ambiance",
        "description": "TAA + brouillard, nuages et occlusion reduits.",
        "values": {
            "r.AntiAliasingMethod": 2,
            "r.ContactShadows": 0,
            "r.VolumetricFog": 0,
            "r.VolumetricCloud": 0,
            "r.Fog": 0,
            "r.AmbientOcclusionLevels": 0,
        },
    },
    {
        "id": "lighting_reflections",
        "name": "3 - Lumieres et reflets",
        "button": "3 - Lumieres",
        "description": "AA perf + reflets, Lumen et GI reduits.",
        "values": {
            "r.AntiAliasingMethod": 1,
            "r.SSR.Quality": 0,
            "r.ReflectionEnvironment": 0,
            "r.DynamicGlobalIlluminationMethod": 0,
            "r.ReflectionMethod": 0,
            "r.Lumen.Reflections.Allow": 0,
            "r.Lumen.DiffuseIndirect.Allow": 0,
            "r.ReflectionQuality": 0,
            "r.GlobalIlluminationQuality": 0,
        },
    },
    {
        "id": "distance_shadows",
        "name": "4 - Distance et ombres",
        "button": "4 - Distance",
        "description": "AA perf + ombres, distance, LOD et vegetation reduits.",
        "values": {
            "r.AntiAliasingMethod": 1,
            "r.Shadow.MaxResolution": 1024,
            "r.Shadow.CSM.MaxCascades": 2,
            "r.Shadow.DistanceScale": "0.8",
            "r.LightMaxDrawDistanceScale": "0.8",
            "r.ViewDistanceScale": "0.8",
            "r.foliage.DensityScale": "0.7",
            "r.StaticMeshLODDistanceScale": "1.2",
            "r.Nanite": 1,
            "r.VirtualShadowMaps": 0,
            "r.Shadow.Virtual.Enable": 0,
            "r.ShadowQuality": 0,
        },
    },
]
