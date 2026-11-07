import time
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

# 1. INITIAL SYSTEM SETUP
st.set_page_config(
    page_title="Macaw By Stories | Operations Center",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. SEAMLESS DARK MODE ARCHITECTURE
st.markdown("""
    <style>
    .stApp { background-color: #0b0b10; color: #f5f5f7; }
    h1, h2, h3, h4, p, label { color: #f5f5f7 !important; }
    .stButton>button {
        width: 100%;
        background-color: #1c1c24;
        color: #f5f5f7;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 10px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ffd966;
        color: #0b0b10;
        border-color: #ffd966;
    }
    .zone-card {
        background-color: #14141c;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #222;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🦜 Macaw By Stories — Control Room")
st.markdown("---")

# 3. GLOBAL ENGINE MEMORY (SESSION STATE)
if 'zones' not in st.session_state:
    st.session_state.zones = {
        'T1 (Rooftop Table)': 'Available',
        'T2 (Rooftop Table)': 'Available',
        'T3 (Rooftop Table)': 'Available',
        'K1 (Karaoke Lounge)': 'Available',
        'S1 (Screening Room)': 'Available',
        'B1 (Main Bar)': 'Available'
    }

if 'waitlist' not in st.session_state:
    st.session_state.waitlist = pd.DataFrame(columns=['Token', 'Guest Name', 'Phone', 'Size', 'Status'])

if 'token_counter' not in st.session_state:
    st.session_state.token_counter = 101

# 4. MULTI-PANEL VIEW INTERFACE
tab1, tab2 = st.tabs(["⚙️ Zone & Table Monitor", "👑 Host Waitlist Portal"])

with tab1:
    st.subheader("Live Floor Layout Status")
    cols = st.columns(3)
    
    for idx, (zone, current_status) in enumerate(st.session_state.zones.items()):
        with cols[idx % 3]:
            st.markdown(f'<div class="zone-card"><h3>{zone}</h3></div>', unsafe_allow_html=True)
            
            # Dynamic Visual Tags
            if current_status == 'Available':
                st.success(f"Status: {current_status}")
            elif current_status == 'Occupied':
                st.error(f"Status: {current_status}")
            else:
                st.warning(f"Status: {current_status}")
            
            # Simple One-Click Rotation Mechanism
            if st.button(f"Cycle {zone}"):
                if current_status == 'Available':
                    st.session_state.zones[zone] = 'Occupied'
                elif current_status == 'Occupied':
                    st.session_state.zones[zone] = 'Needs Cleaning'
                else:
                    st.session_state.zones[zone] = 'Available'
                st.rerun()

with tab2:
    st.subheader("Entrance Gate Queue")
    
    # Customer Entry Interface
    with st.form("waitlist_form", clear_on_submit=True):
        name = st.text_input("Guest Name")
        phone = st.text_input("Mobile Number")
        size = st.number_input("Group Size", min_value=1, max_value=20, value=2)
        submit = st.form_submit_button("Add to Queue")
        
        if submit and name and phone:
            new_guest = pd.DataFrame([{
                'Token': f"MC-{st.session_state.token_counter}",
                'Guest Name': name,
                'Phone': phone,
                'Size': int(size),
                'Status': 'Waiting'
            }])
            st.session_state.waitlist = pd.concat([st.session_state.waitlist, new_guest], ignore_index=True)
            st.session_state.token_counter += 1
            st.success(f"Added {name} to the system!")
            st.rerun()
            
    st.markdown("### Active Waitlist Queue")
    if not st.session_state.waitlist.empty:
        st.dataframe(st.session_state.waitlist, use_container_width=True)
        
        # Clear Operations Action
        if st.button("Seat Next Guest in Line"):
            if not st.session_state.waitlist.empty:
                st.session_state.waitlist = st.session_state.waitlist.iloc[1:].reset_index(drop=True)
                st.success("Queue updated successfully.")
                st.rerun()
    else:
        st.info("The entrance gate is currently clear.")
