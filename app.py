import streamlit as st
import requests
import pandas as pd

# Set up Page configuration
st.set_page_config(page_title="SeatScanr - Ticketmaster Live", layout="wide")

st.title("🎟️ SeatScanr - Live Event Search")
st.write("Search for your favorite sports teams or artists directly via Ticketmaster.")

# 🔒 Ticketmaster API Key (Reading securely from Streamlit Advanced Settings)
TM_API_KEY = st.secrets["TM_API_KEY"]

# Search Input
query = st.text_input("Search for an event (e.g., Hornets, Eagles, Adele):", "")

if query:
    st.write(f"Searching for: **{query}**...")
    
    # Ticketmaster Discovery API URL
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={TM_API_KEY}&keyword={query}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Check if events were found
        if '_embedded' in data and 'events' in data['_embedded']:
            events = data['_embedded']['events']
            
            # Prepare data for display
            event_list = []
            for ev in events:
                name = ev.get('name', 'N/A')
                date = ev.get('dates', {}).get('start', {}).get('localDate', 'N/A')
                venue = ev.get('_embedded', {}).get('venues', [{}])[0].get('name', 'N/A')
                city = ev.get('_embedded', {}).get('venues', [{}])[0].get('city', {}).get('name', 'N/A')
                link = ev.get('url', '#')
                
                event_list.append({
                    "Event Name": name,
                    "Date": date,
                    "Venue": f"{venue} ({city})",
                    "Ticket Link": link
                })
            
            df = pd.DataFrame(event_list)
            
            # Display interactive table
            st.dataframe(df, use_container_width=True)
            
            # Display pretty visual grids
            st.divider()
            cols = st.columns(3)
            for i, ev in enumerate(events[:6]):  # Show top 6 events visually
                with cols[i % 3]:
                    st.subheader(ev['name'])
                    if 'images' in ev:
                        st.image(ev['images'][0]['url'], use_container_width=True)
                    st.write(f"📅 **Date:** {ev['dates']['start'].get('localDate', 'N/A')}")
                    st.write(f"📍 **Venue:** {ev['_embedded']['venues'][0]['name']}")
                    st.markdown(f"[🎟️ Buy Tickets]({ev['url']})")
                    st.divider()
                    
        else:
            st.warning("No events found. Try searching for something else!")
            
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
      
