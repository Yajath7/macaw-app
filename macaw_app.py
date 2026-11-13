import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Macaw By Stories | Operations Center",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
        padding: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ffd966;
        color: #0b0b10;
        border-color: #ffd966;
    }
    .zone-card {
        background-color: #14141c;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #222;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    c_logo, c_title = st.columns([1, 6])
    with c_logo:
        st.image("logo.png", width=95)
    with c_title:
        st.title("Macaw Ops — Security Gateway")
    st.markdown("---")
    access_key = st.text_input("Enter Staff Access Key", type="password")
    if st.button("Unlock Dashboard", key="login_btn"):
        if access_key == "macaw99": 
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid Access Key. Entry Denied.")
    st.stop()

col_logo, col_head = st.columns([1, 8])
with col_logo:
    st.image("logo.png", width=85)
with col_head:
    st.title("Macaw By Stories — Full Venue Control Room")
st.markdown("---")

if 'zones' not in st.session_state:
    st.session_state.zones = {
        'RT-01 (Rooftop)': 'Available', 'RT-02 (Rooftop)': 'Available',
        'RT-03 (Rooftop)': 'Available', 'RT-04 (Rooftop)': 'Available',
        'RT-05 (Rooftop)': 'Available', 'RT-06 (Rooftop)': 'Available',
        'RT-07 (Rooftop)': 'Available', 'RT-08 (Rooftop)': 'Available',
        'RT-09 (Rooftop)': 'Available', 'RT-10 (Rooftop)': 'Available',
        'VIP-01 (Cabana)': 'Available', 'VIP-02 (Cabana)': 'Available',
        'VIP-03 (Cabana)': 'Available', 'VIP-04 (Cabana)': 'Available',
        'JD-01 (Jungle Deck)': 'Available', 'JD-02 (Jungle Deck)': 'Available',
        'KR-01 (Karaoke Room 1)': 'Available', 'KR-02 (Karaoke Room 2)': 'Available',
        'SR-01 (Private Screening)': 'Available', 'PR-01 (Corporate Party Hall)': 'Available',
        'BAR-01 (Main Counter)': 'Available', 'BAR-02 (Sky Bar)': 'Available',
        'HT-01 (High-Top)': 'Available', 'HT-02 (High-Top)': 'Available'
    }

if 'waitlist' not in st.session_state:
    st.session_state.waitlist = pd.DataFrame(columns=['Token', 'Guest Name', 'Phone', 'Size', 'Preferred Zone', 'Status'])

if 'token_counter' not in st.session_state:
    st.session_state.token_counter = 101

tab1, tab2 = st.tabs(["⚙️ Live Floor & Zone Monitor (24 Zones)", "👑 Host Waitlist Portal"])

with tab1:
    total = len(st.session_state.zones)
    avail = sum(1 for v in st.session_state.zones.values() if v == 'Available')
    occ = sum(1 for v in st.session_state.zones.values() if v == 'Occupied')
    clean = sum(1 for v in st.session_state.zones.values() if v == 'Needs Cleaning')
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Capacity", f"{total} Zones")
    m2.metric("🟢 Available", avail)
    m3.metric("🔴 Occupied", occ)
    m4.metric("🟡 Needs Cleaning", clean)
    st.markdown("---")

    section = st.selectbox("Filter Floor Section:", [
        "All Zones (24)", 
        "Rooftop Dining (RT)", 
        "VIP Cabanas & Jungle Deck (VIP/JD)", 
        "Karaoke & Private Screening (KR/SR/PR)", 
        "Bar & High-Tops (BAR/HT)"
    ])

    filtered_zones = {}
    for k, v in st.session_state.zones.items():
        if section == "All Zones (24)":
            filtered_zones[k] = v
        elif "Rooftop" in section and k.startswith("RT"):
            filtered_zones[k] = v
        elif "VIP" in section and (k.startswith("VIP") or k.startswith("JD")):
            filtered_zones[k] = v
        elif "Karaoke" in section and (k.startswith("KR") or k.startswith("SR") or k.startswith("PR")):
            filtered_zones[k] = v
        elif "Bar" in section and (k.startswith("BAR") or k.startswith("HT")):
            filtered_zones[k] = v

    cols = st.columns(4)
    for idx, (zone, current_status) in enumerate(filtered_zones.items()):
        with cols[idx % 4]:
            st.markdown(f'<div class="zone-card"><h4>{zone}</h4></div>', unsafe_allow_html=True)
            
            if current_status == 'Available':
                st.success(f"🟢 {current_status}")
            elif current_status == 'Occupied':
                st.error(f"🔴 {current_status}")
            else:
                st.warning(f"🟡 {current_status}")
            
            if st.button("Cycle Status", key=f"btn_{zone}"):
                if current_status == 'Available':
                    st.session_state.zones[zone] = 'Occupied'
                elif current_status == 'Occupied':
                    st.session_state.zones[zone] = 'Needs Cleaning'
                else:
                    st.session_state.zones[zone] = 'Available'
                st.rerun()

with tab2:
    st.subheader("Entrance Gate Queue")
    
    with st.form("waitlist_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Guest Name")
        phone = c2.text_input("Mobile Number")
        c3, c4 = st.columns(2)
        size = c3.number_input("Group Size", min_value=1, max_value=30, value=2)
        pref = c4.selectbox("Preferred Zone", ["Any", "Rooftop Dining", "VIP Cabana", "Karaoke / Screening", "Bar Counter"])
        submit = st.form_submit_button("Add to Queue")
        
        if submit and name and phone:
            new_guest = pd.DataFrame([{
                'Token': f"MC-{st.session_state.token_counter}",
                'Guest Name': name,
                'Phone': phone,
                'Size': int(size),
                'Preferred Zone': pref,
                'Status': 'Waiting'
            }])
            st.session_state.waitlist = pd.concat([st.session_state.waitlist, new_guest], ignore_index=True)
            st.session_state.token_counter += 1
            st.success(f"Added {name} to the system!")
            st.rerun()
            
    st.markdown("### Active Waitlist Queue")
    if not st.session_state.waitlist.empty:
        st.dataframe(st.session_state.waitlist, use_container_width=True)
        
        if st.button("Seat Next Guest in Line", key="seat_guest_btn"):
            st.session_state.waitlist = st.session_state.waitlist.iloc[1:].reset_index(drop=True)
            st.success("Queue updated successfully.")
            st.rerun()
    else:
        st.info("The entrance gate is currently clear.")

st.markdown("---")
if st.button("🔒 Lock Dashboard Management", key="lock_system_btn"):
    st.session_state.authenticated = False
    st.rerun()
