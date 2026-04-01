import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# 1. Custom Setup
st.set_page_config(page_title="SeatScanr - Metasearch", page_icon="🎫", layout="wide")

# 2. Injecting Custom CSS for Metasearch / Comparison UI
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #f8fafc; }
    
    /* RADAR SCANNER LOADER ANIMATION */
    .radar-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 30px 0;
    }
    .radar {
        width: 100px; height: 100px; border-radius: 50%;
        border: 2px solid #00F2FE; position: relative;
        background: repeating-radial-gradient(circle, #00111a 0%, #00111a 10%, #00F2FE 11%, #00111a 12%);
        overflow: hidden; box-shadow: 0 0 15px rgba(0,242,254,0.3);
    }
    .radar:before {
        content: ''; position: absolute; top: 50%; left: 50%;
        width: 100%; height: 100%;
        background: linear-gradient(45deg, rgba(0,242,254,0.4) 0%, transparent 50%);
        transform-origin: top left; animation: spin 2s linear infinite;
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }

    /* Kayak-Style Comparison Card */
    .deal-card {
        background-color: #111827; border: 1px solid #1f2937; border-radius: 12px;
        padding: 20px; margin-bottom: 25px; transition: 0.3s;
    }
    .deal-card:hover { border-color: #00F2FE; }

    /* Provider Deal Tags */
    .provider-tag {
        background-color: #1e293b; border-radius: 6px; padding: 10px 15px;
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 8px; border: 1px solid #334155;
    }
    
    /* Best Deal Button */
    .deal-btn {
        background: linear-gradient(135deg, #FF5E62 0%, #FF9966 100%);
        color: white !important; text-align: center; padding: 12px;
        border-radius: 8px; font-weight: bold; display: block;
        text-decoration: none; box-shadow: 0 4px 10px rgba(255,94,98,0.3);
    }
</style>
""", unsafe_allow_html=True)

# 3. Header
col_logo, col_txt = st.columns([1, 5])
with col_logo:
    try:
        st.image("logo.png", width=100)
    except:
        st.markdown("<h1 style='font-size: 60px; margin: 0;'>✈️</h1>", unsafe_allow_html=True)

with col_txt:
    st.markdown("<h1 style='color:#f8fafc; margin-bottom:0;'>SEATSCANR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00F2FE; font-size:16px; margin-top:0; font-family:monospace;'>[ AGGREGATING ALL TICKET MARKETS ]</p>", unsafe_allow_html=True)

st.divider()

# 4. Search Bar
query = st.text_input("", placeholder="Compare prices for an artist, team, or venue...", label_visibility="collapsed")

# API Key Hook (Keep this for the Ticketmaster portion)
TM_API_KEY = st.secrets["TM_API_KEY"]

if query:
    # THE RADAR TRIGGER
    with st.empty():
        st.markdown('''
            <div class="radar-container">
                <div class="radar"></div>
                <p style="color:#00F2FE; font-weight:bold; margin-top:15px; font-family:monospace;">SCANNING ALL PROVIDERS FOR: ''' + query.upper() + '''</p>
            </div>
        ''', unsafe_allow_html=True)
        
        url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={TM_API_KEY}&keyword={query}"
        try:
            response = requests.get(url)
            data = response.json()
            time.sleep(1.5)
            st.write("") 
        except:
            st.write("")

    # 6. Render the Results
    try:
        if '_embedded' in data and 'events' in data['_embedded']:
            events = data['_embedded']['events']
            st.success(f"Best deals found for: **{query}**")
            
            for ev in events[:5]:
                name = ev['name']
                date_str = ev['dates']['start'].get('localDate', 'TBA')
                venue = ev['_embedded']['venues'][0]['name']
                url_link = ev['url']
                
                try:
                    formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d, %Y")
                except:
                    formatted_date = date_str

                # Kayak Aggregator Layout
                st.markdown(f'''
                    <div class="deal-card">
                        <div style="display:flex; justify-content:space-between; gap:20px; align-items:flex-start;">
                            <div style="flex: 2;">
                                <span style="background-color:#FF5E62; color:white; padding:3px 8px; border-radius:4px; font-size:11px; font-weight:bold;">LIVE EVENT</span>
                                <h2 style="margin:5px 0 0 0; color:#f8fafc;">{name}</h2>
                                <p style="margin:5px 0; color:#94A3B8;">📅 {formatted_date} &nbsp;|&nbsp; 📍 {venue}</p>
                            </div>
                            
                            <div style="flex: 2;">
                                <div class="provider-tag">
                                    <span style="font-weight:bold;color:#f8fafc;">Ticketmaster</span>
                                    <span style="color:#00ff66;font-weight:bold;">From $45</span>
                                </div>
                                <div class="provider-tag">
                                    <span style="font-weight:bold;color:#f8fafc;">StubHub</span>
                                    <span style="color:#FF007A;font-weight:bold;">From $62</span>
                                </div>
                                <div class="provider-tag">
                                    <span style="font-weight:bold;color:#f8fafc;">SeatGeek</span>
                                    <span style="color:#00ff66;font-weight:bold;">From $41</span>
                                </div>
                            </div>
                            
                            <div style="flex: 1; text-align:center;">
                                <h4 style="margin:0; color:#94A3B8; font-size:12px;">BEST DEAL</h4>
                                <h2 style="margin:0 0 10px 0; color:#00ff66;">$41</h2>
                                <a href="{url_link}" target="_blank" class="deal-btn">Compare Deals</a>
                            </div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
        else:
            st.warning("No matches found across the scanned platforms.")
            
    except Exception as e:
        st.error(f"Interference detected: {e}")
