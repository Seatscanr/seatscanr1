import streamlit as st
import requests
import pandas as pd
import time

# 1. Custom Setup with Fun Favicon
st.set_page_config(page_title="SeatScanr - Ticketmaster Live", page_icon="🎫", layout="wide")

# 2. Injecting Custom CSS for Radar Tracker, Dark Theme, & Polished UI
st.markdown("""
<style>
    /* Dark Slate Background for UI Polish */
    .stApp { background-color: #0f172a; color: #f8fafc; }
    
    /* RADAR SCANNER LOADER ANIMATION */
    .radar-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 30px 0;
    }
    .radar {
        width: 120px; height: 120px; border-radius: 50%;
        border: 2px solid #00ff66; position: relative;
        background: repeating-radial-gradient(circle, #001a00 0%, #001a00 10%, #00ff66 11%, #001a00 12%);
        overflow: hidden; box-shadow: 0 0 15px #00ff66;
    }
    .radar:before {
        content: ''; position: absolute; top: 50%; left: 50%;
        width: 100%; height: 100%;
        background: linear-gradient(45deg, rgba(0,255,102,0.4) 0%, transparent 50%);
        transform-origin: top left; animation: spin 2s linear infinite;
    }
    .radar-ping {
        position: absolute; width: 8px; height: 8px; background-color: #00ff66;
        border-radius: 50%; top: 30%; left: 70%; box-shadow: 0 0 10px #00ff66;
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }

    /* Custom Ticket Buttons */
    .buy-btn {
        background: linear-gradient(135deg, #FF007A 0%, #7B00FF 100%);
        color: white !important; text-align: center; padding: 12px;
        border-radius: 10px; font-weight: bold; margin-top: 15px;
        display: block; text-decoration: none; box-shadow: 0 4px 10px rgba(255,0,122,0.3);
    }
    .buy-btn:hover { transform: scale(1.03); transition: 0.2s; }
</style>
""", unsafe_allow_html=True)

# 3. Header & Logo Placement
col_logo, col_txt = st.columns([1, 4])
with col_logo:
    try:
        # Tries to pull the logo you uploaded to GitHub!
        st.image("logo.png", width=120)
    except:
        # Fallback emoji if the logo is not uploaded yet or fails to load
        st.markdown("<h1 style='font-size: 80px; margin: 0;'>🎫</h1>", unsafe_allow_html=True)

with col_txt:
    st.markdown("<h1 style='color:#FF007A; margin-bottom:0;'>SeatScanr</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8; font-size:18px; margin-top:0;'>Hunting down the best live events across the globe.</p>", unsafe_allow_html=True)

st.divider()

# 4. Search Bar
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    query = st.text_input("", placeholder="Enter an artist, team, or city...", label_visibility="collapsed")

# 5. API Key Hook
TM_API_KEY = st.secrets["TM_API_KEY"]

if query:
    # 💥 THE RADAR TRIGGER: Appears while waiting for Ticketmaster
    with st.empty():
        st.markdown('''
            <div class="radar-container">
                <div class="radar"><div class="radar-ping"></div></div>
                <p style="color:#00ff66; font-weight:bold; margin-top:15px; font-family:monospace;">SCANNING TICKETMASTER FREQUENCIES...</p>
            </div>
        ''', unsafe_allow_html=True)
        
        # Pull Data from Ticketmaster
        url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={TM_API_KEY}&keyword={query}"
        try:
            response = requests.get(url)
            data = response.json()
            time.sleep(1.5) # Keeps the radar visible for a beat so it feels functional!
            
            # Clear the radar when results land
            st.write("") 
            
        except:
            st.write("")

    # 6. Render the Results
    try:
        if '_embedded' in data and 'events' in data['_embedded']:
            events = data['_embedded']['events']
            st.success(f"Radar contact confirmed. Showing results for: **{query}**")
            
            grid = st.columns(3)
            for i, ev in enumerate(events[:9]):
                with grid[i % 3]:
                    with st.container(border=True):
                        if 'images' in ev:
                            st.image(ev['images'][0]['url'], use_container_width=True)
                        
                        st.subheader(ev['name'])
                        date = ev['dates']['start'].get('localDate', 'TBA')
                        venue = ev['_embedded']['venues'][0]['name']
                        
                        st.markdown(f"📅 **Date:** `{date}`")
                        st.markdown(f"📍 **Venue:** {venue}")
                        
                        # Glowing gradient button!
                        st.markdown(f'<a href="{ev["url"]}" target="_blank" class="buy-btn">Grab Tickets</a>', unsafe_allow_html=True)
        else:
            st.warning("Target not found. Try scanning another frequency.")
            
    except Exception as e:
        st.error(f"Interference detected: {e}")
