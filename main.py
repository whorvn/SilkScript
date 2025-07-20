
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import requests
import urllib.parse

app = FastAPI()

# Allow CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for carpet design data from frontend
class CarpetDesignRequest(BaseModel):
    design_style: str
    color_palette: str  # Name of the color palette (e.g., "Mystical Journey")
    motif: str  # Single motif name (e.g., "Palmette")
    additional_details: Optional[str] = ""  # Any additional design details

# Response model for API response
class GenerationResponse(BaseModel):
    success: bool
    message: str
    image_url: Optional[str] = None
    error: Optional[str] = None

def create_detailed_prompt(request: CarpetDesignRequest) -> str:
    """
    Create a detailed prompt for Azerbaijan Persian carpet generation
    based on frontend data
    """
    # Define color palettes
    color_palettes = {
        "Mystical Journey": ["Deep Purple", "Royal Blue", "Violet", "Light Gray"],
        "Mugham Harmony": ["Sky Blue", "Cyan", "Purple", "Amber"],
        "Royal Purple": ["Dark Purple", "Medium Purple", "Light Purple", "Pale Purple"],
        "Azure Sky": ["Sky Blue", "Cyan Blue", "Royal Blue", "Indigo"],
        "Earth Tones": ["Saddle Brown", "Chocolate", "Sandy Brown", "Sienna"],
        "Sunset Fire": ["Orange Red", "Dark Orange", "Gold", "Fire Brick"],
        "Forest Harmony": ["Forest Green", "Lime Green", "Olive Drab", "Yellow Green"],
        "Modern Monochrome": ["Dark Gray", "Gray", "Light Gray", "Very Light Gray"]
    }
    
    # Get colors from palette name
    colors = color_palettes.get(request.color_palette, ["Deep Red", "Navy Blue", "Golden Yellow", "Dark Gray"])
    colors_text = ", ".join(colors)
    
    # Get motif description
    motif_description = ""
    motif = request.motif.lower()
    if motif == "buta":
        motif_description = "Buta (traditional paisley motif, iconic Azerbaijan symbol representing life and eternity)"
    elif motif == "rosekhatte":
        motif_description = "RoseKhatte (rose and line motif, symbol of beauty and elegance in Azerbaijan carpets)"
    elif motif == "bird":
        motif_description = "Bird (freedom and nature symbol, representing the soul's journey to heaven)"
    elif "geometric" in motif:
        motif_description = "intricate geometric patterns (mathematical precision representing divine order and infinity)"
    elif "floral" in motif:
        motif_description = "traditional floral designs (garden of paradise motifs with roses, tulips, and vines)"
    else:
        motif_description = f"{request.motif} motif"
    
    # Create detailed prompt
    prompt = (
        f"A highly detailed, traditional Persian and Azerbaijan carpet design in the style of {request.design_style}, "
        f"featuring {motif_description}, clearly visible in the carpet design. "
        f"Intricate floral and geometric patterns, rich textures, and authentic weaving. "
        f"Color palette: {colors_text}. "
        f"Ornate, symmetrical, museum-quality, high-resolution, vibrant, "
        f"inspired by historical carpets from Shirvan, Karabagh, and the Caucasus region."
    )
    
    # Add additional details if provided
    if request.additional_details:
        prompt += f" {request.additional_details}."
    
    return prompt

@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Azerbaijan Carpet Design Generator API",
        "version": "1.0.0",
        "endpoints": {
            "/generate": "POST - Generate carpet design",
            "/options": "GET - Get available options",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "carpet-design-generator"}

@app.post("/generate", response_model=GenerationResponse)
async def generate_carpet_design(request: CarpetDesignRequest):
    """
    Generate Azerbaijan carpet design from frontend data
    
    Expected JSON format:
    {
      "design_style": "Tabriz",
      "color_palette": "Mystical Journey",
      "motif": "Palmette",
      "additional_details": "optional details"
    }
    """
    try:
        # Validate input
        if not request.design_style:
            raise HTTPException(status_code=400, detail="Design style is required")
        
        if not request.color_palette:
            raise HTTPException(status_code=400, detail="Color palette is required")
        
        if not request.motif:
            raise HTTPException(status_code=400, detail="Motif is required")
        
        # Create detailed prompt from frontend data
        prompt = create_detailed_prompt(request)
        
        # URL encode the prompt for Pollinations API
        encoded_prompt = urllib.parse.quote(prompt)
        api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        
        # Call Pollinations API
        response = requests.get(api_url, timeout=30)
        
        if response.status_code == 200:
            return GenerationResponse(
                success=True,
                message="Carpet design generated successfully",
                image_url=api_url
            )
        else:
            return GenerationResponse(
                success=False,
                message="Failed to generate carpet design",
                error=f"API returned status code {response.status_code}"
            )
            
    except requests.RequestException as e:
        return GenerationResponse(
            success=False,
            message="Failed to generate carpet design",
            error=f"Network error: {str(e)}"
        )
    except Exception as e:
        return GenerationResponse(
            success=False,
            message="Failed to generate carpet design",
            error=f"Internal error: {str(e)}"
        )

@app.get("/options")
def get_options():
    """
    Get available design options for the frontend
    """
    return {
        "design_patterns": [
            "Tabriz",
            "Ganja", 
            "Shirvan",
            "Baku",
            "Karabagh",
            "Gazakh",
            "Kubba"
        ],
        "color_palettes": [
            {
                "name": "Mystical Journey",
                "colors": [
                    {"name": "Deep Purple", "hex": "#4c1d95"},
                    {"name": "Royal Blue", "hex": "#6366f1"},
                    {"name": "Violet", "hex": "#a855f7"},
                    {"name": "Light Gray", "hex": "#f3f4f6"}
                ]
            },
            {
                "name": "Mugham Harmony", 
                "colors": [
                    {"name": "Sky Blue", "hex": "#0ea5e9"},
                    {"name": "Cyan", "hex": "#06b6d4"},
                    {"name": "Purple", "hex": "#8b5cf6"},
                    {"name": "Amber", "hex": "#f59e0b"}
                ]
            },
            {
                "name": "Royal Purple",
                "colors": [
                    {"name": "Dark Purple", "hex": "#4c1d95"},
                    {"name": "Medium Purple", "hex": "#7c3aed"},
                    {"name": "Light Purple", "hex": "#a855f7"},
                    {"name": "Pale Purple", "hex": "#c084fc"}
                ]
            },
            {
                "name": "Azure Sky",
                "colors": [
                    {"name": "Sky Blue", "hex": "#0ea5e9"},
                    {"name": "Cyan Blue", "hex": "#06b6d4"},
                    {"name": "Royal Blue", "hex": "#3b82f6"},
                    {"name": "Indigo", "hex": "#6366f1"}
                ]
            },
            {
                "name": "Earth Tones",
                "colors": [
                    {"name": "Saddle Brown", "hex": "#8B4513"},
                    {"name": "Chocolate", "hex": "#D2691E"},
                    {"name": "Sandy Brown", "hex": "#CD853F"},
                    {"name": "Sienna", "hex": "#A0522D"}
                ]
            },
            {
                "name": "Sunset Fire",
                "colors": [
                    {"name": "Orange Red", "hex": "#FF4500"},
                    {"name": "Dark Orange", "hex": "#FF8C00"},
                    {"name": "Gold", "hex": "#FFD700"},
                    {"name": "Fire Brick", "hex": "#B22222"}
                ]
            },
            {
                "name": "Forest Harmony",
                "colors": [
                    {"name": "Forest Green", "hex": "#228B22"},
                    {"name": "Lime Green", "hex": "#32CD32"},
                    {"name": "Olive Drab", "hex": "#6B8E23"},
                    {"name": "Yellow Green", "hex": "#9ACD32"}
                ]
            },
            {
                "name": "Modern Monochrome",
                "colors": [
                    {"name": "Dark Gray", "hex": "#2D3748"},
                    {"name": "Gray", "hex": "#4A5568"},
                    {"name": "Light Gray", "hex": "#718096"},
                    {"name": "Very Light Gray", "hex": "#E2E8F0"}
                ]
            }
        ],
        "motifs": [
            "Buta",
            "Khari Bul-Bul",
            "Bird",
            "Geometric patterns",
            "Floral designs",
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
