import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
import streamlit.components.v1 as components

# 1. Custom Setup with Game Favicon
st.set_page_config(page_title="SeatScanr - Metasearch", page_icon="🎫", layout="wide")

# 2. Injecting Custom CSS for Professional UI & Infinite Ticker
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
    
    /* Input Styling override to feel like a high-end search bar */
    div[data-baseweb="input"] {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 50px !important;
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
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 📈 INFINITE STOCK TICKER
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

# 5. Centered search bar (Clean & Alone)
left_space, search_box, right_space = st.columns([1, 2, 1])

with search_box:
    query = st.text_input("", placeholder="Search for artists, teams, sports or venues...", label_visibility="collapsed")

st.write("") 

# API Key Hook
TM_API_KEY = st.secrets["TM_API_KEY"]

# Function to handle the alert pop-up (Streamlit Modal)
@st.dialog("🔔 Create Price Alert")
def set_alert_modal(event_name):
    st.write(f"We will monitor secondary markets and email you when prices drop for **{event_name}**.")
    user_email = st.text_input("Your Email address", placeholder="alex@example.com")
    target_price = st.number_input("Target Price ($)", min_value=10, value=40)
    
    if st.button("Confirm Alert", use_container_width=True):
        if user_email:
            st.success(f"Alert Active! We are watching for prices below ${target_price}.")
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("Please enter a valid email.")

if query:
    # THE RADAR TRIGGER
    with st.empty():
        st.markdown('''
            <div class="radar-container">
                <div class="radar"></div>
                <p style="color:#00F2FE; font-weight:bold; margin-top:15px; font-family:monospace; letter-spacing
