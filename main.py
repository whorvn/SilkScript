
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

# Allow CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example design patterns, color palettes, and motifs
DESIGN_PATTERNS = [
    "Epic Journey Motif",
    "Rhythmic Harmony",
    "Shirvan",
    "Karabagh"
]

COLOR_PALETTES = [
    {
        "name": "Sunset Fire",
        "colors": [
            {"name": "Red", "hex": "#FF4500"},
            {"name": "Orange", "hex": "#FFA500"},
            {"name": "Yellow", "hex": "#FFD700"},
            {"name": "Deep Purple", "hex": "#800080"}
        ]
    },
    {
        "name": "Ocean Breeze",
        "colors": [
            {"name": "Blue", "hex": "#1E90FF"},
            {"name": "Teal", "hex": "#008080"},
            {"name": "Seafoam", "hex": "#20B2AA"},
            {"name": "Sand", "hex": "#F4E2D8"}
        ]
    }
]

PATTERNS = [
    "Buta",
    "Khari BulBul"
]

@app.get("/options")
def get_options():
    return {
        "design_patterns": DESIGN_PATTERNS,
        "color_palettes": COLOR_PALETTES,
        "motifs": PATTERNS
    }

@app.get("/generate-image")
def generate_image(
    design_pattern: str = Query(...),
    color_palette: str = Query(...),
    motif: str = Query(...)
):
    # Find palette colors
    palette = next((p for p in COLOR_PALETTES if p["name"] == color_palette), None)
    if not palette:
        return JSONResponse(status_code=400, content={"error": "Invalid color palette"})
    colors = ", ".join([f"{c['name']} ({c['hex']})" for c in palette["colors"]])
    # Compose a detailed prompt for Persian and Azerbaijan carpet styles
    motif_detail = ""
    if motif.lower() == "buta":
        motif_detail = "Buta, an iconic Azerbaijan cultural motif, clearly visible in the carpet design. "
    elif motif.lower() == "khari bulbul":
        motif_detail = "Khari BulBul, a famous Azerbaijan cultural motif, clearly featured in the carpet. "
    else:
        motif_detail = f"{motif} motif, clearly visible in the carpet design. "

    prompt = (
        f"A highly detailed, traditional Persian and Azerbaijan carpet design in the style of {design_pattern}, "
        f"{motif_detail}Intricate floral and geometric patterns, rich textures, and authentic weaving. "
        f"Color palette: {colors}. Ornate, symmetrical, museum-quality, high-resolution, vibrant, inspired by historical carpets from Shirvan, Karabagh, and the Caucasus region."
    )
    api_url = f"https://image.pollinations.ai/prompt/{prompt}"
    # Call Pollinations API
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            # Return the image URL (Pollinations serves the image directly)
            return {"image_url": api_url}
        else:
            return JSONResponse(status_code=502, content={"error": "Image generation failed"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
