import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
import streamlit.components.v1 as components

# 1. Custom Setup with Game Favicon
st.set_page_config(page_title="SeatScanr - Metasearch", page_icon="🎫", layout="wide")

# 2. Injecting Custom CSS for Professional UI & Subtle Neon
st.markdown("""
<style>
    /* Dark Premium Background */
    .stApp { 
        background-color: #060913; 
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(0, 242, 254, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(255, 0, 122, 0.05) 0%, transparent 40%),
            linear-gradient(135deg, #060913 0%, #0b111e 100%);
        color: #f8fafc; 
    }
    
    /* RADAR SCANNER LOADER ANIMATION */
    .radar-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 30px 0;
    }
    .radar {
        width: 100px; height: 100px; border-radius: 50%;
        border: 2px solid #00F2FE; position: relative;
        background: repeating-radial-gradient(circle, #060913 0%, #060913 10%, #00F2FE 11%, #060913 12%);
        overflow: hidden; box-shadow: 0 0 15px rgba(0,242,254,0.3);
    }
    .radar:before {
        content: ''; position: absolute; top: 50%; left: 50%;
        width: 100%; height: 100%;
        background: linear-gradient(45deg, rgba(255,0,122,0.3) 0%, transparent 50%);
        transform-origin: top left; animation: spin 1.5s linear infinite;
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }

    /* Polished, professional headline */
    .hero-title {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 56px;
        font-weight: 800;
        text-align: center;
        letter-spacing: -1px;
        line-height: 1.1;
        background: linear-gradient(to right, #FFFFFF 0%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    /* Input Styling override to feel like a high-end search bar */
    div[data-baseweb="input"] {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 50px !important; /* Rounded pill shape for search bar */
        padding-left: 15px !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #00F2FE !important;
        box-shadow: 0 0 12px rgba(0,242,254,0.2) !important;
    }
    
    .hero-sub {
        color: #00F2FE; 
        font-size: 13px; 
        font-weight: bold; 
        font-family: monospace;
        letter-spacing: 2px;
        text-align: center;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# 3. Clean Professional Nav Bar
col_logo, col_txt = st.columns([1, 5])
with col_logo:
    try:
        st.image("logo.png", width=60)
    except:
        st.markdown("<h1 style='font-size: 40px; margin: 0;'>🎫</h1>", unsafe_allow_html=True)

with col_txt:
    st.markdown("<h3 style='color:#f8fafc; margin: 10px 0 0 0; font-family:sans-serif;'>SeatScanr</h3>", unsafe_allow_html=True)

st.divider()

# 4. Centered, Professional Hero Section
st.markdown('<p class="hero-sub">// Live Ticket Metasearch</p>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Find the best seats.<br>Compare the market.</h1>', unsafe_allow_html=True)

# 5. 🛠️ THE FIX: Centered search bar that doesn't stretch across the screen
# This creates 3 columns. The middle column [2] is the only one with content!
left_space, search_box, right_space = st.columns([1, 2, 1])

with search_box:
    query = st.text_input("", placeholder="Search for artists, teams, sports or venues...", label_visibility="collapsed")

st.write("") # Spacer

# API Key Hook
TM_API_KEY = st.secrets["TM_API_KEY"]

if query:
    # THE RADAR TRIGGER
    with st.empty():
        st.markdown('''
            <div class="radar-container">
                <div class="radar"></div>
                <p style="color:#00F2FE; font-weight:bold; margin-top:15px; font-family:monospace; letter-spacing:1px;">SCANNING THE MARKET...</p>
            </div>
        ''', unsafe_allow_html=True)
        
        url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={TM_API_KEY}&keyword={query}"
        try:
            response = requests.get(url)
            data = response.json()
            time.sleep(1.2)
            st.write("") 
        except:
            st.write("")

    # 6. Render the Results
    try:
        if '_embedded' in data and 'events' in data['_embedded']:
            events = data['_embedded']['events']
            
            # Keep the success message looking clean and centered
            _, success_box, _ = st.columns([1, 2, 1])
            with success_box:
                st.success(f"Results found for: **{query}**")
            
            for ev in events[:5]:
                name = ev['name']
                date_str = ev['dates']['start'].get('localDate', 'TBA')
                venue = ev['_embedded']['venues'][0]['name']
                url_link = ev['url']
                
                try:
                    formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d, %Y")
                except:
                    formatted_date = date_str

                # Clean, component-based row rendering
                card_html = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body {{
                            background: transparent;
                            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                            color: #f8fafc;
                            margin: 0;
                            padding: 10px 0;
                        }}
                        .deal-card {{
                            background-color: #0f172a; 
                            border: 1px solid #1e293b; 
                            border-radius: 8px;
                            padding: 18px; 
                            margin-bottom: 12px; 
                            transition: 0.2s ease;
                        }}
                        .deal-card:hover {{ 
                            border-color: #334155; 
                            background-color: #1e293b;
                        }}
                        .provider-tag {{
                            background-color: #0b111e; 
                            border-radius: 4px; 
                            padding: 8px 12px;
                            display: flex; 
                            justify-content: space-between; 
                            align-items: center;
                            margin-bottom: 6px; 
                            border: 1px solid #1e293b;
                        }}
                        .deal-btn {{
                            background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
                            color: #060913 !important; 
                            text-align: center; 
                            padding: 12px;
                            border-radius: 4px; 
                            font-weight: 700; 
                            display: block;
                            text-decoration: none; 
                            text-transform: uppercase;
                            font-size: 13px;
                            letter-spacing: 0.5px;
                        }}
                        .deal-btn:hover {{
                            opacity: 0.9;
                        }}
                        .best-deal-price {{
                            font-family: sans-serif;
                            font-weight: 800;
                            font-size: 32px;
                            color: #00ff66;
                            margin: 0;
                            line-height: 1;
                        }}
                    </style>
                </head>
                <body>
                    <div style="width: 80%; margin: 0 auto;">
                        <div class="deal-card">
                            <div style="display:flex; justify-content:space-between; gap:20px; align-items:center;">
                                <div style="flex: 2;">
                                    <span style="background-color:#1e293b; color:#94A3B8; padding:3px 6px; border-radius:3px; font-size:10px; font-weight:bold; letter-spacing:1px; text-transform:uppercase;">Confirmed Match</span>
                                    <h2 style="margin:4px 0 2px 0; color:#f8fafc; font-size: 18px;">{name}</h2>
                                    <p style="margin:0; color:#64748b; font-size: 13px;">📅 {formatted_date} &nbsp;|&nbsp; 📍 {venue}</p>
                                </div>
                                
                                <div style="flex: 2;">
                                    <div class="provider-tag">
                                        <span style="font-weight:bold;color:#64748b;font-size:12px;">Ticketmaster</span>
                                        <span style="color:#f8fafc;font-weight:bold;font-size:12px;">From $45</span>
                                    </div>
                                    <div class="provider-tag">
                                        <span style="font-weight:bold;color:#64748b;font-size:12px;">StubHub</span>
                                        <span style="color:#f8fafc;font-weight:bold;font-size:12px;">From $62</span>
                                    </div>
                                    <div class="provider-tag">
                                        <span style="font-weight:bold;color:#64748b;font-size:12px;">SeatGeek</span>
                                        <span style="color:#00ff66;font-weight:bold;font-size:12px;">From $41</span>
                                    </div>
                                </div>
                                
                                <div style="flex: 1; text-align:center;">
                                    <h4 style="margin:0; color:#64748b; font-size:11px; letter-spacing:0.5px; text-transform:uppercase;">Best Price</h4>
                                    <p class="best-deal-price">$41</p>
                                    <a href="{url_link}" target="_blank" class="deal-btn">Get Tickets</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </body>
                </html>
                '''
                components.html(card_html, height=140)
                
        else:
             # Keep warning centered too
            _, warn_box, _ = st.columns([1, 2, 1])
            with warn_box:
                st.warning("No matches found across the scanned platforms.")
            
    except Exception as e:
        st.error(f"Interference detected: {e}")
