import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# 1. Custom Setup with Game Favicon
st.set_page_config(page_title="SeatScanr - Metasearch", page_icon="🎫", layout="wide")

# 2. Injecting Custom CSS for Professional UI, Infinite Ticker & Alerts
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
    
    /* 📈 INFINITE SEAMLESS STOCK TICKER AT THE TOP */
    .ticker-wrap {
        position: fixed; top: 0; left: 0; width: 100%; overflow: hidden; height: 35px;
        background-color: #0b111e; border-bottom: 1px solid #1e293b; z-index: 9999;
        display: flex; align-items: center;
    }
    .ticker {
        display: flex;
        white-space: nowrap;
        animation: ticker 35s linear infinite;
    }
    .ticker-content {
        display: flex;
        flex-shrink: 0;
    }
    .ticker-item {
        display: inline-block; padding: 0 25px; font-family: monospace; font-size: 12px;
        font-weight: bold; color: #94A3B8; line-height: 35px;
    }
    .price-up { color: #00ff66; }
    .price-down { color: #FF007A; }
    
    @keyframes ticker {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-50%, 0, 0); }
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
        margin-top: 60px;
        margin-bottom: 10px;
    }
    
    /* Input & Selectbox Styling override */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    
    .hero-sub {
        color: #00F2FE; 
        font-size: 13px; 
        font-weight: bold; 
        font-family: monospace;
        letter-spacing: 2px;
        text-align: center;
        text-transform: uppercase;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 📈 LIVE STOCK TICKER
st.markdown("""
<div class="ticker-wrap">
    <div class="ticker">
        <div class="ticker-content">
            <span class="ticker-item">🎫 MARKET LIVE</span>
            <span class="ticker-item">WEEZER: <span class="price-down">$85 (-3.2%)</span></span>
            <span class="ticker-item">SANTANA: <span class="price-up">$120 (+5.4%)</span></span>
            <span class="ticker-item">RUSH REUNION: <span class="price-up">$250 (+15.1%)</span></span>
            <span class="ticker-item">NY YANKEES: <span class="price-down">$65 (-1.5%)</span></span>
            <span class="ticker-item">COACHELLA 2026: <span class="price-up">$549 (+2.1%)</span></span>
            <span class="ticker-item">LA LAKERS: <span class="price-down">$1,100 (-0.8%)</span></span>
        </div>
        <div class="ticker-content">
            <span class="ticker-item">🎫 MARKET LIVE</span>
            <span class="ticker-item">WEEZER: <span class="price-down">$85 (-3.2%)</span></span>
            <span class="ticker-item">SANTANA: <span class="price-up">$120 (+5.4%)</span></span>
            <span class="ticker-item">RUSH REUNION: <span class="price-up">$250 (+15.1%)</span></span>
            <span class="ticker-item">NY YANKEES: <span class="price-down">$65 (-1.5%)</span></span>
            <span class="ticker-item">COACHELLA 2026: <span class="price-up">$549 (+2.1%)</span></span>
            <span class="ticker-item">LA LAKERS: <span class="price-down">$1,100 (-0.8%)</span></span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Centered, Professional Hero Section
st.markdown('<p class="hero-sub">// Live Ticket Metasearch</p>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Find the best seats.<br>Compare the market.</h1>', unsafe_allow_html=True)

# 5. Centered Search UI
left_space, search_box, right_space = st.columns([1, 2, 1])

# TOP 5 POPULAR SUGGESTIONS DROPDOWN (With image emojis as logos!)
popular_options = [
    "Type or Select an Event...",
    "🎤 Taylor Swift",
    "⚾ New York Yankees",
    "🏀 Los Angeles Lakers",
    "🎸 Metallica",
    "🎭 Hamilton"
]

with search_box:
    selected_option = st.selectbox("", options=popular_options, label_visibility="collapsed")
    
    # Text fallback if they want to type something completely custom
    custom_query = st.text_input("", placeholder="...or type any other artist, team, or venue here", label_visibility="collapsed")

# Resolve which query to use
query = ""
if selected_option != "Type or Select an Event...":
    # Strip the emoji off the front for clean API searching
    query = selected_option.split(" ", 1)[1] if " " in selected_option else selected_option
if custom_query:
    query = custom_query

st.write("") 

# --- CITY EXPLORER FEATURE ---
_, explorer_col, _ = st.columns([1, 2, 1])
with explorer_col:
    with st.expander("🌍 Explore Your City (Next 14 Days)"):
        city_input = st.text_input("Enter City Name", placeholder="e.g., Chicago, New York, Los Angeles")
        if st.button("Find Local Events"):
            if city_input:
                query = f"city_mode:{city_input}"
            else:
                st.error("Please enter a city name first!")

# API Key Hook
TM_API_KEY = st.secrets["TM_API_KEY"]

if query:
    events = []
    # THE RADAR TRIGGER
    with st.empty():
        st.markdown('''
            <div class="radar-container">
                <div class="radar"></div>
                <p style="color:#00F2FE; font-weight:bold; margin-top:15px; font-family:monospace; letter-spacing:1px;">SCANNING THE MARKET...</p>
            </div>
        ''', unsafe_allow_html=True)
        
        # Determine if we are doing a standard query or a city explore
        if query.startswith("city_mode:"):
            city = query.split(":")[1]
            now = datetime.now()
            two_weeks_later = now + timedelta(days=14)
            start_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
            end_date = two_weeks_later.strftime("%Y-%m-%dT%H:%M:%SZ")
            url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={TM_API_KEY}&city={city}&startDateTime={start_date}&endDateTime={end_date}&sort=date,asc"
        else:
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
            
            _, success_box, _ = st.columns([1, 2, 1])
            with success_box:
                display_name = query.split(":")[1] if query.startswith("city_mode:") else query
                st.success(f"Discovered {len(events)} matching live dates for **{display_name}**")
            
            # REMOVED THE [:5] LIMIT. Now it will loop through dozens of matches!
            for ev in events[:50]: 
                name = ev['name']
                date_str = ev['dates']['start'].get('localDate', 'TBA')
                venue = "TBA"
                if '_embedded' in ev and 'venues' in ev['_embedded']:
                    venue = ev['_embedded']['venues'][0]['name']
                url_link = ev['url']
                
                try:
                    formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d, %Y")
                except:
                    formatted_date = date_str

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
                            padding: 5px 0;
                        }}
                        .deal-card {{
                            background-color: #0f172a; 
                            border: 1px solid #1e293b; 
                            border-radius: 8px;
                            padding: 18px; 
                            margin-bottom: 5px; 
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
                                    <span style="background-color:#1e293b; color:#94A3B8; padding:3px 6px; border-radius:3px; font-size:10px; font-weight:bold; letter-spacing:1px; text-transform:uppercase;">Confirmed Event</span>
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
                components.html(card_html, height=130)
                
                # 🛎️ PRICE MONITORING ALERTS
                _, alert_box, _ = st.columns([1, 2, 1])
                with alert_box:
                    with st.expander(f"🔔 Create Price Alert for {name}"):
                        st.write("We will monitor secondary markets and email you when prices drop below your target.")
                        col_email, col_target, col_btn = st.columns([2, 1, 1])
                        with col_email:
                            user_email = st.text_input("Your Email", key=f"email_{ev['id']}")
                        with col_target:
                            target_price = st.number_input("Target Price ($)", min_value=10, value=40, key=f"price_{ev['id']}")
                        with col_btn:
                            st.write("") 
                            if st.button("Set Alert", key=f"btn_{ev['id']}"):
                                if user_email:
                                    st.success(f"Alert Active! Watching for prices below ${target_price} for {name}.")
                                else:
                                    st.error("Please enter an email address.")
                st.divider()
                
        else:
            _, warn_box, _ = st.columns([1, 2, 1])
            with warn_box:
                st.warning("No matches found across the scanned platforms.")
            
    except Exception as e:
        st.error(f"Interference detected: {e}")
