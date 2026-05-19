import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(page_title="Sovereign Mesh", layout="wide")
st.title("🛡️ Sovereign Mesh: Real-Time Sentinel")

placeholder = st.empty()

while True:
    try:
        if os.path.exists("traffic_logs.csv"):
            # Load logs and clear cache
            df = pd.read_csv("traffic_logs.csv")
            
            with placeholder.container():
                if not df.empty:
                    last_status = df.iloc[-1]['status']
                    
                    if last_status == "MALICIOUS":
                        st.error(f"🚨 ATTACK DETECTED: {df.iloc[-1]['timestamp']}")
                        st.toast("Blocking Malicious Payload...")
                    else:
                        st.success("✅ Network Integrity Verified")
                    
                    st.subheader("Live Traffic Feed")
                    st.dataframe(df.tail(15), use_container_width=True)
                else:
                    st.info("Waiting for traffic logs...")
        else:
            st.warning("Logs not found. Waiting for Security Brain to start...")
            
    except Exception as e:
        st.error(f"Sync Error: {e}")
    
    time.sleep(1)