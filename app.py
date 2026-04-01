import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
import streamlit.components.v1 as components

# 1. Custom Setup with Game Favicon
st.set_page_config(page_title="SeatScanr - Metasearch", page_icon="🎫", layout="wide")

# 2. Injecting Custom CSS for "The Show" Neon Game Aesthetic
st.markdown("""
<style>
    /* "The Show" Background with glowing geometric neon overlays */
    .stApp { 
        background-color: #060913; 
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(0, 242, 254, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(255, 0, 122, 0.15) 0%, transparent 50%),
            linear-gradient(135deg, #060913 0%, #0b1528 100%);
        color: #f8fafc; 
    }
    
    /* RADAR SCANNER LOADER ANIMATION */
    .radar-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 30px 0;
    }
    .radar {
        width: 120px; height: 120px; border-radius: 50%;
        border: 2px solid #FF007A; position: relative;
        background: repeating-radial-gradient(circle, #060913 0%, #060913 10%, #00F2FE 11%, #060913 12%);
        overflow: hidden; box-shadow: 0 0 25px rgba(0,242,254,0.4);
    }
    .radar:before {
        content: ''; position: absolute; top: 50%; left: 50%;
        width: 100%; height: 100%;
        background: linear-gradient(45deg, rgba(255,0,122,0.4) 0%, transparent 50%);
        transform-origin: top left; animation: spin 1.5s linear infinite;
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }

    /* Massive Search Title (Game Style) */
    .game-hero-title {
        font-family: 'Impact', 'Arial Black', sans-serif;
        font-size: 72px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -2px;
        line-height: 0.9;
        background: linear-gradient(to bottom, #FFFFFF 0%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        text-shadow: 0px 10px 20px rgba(0,0,0,0.5);
    }
    
    /* Input Styling override to feel like a console UI */
    div[data-baseweb="input"] {
        background-color: #111827 !important;
        border: 2px solid #334155 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #00F2FE !important;
        box-shadow: 0 0 10px rgba(0,242,254,0.3) !important;
    }
    
    /* Subtext for Game UI */
    .game-sub {
        color: #00F2FE; 
        font-size: 14px; 
        font-weight: bold; 
        font-family: monospace;
        letter-spacing: 3px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header / Nav Bar
col_logo, col_txt = st.columns([1, 5])
with col_logo:
    try:
        st.image("logo.png", width=80)
    except:
        st.markdown("<h1 style='font-size: 50px; margin: 0;'>🎮</h1>", unsafe_allow_html=True)

with col_txt:
    st.markdown("<p style='color:#FF007A; font-size:12px; margin-bottom:0; font-weight:bold; letter-spacing:2px;'>LIVE TICKET AGGREGATOR</p>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#f8fafc; margin-top:0; font-family:Arial Black;'>SEATSCANR</h2>", unsafe_allow_html=True)

st.divider()

# 4. Big "The Show" Style Landing Hero
st.markdown('<p class="game-sub">// SECURE THE BEST SEATS</p>', unsafe_allow_html=True)
st.markdown('<h1 class="game-hero-title">FIND YOUR<br>NEXT EVENT</h1>', unsafe_allow_html=True)

# 5. Search Bar
query = st.text_input("", placeholder="Search for artists, teams, sports or venues...", label_visibility="collapsed")

# API Key Hook
TM_API_KEY = st.secrets["TM_API_KEY"]

if query:
    # THE RADAR TRIGGER
    with st.empty():
        st.markdown('''
            <div class="radar-container">
                <div class="radar"></div>
                <p style="color:#FF007A; font-weight:bold; margin-top:15px; font-family:monospace; letter-spacing:1px;">FETCHING LIVE MARKET DATA...</p>
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
            
            st.markdown(f"<p class='game-sub'>// SCAN COMPLETE: {len(events)} MATCHES</p>", unsafe_allow_html=True)
            
            for ev in events[:5]:
                name = ev['name']
                date_str = ev['dates']['start'].get('localDate', 'TBA')
                venue = ev['_embedded']['venues'][0]['name']
                url_link = ev['url']
                
                try:
                    formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d, %Y")
                except:
                    formatted_date = date_str

                # NEW BULLETPROOF HTML RENDERER
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
                            border: 1px solid #334155; 
                            border-radius: 8px;
                            padding: 18px; 
                            margin-bottom: 15px; 
                            transition: 0.2s ease;
                            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                        }}
                        .deal-card:hover {{ 
                            border-color: #00F2FE; 
                            box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
                            transform: translateY(-2px);
                        }}
                        .provider-tag {{
                            background-color: #1e293b; 
                            border-radius: 4px; 
                            padding: 8px 12px;
                            display: flex; 
                            justify-content: space-between; 
                            align-items: center;
                            margin-bottom: 6px; 
                            border: 1px solid #475569;
                        }}
                        .deal-btn {{
                            background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
                            color: #060913 !important; 
                            text-align: center; 
                            padding: 12px;
                            border-radius: 4px; 
                            font-weight: 900; 
                            display: block;
                            text-decoration: none; 
                            text-transform: uppercase;
                            font-size: 14px;
                            letter-spacing: 1px;
                        }}
                        .deal-btn:hover {{
                            opacity: 0.9;
                        }}
                        .best-deal-price {{
                            font-family: 'Impact', sans-serif;
                            font-size: 36px;
                            color: #00ff66;
                            margin: 0;
                            line-height: 1;
                        }}
                    </style>
                </head>
                <body>
                    <div class="deal-card">
                        <div style="display:flex; justify-content:space-between; gap:20px; align-items:center;">
                            <div style="flex: 2;">
                                <span style="background-color:#FF007A; color:white; padding:2px 6px; border-radius:3px; font-size:10px; font-weight:bold; letter-spacing:1px; text-transform:uppercase;">Live Match</span>
                                <h2 style="margin:4px 0 2px 0; color:#f8fafc; font-size: 20px;">{name}</h2>
                                <p style="margin:0; color:#94A3B8; font-size: 13px;">📅 {formatted_date} &nbsp;|&nbsp; 📍 {venue}</p>
                            </div>
                            
                            <div style="flex: 2;">
                                <div class="provider-tag">
                                    <span style="font-weight:bold;color:#94A3B8;font-size:12px;">Ticketmaster</span>
                                    <span style="color:#f8fafc;font-weight:bold;font-size:12px;">From $45</span>
                                </div>
                                <div class="provider-tag">
                                    <span style="font-weight:bold;color:#94A3B8;font-size:12px;">StubHub</span>
                                    <span style="color:#FF007A;font-weight:bold;font-size:12px;">From $62</span>
                                </div>
                                <div class="provider-tag">
                                    <span style="font-weight:bold;color:#94A3B8;font-size:12px;">SeatGeek</span>
                                    <span style="color:#00ff66;font-weight:bold;font-size:12px;">From $41</span>
                                </div>
                            </div>
                            
                            <div style="flex: 1; text-align:center;">
                                <h4 style="margin:0; color:#94A3B8; font-size:11px; letter-spacing:1px; text-transform:uppercase;">Best Market Deal</h4>
                                <p class="best-deal-price">$41</p>
                                <a href="{url_link}" target="_blank" class="deal-btn">Get Tickets</a>
                            </div>
                        </div>
                    </div>
                </body>
                </html>
                '''
                components.html(card_html, height=155)
                
        else:
            st.warning("No matches found across the scanned platforms.")
            
    except Exception as e:
        st.error(f"Interference detected: {e}")
