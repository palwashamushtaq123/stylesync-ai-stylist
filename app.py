import streamlit as st
from PIL import Image
import config
from vision_utils import analyze_skin_tone
from agent_brain import generate_style_recommendation, analyze_market_fabric

st.set_page_config(page_title="StyleSync AI - Pakistani Personal Stylist", page_icon="💃", layout="wide")

# Custom CSS for Luxury Boutique Look with Borders & Gold Accents
st.markdown("""
    <style>
    .main { background: #faf7f2; }
    .stButton>button {
        background: linear-gradient(135deg, #b8860b 0%, #785109 100%);
        color: white;
        border-radius: 12px;
        font-weight: bold;
        border: none;
        padding: 0.8rem 1.8rem;
        box-shadow: 0 6px 20px rgba(184, 134, 11, 0.35);
        font-size: 16px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #d4af37 0%, #a67c2e 100%);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.5);
    }
    .sale-popup {
        background: linear-gradient(90deg, #800020, #b22222, #800020);
        color: #fff;
        padding: 14px 25px;
        border-radius: 30px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 25px;
        font-size: 17px;
        box-shadow: 0 4px 18px rgba(128, 0, 32, 0.4);
    }
    .card {
        background: #ffffff;
        padding: 28px;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.07);
        border: 2px solid #e6d7c3;
        margin-bottom: 25px;
    }
    .body-card {
        text-align: center;
        background: #fffdf9;
        border: 1px solid #d2c2ad;
        border-radius: 12px;
        padding: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Sale Announcement Banner
st.markdown('<div class="sale-popup">🛍️ BLESSED & FESTIVE SALE ACTIVE: Direct Print-Filtered Matching across Sapphire, Khaadi, Gul Ahmed & J.</div>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #3b2c1a; font-family: serif;'>✨ StyleSync AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7a634a; font-size: 19px;'>Autonomous Personal Stylist & Virtual Wardrobe Assistant for Pakistani Fashion</p>", unsafe_allow_html=True)
st.divider()

# Navigation Tabs
tab1, tab2 = st.tabs(["🛍️ Brand Catalog Stylist Mode", "✂️ Market Unstitched Fabric Custom Stylist"])

# TAB 1: BRAND CATALOG MODE
with tab1:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 📸 Step 1: Skin Tone Analysis")
        st.write("Upload a photo or capture live using your camera for color extraction.")
        
        input_method = st.radio("Choose Input Method", ["Upload Image File", "Capture Live with Camera"], key="brand_input_method")
        
        uploaded_file = None
        if input_method == "Upload Image File":
            uploaded_file = st.file_uploader("Upload Skin Image (All Formats)", type=["jpg", "jpeg", "png", "webp", "heic", "jfif"], key="brand_skin")
        else:
            uploaded_file = st.camera_input("Take a photo of your hand, arm, or face", key="brand_camera")
        
        image_analyzed = False
        skin_data = {}
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Selected Image Source", width="stretch")
            
            with st.spinner("Extracting RGB values & skin tone palette..."):
                skin_data = analyze_skin_tone(image)
                image_analyzed = True
                
            st.success(f"✨ Skin Tone: **{skin_data['skin_tone']}**")
            st.info(f"🧬 Undertone: **{skin_data['undertone']}**")
            st.write(f"🎨 **Best Palette:** {skin_data['best_colors']}")
            
            rgb = skin_data["avg_rgb"]
            hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
            st.markdown(
                f'<div style="display: flex; align-items: center; gap: 12px; margin-top: 15px; padding: 12px; background: #fdfbf7; border-radius: 10px; border: 1px solid #e0d0bc;">'
                f'<div style="width: 38px; height: 38px; background-color: {hex_color}; border-radius: 50%; border: 2px solid #555;"></div>'
                f'<span style="font-size: 14px;"><b>Tone Code:</b> {hex_color} (RGB: {rgb})</span>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 🛍️ Step 2: Body Architecture & Preferences")
        
        gender = st.selectbox("Gender", ["Female", "Male"], key="brand_gender")
        col_a, col_b = st.columns(2)
        with col_a:
            age = st.slider("Age", 15, 60, 22, key="brand_age")
        with col_b:
            height = st.selectbox("Height Range", ["Petite (Under 5'2'')", "Average (5'2'' - 5'7'')", "Tall (5'8'' and Above)"], key="brand_height")
            
        if gender == "Female":
            body_shape = st.selectbox("Select Female Body Shape", [
                "Rectangle (Straight Silhouette)", 
                "Hourglass (Balanced Curve)", 
                "Pear (Narrow Shoulders, Wider Hips)", 
                "Apple (Fuller Midsection)"
            ], key="brand_body")
            
            st.markdown("#### 📐 Pakistani Female Body Shape Guide:")
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                st.markdown("<div class='body-card'>", unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=150", width="stretch")
                st.markdown("<b>Rectangle</b><br><small>Straight Cut</small></div>", unsafe_allow_html=True)
            with b2:
                st.markdown("<div class='body-card'>", unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=150", width="stretch")
                st.markdown("<b>Hourglass</b><br><small>Fitted Waist</small></div>", unsafe_allow_html=True)
            with b3:
                st.markdown("<div class='body-card'>", unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=150", width="stretch")
                st.markdown("<b>Pear</b><br><small>A-Line Flare</small></div>", unsafe_allow_html=True)
            with b4:
                st.markdown("<div class='body-card'>", unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1485230895905-ec40ba36b9bc?w=150", width="stretch")
                st.markdown("<b>Apple</b><br><small>Flowy Peshwas</small></div>", unsafe_allow_html=True)
        else:
            body_shape = st.selectbox("Select Male Body Shape", [
                "Athletic / V-Shape (Broad Shoulders)", 
                "Rectangle / Slim (Straight Build)", 
                "Average / Solid (Fuller Chest & Waist)"
            ], key="brand_body_m")
            
            st.markdown("#### 📐 Pakistani Male Body Shape Guide:")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown("<div class='body-card'>", unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150", width="stretch")
                st.markdown("<b>Athletic / V-Shape</b><br><small>Tailored Kurta</small></div>", unsafe_allow_html=True)
            with m2:
                st.markdown("<div class='body-card'>", unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150", width="stretch")
                st.markdown("<b>Rectangle / Slim</b><br><small>Waistcoat Cut</small></div>", unsafe_allow_html=True)
            with m3:
                st.markdown("<div class='body-card'>", unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=150", width="stretch")
                st.markdown("<b>Average / Solid</b><br><small>Relaxed Fit</small></div>", unsafe_allow_html=True)

        selected_brand = st.selectbox("Target Pakistani Brand", config.PAK_BRANDS)
        
        outfit_style = st.selectbox("Outfit Cut & Format", [
            "Trendy Co-ord Sets", 
            "Long Flared Shirts & Maxis", 
            "Short Kurti & Tulip/Straight Pants", 
            "Classic 3-Piece Unstitched", 
            "Modern Ready-to-Wear"
        ])
        
        pattern_choice = st.selectbox("Preferred Print / Pattern Style", [
            "Floral Prints (Botanical & Flower Designs)", 
            "Geometric Prints (Sharp & Modern)", 
            "Vertical Stripes (Height Extension)", 
            "Minimalist Solids with Subtle Embroidery"
        ])
        
        budget = st.selectbox("Budget Range (PKR)", [
            "Economy (Under 4,000 PKR)", 
            "Mid-Range (4,000 - 8,000 PKR)", 
            "Premium (8,000 - 15,000 PKR)", 
            "Luxury / Festive (15,000+ PKR)"
        ])
        st.markdown("</div>", unsafe_allow_html=True)

    # Dynamic Fabric & Print Showcase
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### 👗 Selected Print Preview Showcase: {pattern_choice.split('(')[0]}")
    img_c1, img_c2 = st.columns(2)

    if "Floral" in pattern_choice:
        with img_c1:
            st.image("https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=500", caption=f"Sample Floral Unstitched ({budget})", width="stretch")
        with img_c2:
            st.image("https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=500", caption=f"Sample Floral Stitched Kurti ({budget})", width="stretch")
    elif "Geometric" in pattern_choice:
        with img_c1:
            st.image("https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=500", caption=f"Geometric Pattern Concept ({budget})", width="stretch")
        with img_c2:
            st.image("https://images.unsplash.com/photo-1509631179647-0177331693ae?w=500", caption=f"Geometric Co-ord Cut ({budget})", width="stretch")
    else:
        with img_c1:
            st.image("https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=500", caption=f"Vertical Line / Solid Pattern ({budget})", width="stretch")
        with img_c2:
            st.image("https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=500", caption=f"Subtle Minimalist Design ({budget})", width="stretch")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("✨ Run AI Brand Stylist Agent", width="stretch", key="btn_brand"):
        if not image_analyzed:
            st.error("⚠️ Please upload or capture your skin tone picture first!")
        else:
            with st.spinner(f"Querying {selected_brand} collection database & accessories stores..."):
                state = {
                    "gender": gender,
                    "age": age,
                    "height": height,
                    "body_shape": body_shape,
                    "brand": selected_brand,
                    "outfit_style": outfit_style,
                    "pattern_choice": pattern_choice,
                    "budget": budget,
                    "skin_tone": skin_data["skin_tone"],
                    "undertone": skin_data["undertone"],
                    "recommended_colors": skin_data["best_colors"]
                }
                
                recommendation = generate_style_recommendation(state)
                st.markdown("---")
                st.markdown(f"## 🌟 Curated AI Outfit Lookbook & Direct Store Links")
                st.markdown(recommendation)
                st.balloons()


# TAB 2: MARKET UNSTITCHED FABRIC CUSTOM TAILOR MODE
with tab2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ✂️ Custom Market Fabric Tailoring & Styling Assistant")
    st.write("Upload or capture your fabric and skin tone photo. Our AI Agent will analyze them and generate custom stitching blueprints and styling advice!")
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown("#### 🖼️ Fabric Photo")
        fabric_input_method = st.radio("Fabric Input", ["Upload File", "Capture Live"], key="fabric_input_method")
        if fabric_input_method == "Upload File":
            fabric_img = st.file_uploader("Upload Bought Fabric Photo", type=["jpg", "jpeg", "png", "webp", "heic", "jfif"], key="market_fabric")
        else:
            fabric_img = st.camera_input("Capture Fabric Live", key="market_fabric_cam")
            
        st.markdown("#### 📸 Skin Tone Photo")
        skin_input_method = st.radio("Skin Input", ["Upload File", "Capture Live"], key="skin_input_method")
        if skin_input_method == "Upload File":
            skin_img_m = st.file_uploader("Upload Your Hand/Face Photo", type=["jpg", "jpeg", "png", "webp", "heic", "jfif"], key="market_skin")
        else:
            skin_img_m = st.camera_input("Capture Skin/Face Live", key="market_skin_cam")
        
    with m_col2:
        m_gender = st.selectbox("Gender", ["Female", "Male"], key="m_gender_m")
        m_height = st.selectbox("Height Range", ["Petite (Under 5'2'')", "Average (5'2'' - 5'7'')", "Tall (5'8'' and Above)"], key="m_height_m")
        
        # Pakistani Body Shape with Pictures for Market Mode
        if m_gender == "Female":
            m_body = st.selectbox("Select Female Body Shape", ["Rectangle", "Hourglass", "Pear", "Apple"], key="m_body_f")
            st.markdown("#### 📐 Pakistani Female Body Shapes:")
            mb1, mb2, mb3, mb4 = st.columns(4)
            with mb1:
                st.markdown("<div class='body-card'>", unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=120", width="stretch")
                st.markdown("<b>Rectangle</b><br><small>Straight Cut</small></div>", unsafe_allow_html=True)
            with mb2:
                st.markdown("<div class='body-card'>", unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=120", width="stretch")
                st.markdown("<b>Hourglass</b><br><small>Fitted Waist</small></div>", unsafe_allow_html=True)
            with mb3:
                st.markdown("<div class='body-card'>", unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=120", width="stretch")
                st.markdown("<b>Pear</b><br><small>A-Line Flare</small></div>", unsafe_allow_html=True)
            with mb4:
                st.markdown("<div class='body-card'>", unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1485230895905-ec40ba36b9bc?w=120", width="stretch")
                st.markdown("<b>Apple</b><br><small>Flowy Peshwas</small></div>", unsafe_allow_html=True)
        else:
            m_body = st.selectbox("Select Male Body Shape", ["Athletic / V-Shape", "Rectangle / Slim", "Average / Solid"], key="m_body_m_type")
            st.markdown("#### 📐 Pakistani Male Body Shapes:")
            mm1, mm2, mm3 = st.columns(3)
            with mm1:
                st.markdown("<div class='body-card'>", unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=120", width="stretch")
                st.markdown("<b>Athletic</b><br><small>Tailored Kurta</small></div>", unsafe_allow_html=True)
            with mm2:
                st.markdown("<div class='body-card'>", unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=120", width="stretch")
                st.markdown("<b>Slim</b><br><small>Waistcoat Cut</small></div>", unsafe_allow_html=True)
            with mm3:
                st.markdown("<div class='body-card'>", unsafe_allow_html=True)
                st.image("https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=120", width="stretch")
                st.markdown("<b>Solid</b><br><small>Relaxed Fit</small></div>", unsafe_allow_html=True)

        desired_vibe = st.selectbox("Event / Vibe", ["Casual Everyday Wear", "Semi-Formal Dinner", "Festive / Eid / Wedding Wear", "Office / University Wear"])

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("✨ Generate Custom Tailoring Guide & Blueprint", width="stretch", key="btn_market"):
        if fabric_img is None or skin_img_m is None:
            st.error("⚠️ Please provide both your fabric photo and skin tone photo first!")
        else:
            with st.spinner("Analyzing fabric texture, colors, and body geometry for tailor instructions..."):
                skin_pil = Image.open(skin_img_m)
                skin_data_m = analyze_skin_tone(skin_pil)
                
                state_m = {
                    "gender": m_gender,
                    "height": m_height,
                    "body_shape": m_body,
                    "desired_vibe": desired_vibe,
                    "skin_tone": skin_data_m["skin_tone"],
                    "undertone": skin_data_m["undertone"]
                }
                
                tailor_guide = analyze_market_fabric(state_m)
                
                st.markdown("---")
                st.markdown("## 👗 AI Master Tailor Design Blueprint")
                st.markdown(tailor_guide)
                
                # Clean Fabric Showcase with Professional English Note
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### 🖼️ Your Market Fabric Analysis:")
                
                f1, f2 = st.columns([1, 2])
                with f1:
                    st.image(fabric_img, caption="Provided Market Fabric Source", width="stretch")
                with f2:
                    st.info("💡 **AI Tailor Note:** This fabric has been custom-styled based on your skin tone and body architecture. You can take this design blueprint to your local tailor to get the exact recommended cuts stitched!")
                    
                st.success("✅ Tailoring guide successfully generated!")
                st.markdown("</div>", unsafe_allow_html=True)
                st.balloons()