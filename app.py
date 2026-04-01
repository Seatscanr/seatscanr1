import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# 1. Custom Setup with Fun Favicon
st.set_page_config(page_title="SeatScanr - Ticketmaster Live", page_icon="🎫", layout="wide")

# 2. Injecting Custom CSS for Radar Tracker, Dark Theme, & Polished UI
st.markdown("""
<style>
    /* Premium Dark Theme */
    .stApp { background-color: #0b0f19; color: #f8fafc; }
    
    /* RADAR SCANNER LOADER ANIMATION */
    .radar-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 30px 0;
    }
    .radar {
        width: 100px; height: 100px; border-radius: 50%;
        border: 2px solid #00ff66; position: relative;
        background: repeating-radial-gradient(circle, #001a00 0%, #001a00 10%, #00ff66 11%, #001a00 12%);
        overflow: hidden; box-shadow: 0 0 15px rgba(0,255,102,0.4);
    }
    .radar:before {
        content: ''; position: absolute; top: 50%; left: 50%;
        width: 100%; height: 100%;
        background: linear-gradient(45deg, rgba(0,255,102,0.4) 0%, transparent 50%);
        transform-origin: top left; animation: spin 2s linear infinite;
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }

    /* Dashboard Metric Cards */
    .metric-card {
        background-color: #1e293b; border-radius: 10px; padding: 15px; text-align: center;
        border: 1px solid #334155;
    }
    
    /* Ticket Cards */
    .ticket-card {
        background-color: #111827; border: 1px solid #1f2937; border-radius: 12px;
        padding: 20px; margin-bottom: 20px; transition: 0.3s;
    }
    .ticket-card:hover { border-color: #00ff66; box-shadow: 0 0 10px rgba(0,255,102,0.1); }

    /* Custom Ticket Buttons */
    .buy-btn {
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
        color: white !important; text-align: center; padding: 12px;
        border-radius: 8px; font-weight: bold; margin-top: 15px;
        display: block; text-decoration: none; box-shadow: 0 4px 10px rgba(0,242,254,0.3);
    }
</style>
""", unsafe_allow_html=True)

# 3. Header & Logo Placement
col_logo, col_txt = st.columns([1, 5])
with col_logo:
    try:
        st.image("logo.png", width=100)
    except:
        st.markdown("<h1 style='font-size: 60px; margin: 0;'>📡</h1>", unsafe_allow_html=True)

with col_txt:
    st.markdown("<h1 style='color:#f8fafc; margin-bottom:0;'>SEATSCANR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00ff66; font-size:16px; margin-top:0; font-family:monospace;'>[ MODE: DIRECT FAN ACCESS // ZERO SUBSCRIPTIONS ]</p>", unsafe_allow_html=True)

st.divider()

# 4. Faux "Live System" Metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="metric-card"><h3 style="color:#00ff66;margin:0;">ONLINE</h3><p style="color:#94A3B8;margin:0;font-size:12px;">System Status</p></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card"><h3 style="color:#f8fafc;margin:0;">1,400+</h3><p style="color:#94A3B8;margin:0;font-size:12px;">Active Scans</p></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card"><h3 style="color:#f8fafc;margin:0;">LIVE</h3><p style="color:#94A3B8;margin:0;font-size:12px;">Ticketmaster API</p></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="metric-card"><h3 style="color:#FF007A;margin:0;">FREE</h3><p style="color:#94A3B8;margin:0;font-size:12px;">Access Tier</p></div>', unsafe_allow_html=True)

st.write("")

# 5. Search Bar & Controls
query = st.text_input("", placeholder="Enter an artist, team, or venue to scan...", label_visibility="collapsed")

# API Key Hook
TM_API_KEY = st.secrets["TM_API_KEY"]

if query:
    # THE RADAR TRIGGER
    with st.empty():
        st.markdown('''
            <div class="radar-container">
                <div class="radar"></div>
                <p style="color:#00ff66; font-weight:bold; margin-top:15px; font-family:monospace;">PINGING SATELLITES FOR: ''' + query.upper() + '''</p>
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
            
            # Use a table-like layout for dashboard look
            for ev in events[:10]:
                name = ev['name']
                date_str = ev['dates']['start'].get('localDate', 'TBA')
                venue = ev['_embedded']['venues'][0]['name']
                city = ev['_embedded']['venues'][0]['city']['name']
                url_link = ev['url']
                
                # Turn date into a clean read
                try:
                    formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d, %Y")
                except:
                    formatted_date = date_str

                # Clean Dashboard Row Card
                st.markdown(f'''
                    <div class="ticket-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <h3 style="margin:0; color:#f8fafc;">{name}</h3>
                                <p style="margin:5px 0 0 0; color:#94A3B8;">📅 {formatted_date} &nbsp;|&nbsp; 📍 {venue} ({city})</p>
                            </div>
                            <div style="min-width:150px;">
                                <a href="{url_link}" target="_blank" class="buy-btn">Unlock Seats</a>
                            </div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
        else:
            st.warning("Radar yielded 0 results. Try a broader search term.")
            
    except Exception as e:
        st.error(f"Interference detected: {e}")
