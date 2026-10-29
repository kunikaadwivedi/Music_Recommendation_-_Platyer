# app.py
import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Music Rec Engine", layout="wide")
st.title("🎧 Production AI Music Recommendation Engine")
st.caption("Live Spotify Ingestion • Two-Stage Vector & LightGBM Personalization")

# Sidebar: Ingest Live Data
st.sidebar.header("Data Pipeline")
query = st.sidebar.text_input("Spotify Search Query", value="Synthwave 2024")
limit = st.sidebar.slider("Number of Tracks", 3, 10, 10)

if st.sidebar.button("Ingest Live Data"):
    with st.spinner("Ingesting from Spotify API..."):
        res = requests.post(f"{API_URL}/v1/ingest", json={"query": query, "limit": limit})
        if res.status_code == 200:
            st.sidebar.success(f"Ingested! Total Catalog: {res.json()['total_catalog']}")
        else:
            st.sidebar.error(f"Ingestion failed: {res.text}")

# Main Panel: Catalog & Recommendation
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎵 Catalog Seed Selector")
    try:
        catalog_res = requests.get(f"{API_URL}/v1/catalog")
        catalog = catalog_res.json() if catalog_res.status_code == 200 else []
    except Exception:
        catalog = []

    if not catalog:
        st.warning("Catalog is empty. Please run live ingestion from the sidebar.")
    else:
        song_titles = {f"{s['title']} — {s['artist']}": s["id"] for s in catalog}
        selected_song_name = st.selectbox("Select a seed track to recommend from:", list(song_titles.keys()))
        selected_id = song_titles[selected_song_name]

        user_tier = st.radio("Simulated User Subscription:", ["PREMIUM", "FREE"], horizontal=True)
        top_k = st.slider("Recommendations Count (Top-K):", 3, 10, 5)

with col2:
    st.subheader("⚡ Model Predictions (LightGBM Ranker)")
    if catalog and st.button("Generate Recommendations", type="primary"):
        payload = {
            "user_id": "test_user_01",
            "seed_song_id": selected_id,
            "subscription_tier": user_tier,
            "top_k": top_k
        }
        res = requests.post(f"{API_URL}/v1/recommend", json=payload)
        
        if res.status_code == 200:
            latency = res.headers.get("X-Inference-Time-MS", "N/A")
            st.success(f"Inference complete in **{latency} ms**")
            
            recs = res.json()
            for idx, r in enumerate(recs, start=1):
                st.markdown(f"**{idx}. {r['title']}** — *{r['artist']}* (`{r['duration_seconds']}s`)")
                
                # Redirection & audio preview options
                link_col, audio_col = st.columns([1, 1])
                with link_col:
                    if r.get('spotify_url'):
                        st.markdown(f"[🎵 Open on Spotify]({r['spotify_url']})", unsafe_allow_html=True)
                with audio_col:
                    if r.get('preview_url'):
                        st.audio(r['preview_url'])
                st.divider()
        else:
            st.error(f"Error: {res.text}")