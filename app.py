# app.py (Standalone Version for Streamlit Cloud)
import streamlit as st
import os
from music_streaming_system import MusicStreamingSystem
from strategy.recommendation.two_stage_ranker_strategy import TwoStageRankerStrategy
from entities.user import User
from enums.subscription_tier import SubscriptionTier

st.set_page_config(page_title="AI Music Rec Engine", layout="wide")
st.title("🎧 Production AI Music Recommendation Engine")
st.caption("Live Spotify Ingestion • Two-Stage Vector & LightGBM Personalization")

# Initialize System & Strategy as singletons using session state
@st.cache_resource
def get_system_and_strategy():
    system = MusicStreamingSystem.get_instance()
    strategy = TwoStageRankerStrategy()
    try:
        system.ingest_from_spotify(query="top hits", limit=10)
    except Exception as e:
        st.warning(f"Initial ingestion notice: {e}")
    
    catalog = list(system._songs.values())
    if catalog:
        strategy.build_index(catalog)
        system._recommendation_service.set_strategy(strategy)
    return system, strategy

system, two_stage_strategy = get_system_and_strategy()

# Sidebar: Ingest Live Data
st.sidebar.header("Data Pipeline")
query = st.sidebar.text_input("Spotify Search Query", value="Synthwave 2024")
limit = st.sidebar.slider("Number of Tracks", 3, 10, 10)

if st.sidebar.button("Ingest Live Data"):
    with st.spinner("Ingesting from Spotify API..."):
        try:
            count = system.ingest_from_spotify(query=query, limit=limit)
            catalog = list(system._songs.values())
            two_stage_strategy.build_index(catalog)
            st.sidebar.success(f"Ingested {count} tracks! Total Catalog: {len(catalog)}")
        except Exception as e:
            st.sidebar.error(f"Ingestion failed. Check your Streamlit Secrets for Spotify keys. Error: {e}")

# Main Panel: Catalog & Recommendation
col1, col2 = st.columns([1, 1])

catalog = list(system._songs.values())

with col1:
    st.subheader("🎵 Catalog Seed Selector")
    if not catalog:
        st.warning("Catalog is empty. Please run live ingestion from the sidebar.")
    else:
        song_titles = {f"{s.title} — {s.artist.get_name()}": s.id for s in catalog}
        selected_song_name = st.selectbox("Select a seed track to recommend from:", list(song_titles.keys()))
        selected_id = song_titles[selected_song_name]

        user_tier = st.radio("Simulated User Subscription:", ["PREMIUM", "FREE"], horizontal=True)
        top_k = st.slider("Recommendations Count (Top-K):", 3, 10, 5)

with col2:
    st.subheader("⚡ Model Predictions (LightGBM Ranker)")
    if catalog and st.button("Generate Recommendations", type="primary"):
        seed_song = system._songs[selected_id]
        tier = SubscriptionTier.PREMIUM if user_tier == "PREMIUM" else SubscriptionTier.FREE
        user = User("test_user_01", tier, 0)

        ranked_songs = two_stage_strategy.recommend_for_user(user, seed_song, catalog, top_k=top_k)
        
        st.success("Inference complete via Two-Stage GBDT Engine!")
        
        for idx, r in enumerate(ranked_songs, start=1):
            st.markdown(f"**{idx}. {r.title}** — *{r.artist.get_name()}* (`{r.duration_in_seconds}s`)")
            
            link_col, audio_col = st.columns([1, 1])
            with link_col:
                if r.spotify_url:
                    st.markdown(f"[🎵 Open on Spotify]({r.spotify_url})", unsafe_allow_html=True)
            with audio_col:
                if r.preview_url:
                    st.audio(r.preview_url)
            st.divider()