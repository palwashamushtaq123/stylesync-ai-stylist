# StyleSync AI - Autonomous Personal Stylist & Virtual Wardrobe Assistant

StyleSync AI is an intelligent multimodal AI Agent designed to solve personal fashion styling challenges in the Pakistani retail market. By combining Computer Vision (OpenCV) for precise skin tone/undertone detection with Large Language Models (Groq LLM) for body shape geometry analysis, StyleSync AI delivers hyper-personalized outfit recommendations, direct brand search links, footwear/accessory pairings, and custom market fabric tailoring blueprints.

---

## 🌟 Key Features

1. **Multimodal Skin Tone & Undertone Analysis**
   - Uses Computer Vision to extract average RGB matrix values and calculate luminance.
   - Automatically determines skin tone category, undertone (Warm/Cool), and recommended color palettes.

2. **Brand Catalog Stylist Mode**
   - Supports top Pakistani brands: *Khaadi, Sapphire, Gul Ahmed, Junaid Jamshed (J.), Limelight, Bonanza Satrangi, Sana Safinaz, Alkaram Studio, Outfitters*.
   - Considers height, age, gender, body shape, preferred print style, and budget.
   - Generates exact filtered deep links directly to brand search pages and footwear stores (*Stylo, Borjan*).

3. **Market Unstitched Fabric Tailor Assistant**
   - Allows users to upload unstitched fabric bought from local markets.
   - Generates custom stitching blueprints (necklines, sleeve styles, bottom cuts, trimmings/laces) tailored to body shape and event vibe.

4. **Luxurious Boutique UI**
   - Streamlit interface styled with custom CSS, visual body shape guides, dynamic print showcases, and interactive elements.

---

## 🏗️ AI Agent Workflow & Architecture

```
[ User Input ]
 (Skin Image + Fabric/Brand Preferences + Body Metrics)
       │
       ▼
[ Computer Vision Node ] ──► (OpenCV / NumPy RGB & Luminance Analysis)
       │
       ▼
[ State Aggregation ] ──► (Stores User Metrics, Undertones, & Palette)
       │
       ▼
[ Reasoning & Action Node ] ──► (Groq LLM Reasoning + Direct Link Generation)
       │
       ▼
[ Final Response Node ] ──► (Structured Lookbook, Direct Store Links & Tailor Blueprint)
```

---

## 📂 Repository Structure

```
├── app.py              # Main Streamlit web application & UI
├── agent_brain.py      # LLM logic & URL generation functions
├── vision_utils.py     # OpenCV computer vision logic for skin tone extraction
├── config.py           # Configuration manager & environment variable loader
├── requirements.txt    # Required Python libraries
├── .env.example        # Example environment setup
└── README.md           # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- A Groq API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/StyleSync-AI.git
   cd StyleSync-AI
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory (refer to `.env.example`):
   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   GROQ_MODEL=openai/gpt-oss-20b
   ```

5. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

---

## 🛠️ Tech Stack

- **Frontend/Framework:** Streamlit, Custom HTML/CSS
- **AI / Orchestration:** LangChain Core, Groq API (`openai/gpt-oss-20b`)
- **Computer Vision:** OpenCV (`opencv-python`), NumPy, Pillow
- **Environment Management:** `python-dotenv`

---

## 👥 Presentation & Assignment Context

Designed as a group project on AI Agent Systems. It highlights practical AI workflow concepts including:
- Perception (Computer Vision)
- State Management
- Decision-making (LLM Reasoning)
- Action Execution (Dynamic Link Synthesis)

---
