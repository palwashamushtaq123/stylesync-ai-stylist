from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import config
import urllib.parse

def get_working_llm():
    """Tries Primary Key (1) and Backup Key (2) one by one with automatic fallback."""
    keys = []
    
    # 1. Pehli Primary Key check karein
    if hasattr(config, "GROQ_API_KEY") and config.GROQ_API_KEY:
        keys.append(config.GROQ_API_KEY)
        
    # 2. Doosri Backup Key check karein
    if hasattr(config, "GROQ_API_KEY_2") and config.GROQ_API_KEY_2:
        keys.append(config.GROQ_API_KEY_2)
        
    if not keys:
        keys = [""]
        
    # Keys ko aik aik kar ke try karein ge
    for key in keys:
        try:
            llm = ChatGroq(
                temperature=0.7,
                model_name=config.GROQ_MODEL,
                groq_api_key=key
            )
            return llm
        except Exception:
            continue
            
    # Agar dono fail ho jayein toh pehli wali return kar do
    return ChatGroq(
        temperature=0.7,
        model_name=config.GROQ_MODEL,
        groq_api_key=keys[0]
    )

def generate_style_recommendation(state: dict) -> str:
    llm = get_working_llm()
    
    brand_search_urls = {
        "Khaadi": "https://pk.khaadi.com/search?q=",
        "Sapphire": "https://pk.sapphireonline.pk/search?q=",
        "Gul Ahmed": "https://www.gulahmedshop.com/catalogsearch/result/?q=",
        "Junaid Jamshed (J.)": "https://www.junaidjamshed.com/catalogsearch/result/?q=",
        "Limelight": "https://www.limelight.pk/pages/search-results-page?q=",
        "Bonanza Satrangi": "https://www.bonanzasatrangi.com/search?q=",
        "Sana Safinaz": "https://www.sanasafinaz.com/pk/catalogsearch/result/?q=",
        "Alkaram Studio": "https://www.alkaramstudio.com/search?q=",
        "Outfitters": "https://www.outfitters.com.pk/search?q="
    }
    
    pattern_keyword = state['pattern_choice'].split('(')[0].strip()
    search_query = f"{pattern_keyword} {state['outfit_style']}".strip()
    encoded_query = urllib.parse.quote(search_query)
    
    base_url = brand_search_urls.get(state['brand'], "https://pk.khaadi.com/search?q=")
    exact_filtered_link = f"{base_url}{encoded_query}"
    
    stylo_link = f"https://www.stylo.pk/search?q={urllib.parse.quote(state['skin_tone'] + ' sandals')}"
    borjan_link = f"https://www.borjan.com.pk/search?q={urllib.parse.quote('khussa shoes')}"
    
    prompt = f"""
    You are an elite Pakistani Fashion Designer and Personal Stylist.
    
    User Profile:
    - Gender: {state['gender']}
    - Height: {state['height']}
    - Body Shape: {state['body_shape']}
    - Target Brand: {state['brand']}
    - Outfit Style: {state['outfit_style']}
    - Selected Print/Pattern: {state['pattern_choice']}
    - Skin Tone: {state['skin_tone']} ({state['undertone']})
    - Budget Range: {state['budget']}
    
    Task Requirements:
    1. **Direct Filtered Product Search Link:**
       - Direct Collection Search: [{state['brand']} {pattern_keyword} Collection]({exact_filtered_link})
    2. **Body Architecture & Height Compatibility Verdict:**
       - Clearly state "✅ SUITABLE" or "⚠️ NOT IDEAL" with fashion reasoning for {state['body_shape']} shape and {state['height']} height.
    3. **3 Outfit Recommendations (Within {state['budget']}):**
       - Detail outfit concept, specific fabric type, and price estimate.
    4. **Direct Shopping Links for Shoes & Accessories:**
       - Matching Shoes: [Browse Matching Footwear on Stylo]({stylo_link}) | [Browse Khussas on Borjan]({borjan_link})
       - Jewelry & Accessories: Provide specific color, metal (gold/silver/oxidized), and styling suggestions.
    """
    
    messages = [
        SystemMessage(content="You are a top Pakistani luxury fashion consultant."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content

def analyze_market_fabric(state: dict) -> str:
    llm = get_working_llm()
    
    prompt = f"""
    You are a master Pakistani Tailor and Fashion Designer.
    
    The user bought an unstitched fabric from the market and wants custom styling advice:
    - Gender: {state['gender']}
    - Height: {state['height']}
    - Body Shape: {state['body_shape']}
    - Skin Tone: {state['skin_tone']} ({state['undertone']})
    - Desired Vibe: {state['desired_vibe']}
    
    Provide a detailed stitching & styling plan:
    1. **Neckline & Sleeve Design:** (e.g., Angrakha gala, V-neck with organza lace, Tulip sleeves, Boxy cut)
    2. **Trouser / Bottom Cut:** (e.g., Straight cigarette pants, Tulip shalwar, Flared gharara)
    3. **Dupatta & Trimming Contrast:** Exact contrast lace, organza border, or tassel ideas.
    4. **Footwear & Accessories Match:** Exact khussa / heel color and jewelry pairing.
    5. **Final Look Concept Summary:** Describe the complete final stitched appearance based on their uploaded fabric.
    """
    
    messages = [
        SystemMessage(content="You are a master Pakistani boutique designer."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content