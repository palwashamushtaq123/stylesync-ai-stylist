# ✨ StyleSync AI — Autonomous Personal Stylist & Virtual Wardrobe Assistant

[![Streamlit App](https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://stylesync-ai-stylist-mapfehqgw3anbcpqwzfv88.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-000000?style=for-the-badge)](https://www.langchain.com/langgraph)
[![Groq API](https://img.shields.io/badge/LLM-Groq_LLaMA_3-f34f29?style=for-the-badge)](https://groq.com/)
[![OpenCV](https://img.shields.io/badge/Vision-OpenCV-5C3EE8?style=for-the-badge&logo=opencv)](https://opencv.org/)

> **Live Application URL:** [https://stylesync-ai-stylist-mapfehqgw3anbcpqwzfv88.streamlit.app/](https://stylesync-ai-stylist-mapfehqgw3anbcpqwzfv88.streamlit.app/)

---

## 📌 Executive Summary & Purpose

**StyleSync AI** is an end-to-end, multimodal **Agentic AI System** engineered to address the distinct fashion, e-commerce, and custom tailoring challenges of the Pakistani retail ecosystem. 

Standard e-commerce recommendation engines rely on simple keyword filtering, ignoring individual physical geometry, real-world skin undertones, and local tailoring dynamics (unstitched 3-piece suites, neckline blueprints, dupattas, and footwear pairing). **StyleSync AI** bridges this gap by combining **Computer Vision (OpenCV & Pillow)** for skin tone/undertone extraction with a **LangGraph Agent Architecture** powered by high-speed **Groq LLaMA models** to produce actionable, hyper-personalized fashion advice and instant e-commerce deep-links.

---

## 📸 System Screenshots & Interface

| **Tab 1: Ready-To-Wear Brand Stylist** | **Tab 2: Unstitched Market Fabric Assistant** |
|:--------------------------------------:|:---------------------------------------------:|
| ![Brand Stylist Interface](https://raw.githubusercontent.com/placeholder/stylesync-ai/main/assets/brand_stylist.png) | ![Fabric Tailor Blueprint](https://raw.githubusercontent.com/placeholder/stylesync-ai/main/assets/fabric_assistant.png) |
| *Skin undertone classification & dynamic store links (Sapphire, Khaadi, J., etc.)* | *Custom stitching blueprints (galas, bottoms, laces) for unstitched fabric* |

---

## 🎯 The Real-World Problems We Solve

1. **Skin Tone & Color Palette Mismatch:**
   Shoppers frequently purchase colors that wash out their skin tone. StyleSync AI performs mathematical luminance and RGB analysis on selfie inputs to detect exact skin undertones (Warm, Cool, Neutral) and map them to flattering color palettes.
2. **Silhouette & Fit Flaws:**
   Inappropriate outfit cuts distort body geometry. StyleSync AI takes height, age, gender, and body shape parameters to suggest specific silhouettes (e.g., A-line, Straight Cut, Anarkali, Boxy Cut).
3. **Unstitched Fabric Tailoring Confusion:**
   Pakistan's multi-billion rupee unstitched fabric market leaves customers confused about how to stitch custom suits. StyleSync AI acts as a digital Master Tailor (Darzi), generating tailored blueprints covering necklines, sleeves, bottom styles, and accent lace trims.
4. **Scattered Brand Search:**
   Finding matching products across brands like **Sapphire, Khaadi, Gul Ahmed, J., Stylo,** and **Borjan** takes time. StyleSync AI programmatically constructs deep-filtered search URLs based on recommendation results.

---

## 🌟 Key Features

* 🧠 **Multimodal Perception Engine:** Real-time facial RGB extraction and skin undertone detection using OpenCV.
* ⚡ **LangGraph Stateful Orchestration:** Structured multi-node AI graph retaining execution context across `AgentState`.
* 🛡️ **Dual-API Key Resilience:** Built-in automatic failover between primary (`GROQ_API_KEY`) and secondary (`GROQ_API_KEY_2`) keys to prevent rate-limit downtime during live presentations.
* 🛍️ **E-Commerce Deep Linking:** Dynamic URL generation mapping user styling preferences directly to brand search endpoints (Khaadi, Sapphire, J., Gul Ahmed, Stylo, Borjan, Limelight, Outfitters).
* 🧵 **Market Tailor Blueprint Generator:** Custom stitching guides for unstitched 2-piece and 3-piece suits based on fabric pattern, texture, and occasion.
* 🎨 **Luxurious Boutique UI:** Custom Streamlit CSS theme with gold accents, responsive cards, visual body shape charts, and live camera input.

---

## 🏗️ System Architecture & Workflow

```
                        +---------------------------------------+
                        |             USER INPUT                |
                        | (Selfie Image / Cam + Body Parameters |
                        | + Brand Preference / Fabric Upload)   |
                        +---------------------------------------+
                                            |
                                            v
                        +---------------------------------------+
                        |      COMPUTER VISION PERCEPTION       |
                        |       (vision_utils.extract_tone)     |
                        |  - OpenCV RGB Matrix Calculation      |
                        |  - Luminance Formula Execution        |
                        |  - Undertone & Palette Mapping        |
                        +---------------------------------------+
                                            |
                                            v
                        +---------------------------------------+
                        |        LANGGRAPH AGENT STATE          |
                        |            (AgentState)               |
                        | Aggregates user metrics, skin tone,   |
                        | undertone, budget, and brand choices  |
                        +---------------------------------------+
                                            |
                                            v
                        +---------------------------------------+
                        |       REASONING & ACTION NODES        |
                        |  (brand_stylist_node / fabric_node)   |
                        |  - Dual Groq LLM Failover Execution   |
                        |  - Geometric Silhouette Matching      |
                        |  - Dynamic E-Commerce URL Synthesis   |
                        +---------------------------------------+
                                            |
                                            v
                        +---------------------------------------+
                        |        FINAL OUTPUT LOOKBOOK          |
                        |  - Tailored Recommendations           |
                        |  - Direct Brand Deep-Links            |
                        |  - Footwear & Jewelry Accessories     |
                        |  - Custom Stitching Blueprint         |
                        +---------------------------------------+
```

---

## 💻 Codebase Structure & Core Modules

```
StyleSync-AI/
├── app.py              # Main Streamlit UI, state management, & page layout
├── agent_brain.py      # LangGraph state machine, nodes, LLM logic & URL generator
├── vision_utils.py     # OpenCV computer vision skin tone & luminance logic
├── config.py           # Config loader & environment variable manager
├── requirements.txt    # Project dependencies
├── .env.example        # Environment variable template
└── README.md           # Comprehensive project documentation
```

---

### Module Breakdown

#### 1. `vision_utils.py` — Computer Vision Engine
Converts uploaded or live camera images into OpenCV matrices, extracts mean RGB channels over a centered ROI grid, calculates relative luminance, and assigns undertone classifications:

```python
import cv2
import numpy as np
from PIL import Image

def analyze_skin_tone(image: Image.Image):
    """
    Extracts skin tone, undertone, and recommended color palettes
    using OpenCV matrix calculations and luminance formula.
    """
    img_array = np.array(image.convert('RGB'))
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Calculate average RGB values
    avg_color_per_row = np.average(img_cv, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    b, g, r = avg_color[0], avg_color[1], avg_color[2]
    
    # Luminance formula: 0.299R + 0.587G + 0.114B
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    
    # Tone & Undertone Logic
    if luminance > 170:
        tone = "Fair / Light"
        palette = ["Pastel Pink", "Mint Green", "Soft Blue", "Lavender", "Peach"]
    elif luminance > 120:
        tone = "Wheatish / Medium"
        palette = ["Mustard Gold", "Teal", "Emerald Green", "Maroon", "Rust"]
    else:
        tone = "Deep / Dusky"
        palette = ["Royal Blue", "Deep Red", "Magenta", "Bright Yellow", "Emerald"]
        
    undertone = "Warm (Gold/Yellow)" if r > b else "Cool (Blue/Pink)"
    return tone, undertone, palette
```

#### 2. `agent_brain.py` — LangGraph Orchestration & URL Synthesis
Defines `AgentState`, compiles `StateGraph` workflows, handles multi-key Groq fallback, and synthesizes dynamic brand deep-links:

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import urllib.parse

class AgentState(TypedDict):
    gender: str
    height: str
    body_shape: str
    skin_tone: str
    undertone: str
    recommended_colors: list
    brand: str
    outfit_style: str
    budget: str
    pattern_choice: str
    result: str

def generate_brand_links(brand_name: str, search_term: str) -> str:
    """Generates direct filter links for local Pakistani e-commerce brands."""
    brand_urls = {
        "Khaadi": "https://pk.khaadi.com/search?q=",
        "Sapphire": "https://pk.sapphireonline.pk/search?q=",
        "Gul Ahmed": "https://www.gulahmedshop.com/catalogsearch/result/?q=",
        "Junaid Jamshed (J.)": "https://www.junaidjamshed.com/catalogsearch/result/?q=",
        "Limelight": "https://www.limelight.pk/search?q=",
        "Stylo Shoes": "https://www.stylo.pk/search?q=",
        "Borjan": "https://www.borjan.com.pk/search?q="
    }
    base = brand_urls.get(brand_name, "https://google.com/search?q=")
    encoded_query = urllib.parse.quote(search_term)
    return f"{base}{encoded_query}"
```

---

## 🛍️ Supported E-Commerce Brands

| Brand | Category | Features Integrated |
|:---|:---|:---|
| **Khaadi** | Pret / Unstitched | Direct catalog search URL synthesis |
| **Sapphire** | Pret / Daily Wear | Deep linking & seasonal color matching |
| **Junaid Jamshed (J.)** | Traditional / Modest | Kurta & Festive outfit search links |
| **Gul Ahmed** | Premium Unstitched | Lawn & Winter collection deep links |
| **Limelight** | Western / Fusion | Budget-friendly fast fashion linking |
| **Alkaram Studio** | Unstitched / Fabric | Color palette & print linking |
| **Stylo Shoes** | Footwear / Khussa | Heel height & traditional shoe pairing |
| **Borjan** | Footwear / Sandals | Men & Women footwear match links |

---

## 🛠️ Technology Stack

* **Frontend & UI:** Streamlit (1.32+), Custom HTML5, CSS3, FontAwesome 6
* **Agentic Framework:** LangGraph, LangChain Core
* **Large Language Models:** Groq LLM API (`LLaMA-3` series)
* **Computer Vision:** OpenCV (`opencv-python`), NumPy, Pillow
* **State & Environment:** Python-dotenv, Dynamic API Key Switcher

---

## 🚀 Installation & Local Setup

### Prerequisites
* Python `3.9` or higher
* A valid **Groq API Key** (Get one at [console.groq.com](https://console.groq.com))

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/StyleSync-AI.git
cd StyleSync-AI
```

### 2. Set Up Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY="your_primary_groq_api_key_here"
GROQ_API_KEY_2="your_secondary_groq_api_key_here_optional"
GROQ_MODEL="llama-3.3-70b-versatile"
```

### 5. Launch Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🤝 Authors & Credits

Developed as a flagship project exploring practical AI Agent Systems, Multimodal Computer Vision, and Domain-Specific E-Commerce Integration.

* **Developer & Author:** Palwasha Mushtaq
* **Live App Hosted On:** Streamlit Community Cloud
* **Project Repository:** [GitHub - StyleSync AI](https://github.com/your-username/StyleSync-AI)