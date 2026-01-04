import os
import urllib.request
import urllib.parse
import json

# Configuration
OUTPUT_DIR = "assets/badges"
ICON_CDN = "https://cdn.simpleicons.org"

# Badge Style Config
FONT_FAMILY = "Verdana, Geneva, sans-serif"
FONT_SIZE = 11
HEIGHT = 28
ICON_SIZE = 16
PADDING_X = 10
GAP = 6
BORDER_RADIUS = 4

# Tech Stack & Socials Data
# Format: (Name, Slug, Color, TextColor)
BADGES = [
    # Socials
    ("Instagram", "instagram", "#E4405F", "white"),
    ("LinkedIn", "linkedin", "#0077B5", "white"),
    ("X", "x", "black", "white"),
    ("HackerRank", "hackerrank", "#2EC866", "white"),
    
    # Tech Stack
    ("C", "c", "#00599C", "white"),
    ("C#", "csharp", "#239120", "white"), # Try csharp again, if fails we fallback
    ("C++", "cplusplus", "#00599C", "white"),
    ("JavaScript", "javascript", "#F7DF1E", "black"),
    ("LaTeX", "latex", "#008080", "white"),
    ("Python", "python", "#3776AB", "white"),
    ("AssemblyScript", "assemblyscript", "#000000", "white"),
    ("Bash", "gnubash", "#4EAA25", "white"),
    ("AWS", "amazonaws", "#232F3E", "white"), # Try amazonaws again, maybe network? or 'amazon'
    ("Azure", "azuredevops", "#0078D4", "white"), # Try azuredevops or microsoftazure
    ("Oracle", "oracle", "#F80000", "white"),
    ("Vercel", "vercel", "#000000", "white"),
    ("Google Cloud", "googlecloud", "#4285F4", "white"),
    ("FastAPI", "fastapi", "#009688", "white"),
    ("Next.js", "nextdotjs", "black", "white"),
    ("Vite", "vite", "#646CFF", "white"),
    ("Apache", "apache", "#D42029", "white"),
    ("Supabase", "supabase", "#3ECF8E", "white"),
    ("MySQL", "mysql", "#4479A1", "white"),
    ("MongoDB", "mongodb", "#47A248", "white"),
    ("Matplotlib", "matplotlib", "#ffffff", "black"),
    ("Keras", "keras", "#D00000", "white"),
    ("MLflow", "mlflow", "#0194E2", "white"),
    ("NumPy", "numpy", "#013243", "white"),
    ("Pandas", "pandas", "#150458", "white"),
    ("Plotly", "plotly", "#3F4F75", "white"),
    ("PyTorch", "pytorch", "#EE4C2C", "white"),
    ("scikit-learn", "scikitlearn", "#F7931E", "white"),
    ("SciPy", "scipy", "#8CAAE6", "white"),
    ("TensorFlow", "tensorflow", "#FF6F00", "white"),
    ("GitHub", "github", "#181717", "white"),
]

# Custom SVG Template
def create_svg(name, icon_svg, bg_color, text_color):
    # Calculate width based on text length (approximate)
    text_width = len(name) * 7.5
    
    if icon_svg:
        total_width = PADDING_X + ICON_SIZE + GAP + text_width + PADDING_X
        content_start_x = PADDING_X
        text_x = content_start_x + ICON_SIZE + GAP
        # Add shadow to icon
        icon_element = f"""<g transform="translate({content_start_x}, {(HEIGHT - ICON_SIZE) / 2})">
    {icon_svg.replace('<svg', f'<svg width="{ICON_SIZE}" height="{ICON_SIZE}" fill="{text_color}"')}
  </g>"""
    else:
        # No icon, center text
        total_width = PADDING_X + text_width + PADDING_X
        text_x = total_width / 2
        icon_element = ""
        
    # Plastic/Glossy Effect Gradients
    gradients = """
    <linearGradient id="plastic-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#fff" stop-opacity="0.7" />
      <stop offset="5%" stop-color="#fff" stop-opacity="0.5" />
      <stop offset="100%" stop-color="#000" stop-opacity="0.2" />
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="0" dy="1" stdDeviation="0.5" flood-color="#000" flood-opacity="0.5"/>
    </filter>
    """
        
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{HEIGHT}" viewBox="0 0 {total_width} {HEIGHT}">
  <defs>
    {gradients}
  </defs>
  
  <!-- Background Color -->
  <rect width="{total_width}" height="{HEIGHT}" rx="{BORDER_RADIUS}" fill="{bg_color}" />
  
  <!-- Plastic Gradient Overlay -->
  <rect width="{total_width}" height="{HEIGHT}" rx="{BORDER_RADIUS}" fill="url(#plastic-gradient)" />
  
  <!-- Content with Shadow -->
  <g filter="url(#shadow)">
      {icon_element}
      <text x="{text_x}" y="{HEIGHT/2 + 4}" font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}" fill="{text_color}" font-weight="bold" text-anchor="{'middle' if not icon_svg else 'start'}">{name}</text>
  </g>
</svg>"""
    return svg

def fetch_icon(slug):
    # Try multiple variations if needed
    slugs_to_try = [slug]
    if slug == "csharp": slugs_to_try.append("c") # Fallback
    if slug == "amazonaws": slugs_to_try.extend(["amazon", "aws"])
    if slug == "microsoftazure": slugs_to_try.extend(["azure", "microsoft"])
    if slug == "oracle": slugs_to_try.append("oracle") # Should work
    if slug == "matplotlib": slugs_to_try.append("python") # Fallback
    
    for s in slugs_to_try:
        try:
            url = f"{ICON_CDN}/{s}"
            with urllib.request.urlopen(url) as response:
                return response.read().decode('utf-8')
        except:
            continue
            
    print(f"Could not find icon for {slug}")
    return None

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"Generating badges in {OUTPUT_DIR}...")
    
    for name, slug, bg_color, text_color in BADGES:
        print(f"Processing {name}...")
        icon_svg = fetch_icon(slug)
        badge_svg = create_svg(name, icon_svg, bg_color, text_color)
        
        filename = f"{slug}.svg"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, "w") as f:
            f.write(badge_svg)
            
    print("Done!")

if __name__ == "__main__":
    main()
