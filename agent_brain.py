from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import config
import urllib.parse
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# Define Agent State schema for LangGraph
class AgentState(TypedDict):
    gender: str
    age: int
    height: str
    body_shape: str
    brand: str
    outfit_style: str
    pattern_choice: str
    budget: str
    skin_tone: str
    undertone: str
    recommended_colors: str
    desired_vibe: str
    result: str

def get_working_llm():
    """Tries Primary Key (1) and Backup Key (2) one by one with automatic fallback."""
    keys = []
    if hasattr(config, "GROQ_API_KEY") and config.GROQ_API_KEY:
        keys.append(config.GROQ_API_KEY)
    if hasattr(config, "GROQ_API_KEY_2") and config.GROQ_API_KEY_2:
        keys.append(config.GROQ_API_KEY_2)
    if not keys:
        keys = [""]
        
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
            
    return ChatGroq(
        temperature=0.7,
        model_name=config.GROQ_MODEL,
        groq_api_key=keys[0]
    )

# --- LangGraph Node 1: Brand Stylist Decision Node ---
def brand_stylist_node(state: AgentState) -> AgentState:
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
    
    pattern_keyword = state.get('pattern_choice', '').split('(')[0].strip()
    search_query = f"{pattern_keyword} {state.get('outfit_style', '')}".strip()
    encoded_query = urllib.parse.quote(search_query)
    
    base_url = brand_search_urls.get(state.get('brand', 'Khaadi'), "https://pk.khaadi.com/search?q=")
    exact_filtered_link = f"{base_url}{encoded_query}"
    
    stylo_link = f"https://www.stylo.pk/search?q={urllib.parse.quote(state.get('skin_tone', '') + ' sandals')}"
    borjan_link = f"https://www.borjan.com.pk/search?q={urllib.parse.quote('khussa shoes')}"
    
    prompt = f"""
    You are an elite Pakistani Fashion Designer and Personal Stylist.
    
    User Profile:
    - Gender: {state.get('gender')}
    - Height: {state.get('height')}
    - Body Shape: {state.get('body_shape')}
    - Target Brand: {state.get('brand')}
    - Outfit Style: {state.get('outfit_style')}
    - Selected Print/Pattern: {state.get('pattern_choice')}
    - Skin Tone: {state.get('skin_tone')} ({state.get('undertone')})
    - Budget Range: {state.get('budget')}
    
    Task Requirements:
    1. **Direct Filtered Product Search Link:**
       - Direct Collection Search: [{state.get('brand')} {pattern_keyword} Collection]({exact_filtered_link})
    2. **Body Architecture & Height Compatibility Verdict:**
       - Clearly state "✅ SUITABLE" or "⚠️ NOT IDEAL" with fashion reasoning for {state.get('body_shape')} shape and {state.get('height')} height.
    3. **3 Outfit Recommendations (Within {state.get('budget')}):**
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
    state['result'] = response.content
    return state

# --- LangGraph Node 2: Market Fabric Tailor Node ---
def market_fabric_node(state: AgentState) -> AgentState:
    llm = get_working_llm()
    
    prompt = f"""
    You are a master Pakistani Tailor and Fashion Designer.
    
    The user bought an unstitched fabric from the market and wants custom styling advice:
    - Gender: {state.get('gender')}
    - Height: {state.get('height')}
    - Body Shape: {state.get('body_shape')}
    - Skin Tone: {state.get('skin_tone')} ({state.get('undertone')})
    - Desired Vibe: {state.get('desired_vibe')}
    
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
    state['result'] = response.content
    return state

# --- Building LangGraph Workflows with Explicit Nodes & Edges ---

# 1. Brand Stylist Graph Pipeline
brand_workflow = StateGraph(AgentState)
brand_workflow.add_node("brand_stylist_node", brand_stylist_node)
brand_workflow.add_edge(START, "brand_stylist_node")
brand_workflow.add_edge("brand_stylist_node", END)
compiled_brand_graph = brand_workflow.compile()

# 2. Market Fabric Tailor Graph Pipeline
market_workflow = StateGraph(AgentState)
market_workflow.add_node("market_fabric_node", market_fabric_node)
market_workflow.add_edge(START, "market_fabric_node")
market_workflow.add_edge("market_fabric_node", END)
compiled_market_graph = market_workflow.compile()

# --- Public Wrapper Functions called by app.py ---
def generate_style_recommendation(state_dict: dict) -> str:
    final_state = compiled_brand_graph.invoke(state_dict)
    return final_state.get('result', '')

def analyze_market_fabric(state_dict: dict) -> str:
    final_state = compiled_market_graph.invoke(state_dict)
    return final_state.get('result', '')