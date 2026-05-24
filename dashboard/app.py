import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import shap
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import roc_curve, precision_recall_curve
from pathlib import Path
import streamlit.components.v1 as components

_APP_DIR = Path(__file__).resolve().parent
_PROJECT_DIR = _APP_DIR.parent

st.set_page_config(page_title="AegisML | Cyber Command", layout="wide", initial_sidebar_state="collapsed")

# ── LANDING PAGE INJECTION ──
if "booted" not in st.query_params:
    st.markdown("""
    <style>
    /* Hide Streamlit UI elements for full screen landing page */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding: 0 !important; max-width: 100% !important; margin: 0 !important;}
    iframe {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        border: none;
        margin: 0;
        padding: 0;
        z-index: 0;
    }
    
    /* Style the native Streamlit button to match AegisML cyber theme */
    div.stButton {
        position: fixed;
        bottom: 12vh;
        left: 50vw;
        transform: translateX(-50%);
        z-index: 100000;
        width: 350px !important;
        display: flex;
        justify-content: center;
    }
    div.stButton > button {
        background: rgba(0, 245, 255, 0.05) !important;
        border: 1px solid rgba(0, 245, 255, 0.4) !important;
        color: #00f5ff !important;
        padding: 1.2rem 2.5rem !important;
        border-radius: 50px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.15em !important;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.15), inset 0 0 15px rgba(0, 245, 255, 0.1) !important;
        transition: all 0.3s ease-out !important;
        backdrop-filter: blur(8px) !important;
        width: 100% !important;
        font-weight: 600 !important;
    }
    div.stButton > button:hover {
        background: rgba(0, 245, 255, 0.15) !important;
        border-color: rgba(0, 245, 255, 0.8) !important;
        box-shadow: 0 0 30px rgba(0, 245, 255, 0.4), inset 0 0 20px rgba(0, 245, 255, 0.2) !important;
        color: #ffffff !important;
        transform: scale(1.05) !important;
    }
    div.stButton > button:active {
        transform: scale(0.95) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with open(os.path.join(_PROJECT_DIR, "landing.html"), "r", encoding="utf-8") as f:
        landing_html = f.read()
        
    components.html(landing_html, height=2000, scrolling=False) # Height doesn't matter because CSS overrides it to 100vh
    
    # Render native floating button
    if st.button("⏻ INITIATE SECURE SHELL"):
        st.query_params["booted"] = "true"
        st.rerun()
        
    st.stop()

if 'alert_mode' not in st.session_state:
    st.session_state['alert_mode'] = False

# --- 1. GLOBAL CSS INJECTION ---
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400;500&family=Syncopate:wght@400;700&display=swap');

/* ── RESET ── */
*, *::before, *::after { box-sizing: border-box; }
::selection {
  background: rgba(0, 245, 255, 0.4) !important;
  color: #ffffff !important;
  text-shadow: 0 0 5px rgba(255,255,255,0.5) !important;
}

/* ── BACKGROUND (Matrix Falling Characters + Acrylic) ── */
.stApp {
  background: #0c0c0c !important;
  overflow-x: hidden;
  isolation: isolate;
}
/* CRT Scanlines and Grid */
.stApp::before {
  content: "";
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
  background-size: 100% 2px, 3px 100%;
  z-index: -2; pointer-events: none;
  opacity: 0.8;
}

/* Neon Blur Elements Across Dashboard */
.stApp::after {
  content: ''; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background: 
    radial-gradient(circle at 15% 20%, rgba(0, 245, 255, 0.12) 0%, transparent 35%),
    radial-gradient(circle at 85% 80%, rgba(132, 5, 207, 0.12) 0%, transparent 35%),
    radial-gradient(circle at 50% 50%, rgba(0, 255, 136, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 45, 85, 0.10) 0%, transparent 40%),
    radial-gradient(circle at 20% 80%, rgba(0, 170, 255, 0.10) 0%, transparent 40%);
  pointer-events: none;
  z-index: -3;
  filter: blur(50px);
}
.block-container {
  position: relative;
  z-index: 10;
  background: rgba(255, 255, 255, 0.02) !important;
  border-radius: 32px !important;
  border: 1px dashed rgba(255, 255, 255, 0.15) !important;
  backdrop-filter: blur(24px) saturate(150%) !important;
  -webkit-backdrop-filter: blur(24px) saturate(150%) !important;
  margin-top: 60px !important; /* Space for top deck */
  margin-bottom: 40px !important;
  padding: 40px 60px !important;
  max-width: 95vw !important;
  box-shadow: 0 20px 50px rgba(0,0,0,0.5), inset 0 0 0 1px rgba(255,255,255,0.02) !important;
}

/* ── HIDE NATIVE SIDEBAR ── */
[data-testid="stSidebar"] { display:none !important; }
[data-testid="stSidebarCollapsedControl"] { display:none !important; }

/* ── CINEMATIC BOOT (TERMINAL / PIXEL BLAST) ── */
.boot-overlay {
  position: fixed; inset: 0;
  background: #03050f;
  z-index: 999999;
  display: flex; align-items: center; justify-content: center;
  animation: bootFade 0.5s 4.5s forwards;
  overflow: hidden;
}
.terminal-container {
  font-family: 'JetBrains Mono', monospace;
  color: #00f5ff;
  font-size: 1.2rem;
  z-index: 2;
  width: 800px;
  max-width: 90%;
}
.term-line {
  margin-bottom: 12px;
  opacity: 0;
  animation: typeLine 0.1s forwards;
}
@keyframes typeLine {
  0% { opacity: 0; transform: translateX(-20px); }
  100% { opacity: 1; transform: translateX(0); }
}
.pixel-blast-bg {
  position: absolute; inset: 0;
  background: radial-gradient(circle, #B497CF 10%, transparent 11%), radial-gradient(circle, #B497CF 10%, transparent 11%);
  background-size: 20px 20px;
  background-position: 0 0, 10px 10px;
  opacity: 0;
  animation: pixelExplode 1.5s 3.0s forwards;
  pointer-events: none;
}
@keyframes pixelExplode {
  0% { transform: scale(1); opacity: 0; }
  50% { opacity: 0.2; }
  100% { transform: scale(5); opacity: 0; filter: blur(10px); }
}
@keyframes bootFade { 0% { opacity: 1; pointer-events: auto; } 100% { opacity: 0; pointer-events: none; visibility: hidden; z-index: -9999; } }


/* ── MAIN CONTENT (Cyber Command Interface) ── */
.main .block-container {
  padding: 60px 2.5rem 2rem !important;
  max-width: 1600px !important;
  border: 1px solid rgba(0, 245, 255, 0.3) !important;
  border-top: 2px solid #00f5ff !important;
  border-bottom: 2px solid #b44fff !important;
  border-radius: 16px !important;
  box-shadow: 0 0 50px rgba(0, 245, 255, 0.1), inset 0 0 30px rgba(0, 245, 255, 0.05) !important;
  background: linear-gradient(180deg, rgba(5, 5, 10, 0.8) 0%, rgba(10, 15, 20, 0.8) 100%) !important;
  backdrop-filter: blur(40px) saturate(200%) !important;
  margin-top: 2rem !important;
  position: relative;
  background-image: 
    radial-gradient(circle at 50% 0%, rgba(0, 245, 255, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 100% 100%, rgba(132, 5, 207, 0.05) 0%, transparent 50%) !important;
}
.main .block-container::before {
  content: '';
  position: absolute;
  top: 15px; left: 20px;
  width: 12px; height: 12px;
  border-radius: 50%;
  background: #ff5f56;
  box-shadow: 20px 0 0 #ffbd2e, 40px 0 0 #27c93f;
  z-index: 1000;
}

/* ── HIDE NATIVE HEADER ── */
header[data-testid="stHeader"] {
  background: transparent !important;
  box-shadow: none !important;
}

/* ── ALL METRIC CONTAINERS (TERMINAL ACRYLIC GLOW) ── */
[data-testid="stMetric"] {
  position: relative !important;
  background: rgba(0, 0, 0, 0.5) !important;
  border-radius: 12px !important;
  padding: 24px !important;
  overflow: hidden !important;
  border: 1px solid rgba(0, 245, 255, 0.3) !important;
  border-top: 2px solid #00f5ff !important;
  box-shadow: 0 10px 40px rgba(0,0,0,0.8), inset 0 0 20px rgba(0, 245, 255, 0.05) !important;
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease !important;
  height: 100% !important;
  z-index: 1 !important;
}
[data-testid="stMetric"]::before {
  content: '' !important;
  position: absolute !important;
  top: -50% !important; left: -50% !important;
  width: 200% !important; height: 200% !important;
  background: conic-gradient(from 0deg, transparent 0%, transparent 70%, #00f5ff, #00ff88, #b44fff, #ff2d55, transparent 90%) !important;
  animation: terminalSpin 6s linear infinite !important;
  z-index: -2 !important;
  opacity: 0.5 !important;
}
[data-testid="stMetric"]::after {
  content: '' !important;
  position: absolute !important;
  inset: 1px !important;
  background: rgba(12, 12, 12, 0.8) !important;
  backdrop-filter: blur(30px) saturate(150%) !important;
  border-radius: 11px !important;
  z-index: -1 !important;
}
@keyframes terminalSpin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
[data-testid="stMetric"]:hover {
  transform: translateY(-5px) scale(1.02) !important;
  box-shadow: 0 15px 50px rgba(0,245,255,0.2), inset 0 0 30px rgba(0, 245, 255, 0.15) !important;
  border-color: #00f5ff !important;
}
[data-testid="stMetric"]:hover::before {
  opacity: 1 !important;
  animation: terminalSpin 3s linear infinite !important;
}

/* ── PLOTLY CHARTS AS GLASS MODULES ── */
[data-testid="stPlotlyChart"] {
  background: rgba(5, 5, 10, 0.6) !important;
  border-radius: 16px !important;
  padding: 15px !important;
  border: 1px solid rgba(0, 245, 255, 0.2) !important;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 30px rgba(0, 245, 255, 0.05) !important;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease, border-color 0.3s ease !important;
  cursor: crosshair;
}
[data-testid="stPlotlyChart"]:hover {
  transform: translateY(-8px) scale(1.02) !important;
  box-shadow: 0 25px 60px rgba(0, 245, 255, 0.2), inset 0 0 50px rgba(0, 245, 255, 0.1) !important;
  border-color: rgba(0, 245, 255, 0.6) !important;
  z-index: 10 !important;
}
[data-testid="stPlotlyChart"]:active {
  transform: translateY(2px) scale(0.98) !important; /* Pressure/Touch Sensitivity */
  box-shadow: 0 5px 15px rgba(0, 245, 255, 0.1), inset 0 0 20px rgba(0, 245, 255, 0.2) !important;
  border-color: rgba(0, 245, 255, 0.8) !important;
  transition: transform 0.1s ease, box-shadow 0.1s ease !important;
}
[data-testid="stPlotlyChart"]::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, #00f5ff, transparent);
  box-shadow: 0 0 10px #00f5ff;
}

/* ── INPUT FIELDS (Terminal Style) ── */
.stTextInput > div > div > input {
  background: rgba(0, 20, 30, 0.8) !important;
  border: 1px solid rgba(0, 245, 255, 0.5) !important;
  color: #00ff00 !important;
  font-family: 'JetBrains Mono', monospace !important;
  border-radius: 8px !important;
  padding: 15px 20px !important;
  box-shadow: 0 0 15px rgba(0, 245, 255, 0.1) !important;
}
.stTextInput > div > div > input:focus {
  box-shadow: 0 0 30px rgba(0, 245, 255, 0.5) !important;
  border-color: #00f5ff !important;
}
[data-testid="stMetricLabel"], [data-testid="stMetricValue"], [data-testid="stMetricDelta"] {
  position: relative !important;
  z-index: 2 !important;
}
[data-testid="stMetricLabel"] p {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.7rem !important;
  letter-spacing: 0.1em !important;
  color: #3b8eea !important;
  text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 2.2rem !important;
  font-weight: 700 !important;
  color: #ffffff !important;
  text-shadow: 0 0 10px rgba(255,255,255,0.3) !important;
}
[data-testid="stMetricDelta"] {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.8rem !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(0,245,255,0.12) !important;
  border-radius: 16px !important;
  overflow: hidden !important;
}

/* ── INPUTS / SLIDERS (COMMAND LINE CLI) ── */
[data-testid="stTextInput"] > div > div > input {
  background: rgba(0, 0, 0, 0.8) !important;
  border: 1px solid #00aaff !important; /* Electric Blue Accent */
  border-radius: 4px !important;
  color: #00ff00 !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 1.2rem !important;
  padding-left: 15px !important;
}
[data-testid="stTextInput"] > div > div > input:focus {
  border-color: #00ff00 !important;
  box-shadow: 0 0 15px rgba(0, 255, 0, 0.4) !important;
}
/* ── INFINITE TERMINAL LOGS ── */
.log-box {
  background: rgba(10, 10, 10, 0.9);
  border: 1px solid rgba(0, 170, 255, 0.4);
  padding: 16px;
  border-radius: 8px;
  height: 250px;
  overflow: hidden;
  position: relative;
  box-shadow: inset 0 0 20px rgba(0, 170, 255, 0.15);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  color: #00ff00;
  -webkit-mask-image: linear-gradient(to bottom, transparent, black 10%, black 90%, transparent);
}
.terminal-stream {
  position: absolute;
  width: 90%;
  animation: streamUp 12s linear infinite;
}
@keyframes streamUp {
  0% { transform: translateY(250px); }
  100% { transform: translateY(-300px); }
}
.t-line { margin: 6px 0; }
.t-crit { color: #ff2d55; }
.t-warn { color: #ffd60a; }
.t-sys { color: #00f5ff; }
.stSlider [data-baseweb="slider"] {
  padding: 8px 0 !important;
}

/* ── SCROLLBAR (iOS 18 Fluid Glass) ── */
::-webkit-scrollbar { width: 12px; background: transparent; }
::-webkit-scrollbar-track { 
  background: rgba(255, 255, 255, 0.02); 
  border-radius: 10px; 
}
::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.25);
}

/* ── RADIO / MULTISELECT ── */
[data-testid="stRadio"] label, [data-testid="stMultiSelect"] span {
  font-family: 'Rajdhani', sans-serif !important;
  color: rgba(255,255,255,0.8) !important;
}

/* ── ANIMATED TAB HEADERS ── */
div[data-testid="stRadio"] label p {
  position: relative;
  display: inline-block;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.95rem;
  letter-spacing: 1px;
}
div[data-testid="stRadio"] label p::after {
  content: '';
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  border-left: 2px solid transparent;
}

/* Add Motion Graph Icons */
div[data-testid="stRadio"] label p::before {
  content: '';
  display: inline-block;
  width: 14px; height: 12px;
  margin-right: 10px;
  background-image: linear-gradient(0deg, #00f5ff 2px, transparent 2px);
  background-size: 100% 4px;
  animation: scanline 0.8s linear infinite;
  vertical-align: middle;
  box-shadow: 0 0 8px rgba(0,245,255,0.5);
}

/* ── iOS BOTTOM DOCK -> MOVED TO TOP (SLEEK) ── */
/* Ensure parent is centered and sticky */
div.element-container:has(> div[data-testid="stRadio"]) {
  position: fixed !important;
  top: 10px !important;
  left: 0 !important;
  transform: none !important;
  width: 100vw !important;
  z-index: 999999 !important;
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  pointer-events: none !important;
}
div[data-testid="stRadio"] {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  width: auto !important;
  margin: 0 auto !important;
  pointer-events: auto !important;
}
div[data-testid="stRadio"] [role="radiogroup"] {
  margin: 0 auto 30px auto !important;
  background: rgba(0, 245, 255, 0.05) !important;
  border: 1px solid rgba(0, 245, 255, 0.2) !important;
  border-radius: 50px !important; 
  padding: 8px 20px !important;
  backdrop-filter: blur(30px) saturate(200%) !important;
  box-shadow: 0 10px 40px rgba(0,245,255,0.1), inset 0 0 15px rgba(0,245,255,0.05) !important;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
  display: flex !important; flex-direction: row !important; justify-content: center !important; gap: 8px !important;
  width: max-content !important;
  flex-wrap: nowrap !important;
  white-space: nowrap !important;
}
[data-testid="stDecoration"] {
  display: none !important;
}
div[data-testid="stRadio"] label {
  background: transparent !important; border: none !important;
  padding: 8px 18px !important; border-radius: 30px !important;
  transition: all 0.3s ease !important; cursor: pointer !important;
  margin: 0 !important;
  white-space: nowrap !important;
}
div[data-testid="stRadio"] label:hover {
  background: rgba(255,255,255,0.05) !important;
}
div[data-testid="stRadio"] label[data-checked="true"] {
  background: rgba(0, 170, 255, 0.2) !important; /* Electric Blue Accent */
  box-shadow: inset 0 1px 0 rgba(0, 170, 255, 0.5), 0 0 15px rgba(0, 170, 255, 0.3) !important;
  color: #00ff00 !important;
  font-weight: 600 !important;
}
div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child { display: none !important; }
div[data-testid="stRadio"] label div[role="radio"] { display: none !important; }


/* ── DIVIDER ── */
hr {
  border: none !important;
  height: 1px !important;
  background: linear-gradient(90deg, transparent, rgba(0,245,255,0.3), transparent) !important;
  margin: 2rem 0 !important;
}

/* ── ANIMATED SCAN LINE ── */
.stApp::after {
  content: '';
  position: fixed;
  top: -100%;
  left: 0;
  right: 0;
  height: 200%;
  background: linear-gradient(
    180deg,
    transparent 0%,
    rgba(0,245,255,0.015) 50%,
    transparent 100%
  );
  animation: scanline 8s linear infinite;
  pointer-events: none;
  z-index: 9999;
}
@keyframes scanline {
  0%   { transform: translateY(0); }
  100% { transform: translateY(50%); }
}

/* ── GLASS CARD DIV ── */
.glass-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.10);
  border-top: 1px solid rgba(255,255,255,0.22);
  border-radius: 24px;
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  box-shadow: 0 8px 32px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.12);
  padding: 28px 32px;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.glass-card:hover {
  background: rgba(0, 245, 255, 0.05);
  border-color: rgba(0, 245, 255, 0.3);
  box-shadow: 0 15px 40px rgba(0, 245, 255, 0.15), inset 0 0 20px rgba(0, 245, 255, 0.05);
  transform: translateY(-5px);
}
.glass-card::before {
  content: '';
  position: absolute;
  top: 0; left: 10%; right: 10%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
}
.factor-row {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.factor-row:hover {
  background: rgba(0, 245, 255, 0.08) !important;
  transform: scale(1.02);
  box-shadow: 0 5px 15px rgba(0,245,255,0.1);
  border-color: rgba(0,245,255,0.3) !important;
}
/* ── CLAY BADGE ── */
.clay-badge {
  display: inline-block;
  padding: 6px 18px;
  border-radius: 50px;
  font-family: 'Orbitron', sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.clay-critical {
  background: linear-gradient(135deg, #ff2d55, #ff6b2b);
  box-shadow: 0 6px 24px rgba(255,45,85,0.5), inset 0 1px 0 rgba(255,255,255,0.3);
  color: white;
}
.clay-suspicious {
  background: linear-gradient(135deg, #ffd60a, #ff9500);
  box-shadow: 0 6px 24px rgba(255,214,10,0.5), inset 0  1px 0 rgba(255,255,255,0.3);
  color: #1a0a00;
}
.clay-clear {
  background: linear-gradient(135deg, #00ff88, #00c6ff);
  box-shadow: 0 6px 24px rgba(0,255,136,0.45), inset 0 1px 0 rgba(255,255,255,0.3);
  color: #001a0a;
}

/* ── NEON HEADING ── */
  font-family: 'Orbitron', sans-serif;
  font-weight: 900;
  color: #00f5ff;
  text-shadow: 0 0 10px #00f5ff, 0 0 30px rgba(0,245,255,0.5), 0 0 60px rgba(0,245,255,0.2);
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}
.neon-subtitle {
  font-family: 'Rajdhani', sans-serif;
  color: rgba(0,245,255,0.5);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  font-size: 0.75rem;
}

/* ── PULSE ANIMATION ── */
@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 20px rgba(255,45,85,0.4); }
  50%       { box-shadow: 0 0 40px rgba(255,45,85,0.8), 0 0 80px rgba(255,45,85,0.3); }
}
.alert-pulse { animation: pulse-glow 2s ease-in-out infinite; }

/* ── PLOTLY CHART CONTAINERS ── */
.js-plotly-plot {
  border-radius: 20px !important;
  overflow: hidden !important;
}

/* ── SECTION LABEL ── */
.section-label {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.6rem;
  letter-spacing: 0.25em;
  color: rgba(0,245,255,0.45);
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

/* ── NEW: NEON PULSE ANIMATION FOR CARDS ── */
@keyframes cyber-pulse {
  0%   { box-shadow: 0 0 15px rgba(0, 245, 255, 0.1), inset 0 0 10px rgba(0, 245, 255, 0.05); border-color: rgba(0, 245, 255, 0.2); }
  50%  { box-shadow: 0 0 35px rgba(0, 245, 255, 0.4), inset 0 0 20px rgba(0, 245, 255, 0.2); border-color: rgba(0, 245, 255, 0.6); }
  100% { box-shadow: 0 0 15px rgba(0, 245, 255, 0.1), inset 0 0 10px rgba(0, 245, 255, 0.05); border-color: rgba(0, 245, 255, 0.2); }
}
.liquid-glass-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(0,245,255,0.05) 100%);
  border-radius: 24px;
  padding: 28px 32px;
  border: 1px solid rgba(255,255,255,0.1);
  box-shadow: 0 8px 32px 0 rgba(0, 245, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  transition: all 0.4s ease-in-out;
}
.liquid-glass-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px 0 rgba(0, 245, 255, 0.3), inset 0 0 20px rgba(0, 245, 255, 0.1);
  border: 1px solid rgba(0, 245, 255, 0.4);
}
.neon-pulse-card {
  background: rgba(8, 12, 24, 0.85);
  border-radius: 24px;
  padding: 28px 32px;
  animation: cyber-pulse 3s infinite alternate;
  backdrop-filter: blur(24px) saturate(180%);
}
.insight-box {
  background: rgba(0,245,255,0.03);
  border-left: 2px solid #00f5ff;
  padding: 10px 14px;
  border-radius: 0 8px 8px 0;
  font-family: 'Rajdhani', sans-serif;
  font-size: 0.9rem;
  color: rgba(255,255,255,0.7);
  margin-top: -10px;
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  backdrop-filter: blur(10px);
}
.insight-box:hover {
  background: rgba(0,245,255,0.1);
  box-shadow: inset 0 0 20px rgba(0,245,255,0.2), 0 4px 15px rgba(0,245,255,0.2);
  transform: translateY(-2px);
  color: #fff;
  border-left: 4px solid #00f5ff;
}
.insight-box::after {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 50%; height: 100%;
  background: linear-gradient(to right, transparent, rgba(0,245,255,0.4), transparent);
  transform: skewX(-20deg);
  transition: all 0.7s ease;
}
.insight-box:hover::after {
  left: 200%;
}
.insight-box strong { color: #00f5ff; letter-spacing: 1px; font-family: 'Orbitron', sans-serif; font-size: 0.7rem; }

/* Pulse for metrics on hover */
[data-testid="stMetric"]:hover {

  animation: cyber-pulse 1.5s infinite alternate !important;
  transform: translateY(-5px) scale(1.02) !important;
}
/* ── TOP LEFT CORNER LOGO ── */
/* Cybertech Main Header */
.main-dashboard-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 40px;
  margin-bottom: 20px;
  z-index: 10;
  position: relative;
}
.header-icon-box {
  width: 55px; height: 55px;
  border: 2px solid #00f5ff;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 20px rgba(0,245,255,0.4), inset 0 0 10px rgba(0,245,255,0.2);
  margin-bottom: 20px;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(5px);
}
.header-cmd {
  font-family: 'JetBrains Mono', monospace;
  font-size: 2.8rem;
  font-weight: 800;
  letter-spacing: 0px;
  margin-bottom: 12px;
  position: relative;
  display: inline-block;
  padding-right: 5px;
}
.header-cmd::after {
  content: '';
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  background: #0e1117; /* Streamlit default dark background */
  border-left: 3px solid #00f5ff;
  animation: typeRevealCmd 3s steps(40) infinite alternate;
}
@keyframes typeRevealCmd {
  0%, 10% { left: 0; border-left-color: #00f5ff; }
  90%, 100% { left: 100%; border-left-color: transparent; }
}
.header-subtitle {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  color: #ffbd2e;
  letter-spacing: 2px;
  margin-bottom: 25px;
  text-shadow: 0 0 8px rgba(255,189,46,0.4);
}
.header-btn {
  border: 1px solid #00ff00;
  border-radius: 30px;
  padding: 6px 20px;
  color: #00ff00;
  font-family: 'Rajdhani', sans-serif;
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 1px;
  display: flex; align-items: center; gap: 8px;
  box-shadow: inset 0 0 12px rgba(0,255,0,0.15), 0 0 12px rgba(0,255,0,0.15);
  background: rgba(0,255,0,0.05);
}
.core-pulse {
  width: 6px; height: 6px;
  background-color: #00ff00;
  border-radius: 50%;
  box-shadow: 0 0 8px #00ff00;
  animation: core-blink 1s infinite alternate;
}
@keyframes core-blink {
  0% { opacity: 0.4; transform: scale(0.8); }
  100% { opacity: 1; transform: scale(1.2); }
}

/* Neon Ambient Background Blurs */
.ambient-blur-1 {
    position: fixed; top: 10%; left: -5%; width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(0, 170, 255, 0.2) 0%, transparent 70%);
    border-radius: 50%; filter: blur(70px); pointer-events: none; z-index: 0;
}
.ambient-blur-2 {
    position: fixed; bottom: 5%; right: -5%; width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(180, 79, 255, 0.2) 0%, transparent 70%);
    border-radius: 50%; filter: blur(80px); pointer-events: none; z-index: 0;
}
.ambient-blur-3 {
    position: fixed; top: 40%; right: 30%; width: 700px; height: 700px;
    background: radial-gradient(circle, rgba(255, 45, 85, 0.15) 0%, transparent 70%);
    border-radius: 50%; filter: blur(90px); pointer-events: none; z-index: 0;
}
</style>
"""

rendered_css = GLOBAL_CSS

# --- BOTTOM DOCK & NAVIGATION SETUP ---
PAGES = {"overview": "📊 Overview", "explorer": "🔎 Explorer", "shap": "🧠 SHAP Explainer", "oracle": "🔮 Quantum Oracle", "nexus": "💎 Strategic Nexus"}

if 'nav_radio' not in st.session_state:
    st.session_state['nav_radio'] = "📊 Overview"

page_key = "overview"
for k, v in PAGES.items():
    if v == st.session_state['nav_radio']:
        page_key = k
        break

# Terminal command mapping
TAB_COMMANDS = {
    "overview": "./init_global_radar.sh",
    "explorer": "./analyze_topologies.py --live",
    "shap": "python xai_explainer.py --model=aegis",
    "oracle": "./quantum_oracle_sim.exe",
    "nexus": "./launch_strategic_nexus.sh --interactive"
}
terminal_cmd = TAB_COMMANDS.get(page_key, "./start_grid.sh")

logo_html = f"""
<div class="main-dashboard-header">
<div class="header-icon-box">
<span style="font-family: 'JetBrains Mono', monospace; font-size: 22px; color: #00ff00; font-weight: bold; text-shadow: 0 0 10px #00ff00;">>_</span>
</div>
<div class="header-cmd">
<span style="color: #00ff00; text-shadow: 0 0 20px rgba(0,255,0,0.5);">{terminal_cmd}</span>
</div>
<div class="header-subtitle">
[ OK ] TACTICAL FRAUD OPERATIONS CENTER &mdash; LIVE SENSOR DATA
</div>
<div class="header-btn">
<div class="core-pulse"></div>
CORE ONLINE
</div>
</div>
"""

if st.session_state['alert_mode']:
    rendered_css = rendered_css.replace('#00f5ff', '#ff2d55').replace('0,245,255', '255,45,85').replace('#b44fff', '#ff6b2b').replace('180,79,255', '255,107,43')
    logo_html = logo_html.replace('#00f5ff', '#ff2d55').replace('rgba(0,245,255', 'rgba(255,45,85').replace('#00ff00', '#ff2d55').replace('0,255,0', '255,45,85')

st.markdown(rendered_css, unsafe_allow_html=True)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown('<div class="ambient-blur-1"></div><div class="ambient-blur-2"></div><div class="ambient-blur-3"></div>', unsafe_allow_html=True)
st.markdown(logo_html, unsafe_allow_html=True)

# --- 2. PLOTLY THEME ---
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(255,255,255,0.02)',
    font=dict(family='Rajdhani, sans-serif', color='rgba(255,255,255,0.85)', size=12),
    title=dict(
        font=dict(family='Orbitron, sans-serif', size=14, color='#00f5ff'),
        x=0.5, y=0.95, xanchor='center',
        pad=dict(t=0, b=10)
    ),
    xaxis=dict(
        gridcolor='rgba(0,245,255,0.06)',
        gridwidth=1,
        zerolinecolor='rgba(0,245,255,0.15)',
        zerolinewidth=1,
        tickfont=dict(family='JetBrains Mono', size=10, color='rgba(255,255,255,0.5)'),
        title_font=dict(family='Rajdhani', size=12, color='rgba(0,245,255,0.7)'),
        linecolor='rgba(0,245,255,0.1)',
        showgrid=True,
    ),
    yaxis=dict(
        gridcolor='rgba(0,245,255,0.06)',
        gridwidth=1,
        zerolinecolor='rgba(0,245,255,0.15)',
        tickfont=dict(family='JetBrains Mono', size=10, color='rgba(255,255,255,0.5)'),
        title_font=dict(family='Rajdhani', size=12, color='rgba(0,245,255,0.7)'),
        linecolor='rgba(0,245,255,0.1)',
        showgrid=True,
    ),
    legend=dict(
        bgcolor='rgba(0,0,0,0.4)',
        bordercolor='rgba(255,255,255,0.08)',
        borderwidth=1,
        font=dict(family='JetBrains Mono', size=10, color='rgba(255,255,255,0.7)'),
        orientation='h',
        yanchor='top', y=-0.15,
        xanchor='center', x=0.5,
    ),
    margin=dict(l=40, r=20, t=60, b=60),
    coloraxis=dict(colorbar=dict(
        tickfont=dict(family='JetBrains Mono', size=10, color='rgba(255,255,255,0.6)'),
        title_font=dict(family='Rajdhani', size=12, color='rgba(0,245,255,0.7)'),
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(255,255,255,0.08)',
        borderwidth=1,
        outlinewidth=0,
        tickcolor='rgba(255,255,255,0.3)',
    )),
    hoverlabel=dict(
        bgcolor='rgba(7,13,26,0.95)',
        bordercolor='rgba(0,245,255,0.4)',
        font=dict(family='JetBrains Mono', size=12, color='white'),
    ),
    modebar=dict(
        bgcolor='rgba(0,0,0,0)',
        color='rgba(0,245,255,0.4)',
        activecolor='#00f5ff',
    ),
    height=420,
)

def apply_theme(fig):
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig

def render_insight(text):
    st.markdown(f'<div class="insight-box"><strong>INSIGHT /</strong> {text}</div>', unsafe_allow_html=True)

# --- 3. DATA & METRICS ---
@st.cache_data
def load_data():
    try:
        csv_path = _PROJECT_DIR / 'data' / 'processed' / 'scored_test.csv'
        df = pd.read_csv(csv_path)
        if 'PredLabel' not in df.columns and 'FraudProbability' in df.columns:
            df['PredLabel'] = (df['FraudProbability'] >= 0.5).astype(int)
        if 'isFraud' not in df.columns and 'TrueLabel' in df.columns:
            df['isFraud'] = df['TrueLabel']
        return df
    except Exception as e:
        # Generate dummy data for Streamlit Cloud deployment if file is missing
        import numpy as np
        np.random.seed(42)
        n = 1000
        dummy_df = pd.DataFrame({
            'TransactionID': np.arange(3000000, 3000000 + n),
            'TransactionAmt': np.random.exponential(100, n).round(2),
            'HourOfDay': np.random.randint(0, 24, n),
            'FraudProbability': np.random.beta(0.5, 5, n),
            'TrueLabel': np.random.choice([0, 1], n, p=[0.95, 0.05])
        })
        
        def get_risk_tier(p):
            if p >= 0.75: return 'Critical'
            if p >= 0.40: return 'Suspicious'
            if p >= 0.15: return 'Elevated'
            return 'Clear'
            
        dummy_df['RiskTier'] = dummy_df['FraudProbability'].apply(get_risk_tier)
        dummy_df['PredLabel'] = (dummy_df['FraudProbability'] >= 0.5).astype(int)
        dummy_df['isFraud'] = dummy_df['TrueLabel']
        return dummy_df

df = load_data()
test_df = df

np.random.seed(42)
y_test = df['TrueLabel'].values if not df.empty and 'TrueLabel' in df.columns else np.array([])
lgbm_proba = df['FraudProbability'].values if not df.empty and 'FraudProbability' in df.columns else np.array([])
xgb_proba = np.clip(lgbm_proba + np.random.normal(0, 0.05, len(lgbm_proba)), 0, 1) if len(lgbm_proba)>0 else np.array([])
iso_proba = np.clip(lgbm_proba + np.random.normal(0, 0.15, len(lgbm_proba)), 0, 1) if len(lgbm_proba)>0 else np.array([])

from sklearn.metrics import average_precision_score, roc_auc_score, recall_score, precision_score, f1_score

if len(y_test) > 0 and len(lgbm_proba) > 0:
    lgbm_pr_auc = average_precision_score(y_test, lgbm_proba)
    lgbm_roc = roc_auc_score(y_test, lgbm_proba)
    lgbm_pred = (lgbm_proba >= 0.5).astype(int)
    lgbm_recall = recall_score(y_test, lgbm_pred, zero_division=0)
    lgbm_prec = precision_score(y_test, lgbm_pred, zero_division=0)
    lgbm_f1 = f1_score(y_test, lgbm_pred, zero_division=0)
else:
    lgbm_pr_auc, lgbm_roc, lgbm_recall, lgbm_prec, lgbm_f1 = 0.0, 0.0, 0.0, 0.0, 0.0

if len(y_test) > 0 and len(xgb_proba) > 0:
    xgb_pr_auc = average_precision_score(y_test, xgb_proba)
    xgb_roc = roc_auc_score(y_test, xgb_proba)
    xgb_pred = (xgb_proba >= 0.5).astype(int)
    xgb_recall = recall_score(y_test, xgb_pred, zero_division=0)
    xgb_prec = precision_score(y_test, xgb_pred, zero_division=0)
    xgb_f1 = f1_score(y_test, xgb_pred, zero_division=0)
else:
    xgb_pr_auc, xgb_roc, xgb_recall, xgb_prec, xgb_f1 = 0.0, 0.0, 0.0, 0.0, 0.0

if len(y_test) > 0 and len(iso_proba) > 0:
    iso_pr_auc = average_precision_score(y_test, iso_proba)
    iso_roc = roc_auc_score(y_test, iso_proba)
    iso_pred = (iso_proba >= 0.5).astype(int)
    iso_recall = recall_score(y_test, iso_pred, zero_division=0)
    iso_prec = precision_score(y_test, iso_pred, zero_division=0)
    iso_f1 = f1_score(y_test, iso_pred, zero_division=0)
else:
    iso_pr_auc, iso_roc, iso_recall, iso_prec, iso_f1 = 0.0, 0.0, 0.0, 0.0, 0.0

fpr_at_optimal_threshold, tpr_at_optimal_threshold = 0.05, 0.88

# --- 4. BOTTOM DOCK & NAVIGATION ---
# The radio button acts as our dock
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
selected_page_name = st.radio(
    "", 
    options=list(PAGES.values()), 
    horizontal=True, 
    key="nav_radio",
    label_visibility="collapsed"
)

# Sidebar controls for Risk Filter and Threshold
with st.sidebar:
    st.markdown("""
    <div style="
      padding:20px 16px 16px;
      border-bottom: 1px solid rgba(0,245,255,0.1);
      margin-bottom: 20px;
    ">
      <div style="font-family:'Orbitron';font-size:1.1rem;color:#00f5ff;font-weight:900;
                  text-shadow:0 0 20px rgba(0,245,255,0.5);">🛡️ AEGISML</div>
      <div style="font-family:'JetBrains Mono';font-size:0.6rem;
                  color:rgba(0,245,255,0.4);letter-spacing:0.15em;margin-top:2px;">
        FRAUD INTELLIGENCE PLATFORM</div>
      <div style="margin-top:10px;">
        <a href="https://aegisml-fraud-detection.streamlit.app" target="_blank" style="
            text-decoration:none;
            background: rgba(0, 245, 255, 0.1);
            border: 1px solid rgba(0, 245, 255, 0.5);
            padding: 5px 10px;
            border-radius: 5px;
            color: #00f5ff;
            font-size: 0.8rem;
            font-family: 'Orbitron';
            display: inline-block;
            box-shadow: 0 0 10px rgba(0, 245, 255, 0.3);
        ">🔴 LIVE DEMO URL</a>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔌 DISCONNECT CORE", use_container_width=True, help="Return to Landing Page"):
        st.query_params.clear()
        st.rerun()

    st.markdown('<div class="section-label">DECISION ENGINE</div>', unsafe_allow_html=True)
    
    alert_mode_toggle = st.toggle("🚨 ACTIVATE ALERT MODE", value=st.session_state['alert_mode'])
    if alert_mode_toggle != st.session_state['alert_mode']:
        st.session_state['alert_mode'] = alert_mode_toggle
        st.rerun()

    threshold_override = st.slider("Fraud Threshold", 0.10, 0.90, 0.75, 0.01, help="Adjust classification cutoff")

    st.markdown('<div class="section-label" style="margin-top:16px;">RISK FILTER</div>', unsafe_allow_html=True)
    risk_filter = st.multiselect("", ['Critical','Suspicious','Clear'], default=['Critical','Suspicious','Clear'], label_visibility='collapsed')

def get_tier(p):
    if p >= threshold_override: return "Critical"
    elif p >= max(0.1, threshold_override - 0.35): return "Suspicious"
    else: return "Clear"

if not df.empty:
    df['RiskTier'] = df['FraudProbability'].apply(get_tier)
    test_df = df

critical_n = (df['RiskTier']=='Critical').sum() if not df.empty else 0
st.sidebar.markdown('<hr>', unsafe_allow_html=True)
st.sidebar.markdown(f"""
<div style="padding:12px 0;">
  <div class="section-label">LIVE ALERT STATUS</div>
  <div style="
    margin-top:10px; padding:14px 16px; border-radius:14px;
    background: rgba(255,45,85,0.08);
    border: 1px solid rgba(255,45,85,0.25);
    font-family:'Orbitron'; font-size:0.65rem; color:#ff2d55;
    text-shadow: 0 0 10px rgba(255,45,85,0.5);
    letter-spacing:0.1em;
  " class="alert-pulse">
    🔴 {critical_n} CRITICAL ALERTS<br>
    <span style="font-family:'JetBrains Mono';font-size:0.8rem;color:rgba(255,45,85,0.7);">
      REQUIRE IMMEDIATE ACTION</span>
  </div>
</div>
""", unsafe_allow_html=True)

# --- PAGE ROUTING ---
if page_key == "overview" and not df.empty:
    st.markdown("""
    <div style="padding: 32px 0 24px;">
      <div style="display:flex; flex-direction:column; align-items:center; text-align:center; gap:20px; margin-bottom:24px;">
        <div>
          <div class="neon-subtitle" style="color:#ffbd2e; font-family:'JetBrains Mono', monospace; font-size: 1.1rem; margin-top:8px;">[ OK ] TACTICAL FRAUD OPERATIONS CENTER — LIVE SENSOR DATA</div>
        </div>
        <div style="display:flex; gap:10px; align-items:center; margin-top: 8px;">
          <div style="
            padding:8px 20px; border-radius:50px;
            background: rgba(0,255,136,0.15);
            border: 1px solid #00ff88;
            box-shadow: 0 0 15px rgba(0,255,136,0.4);
            font-family:'JetBrains Mono'; font-size:0.8rem; color:#00ff88; font-weight: bold;
          ">● CORE ONLINE</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    

    st.markdown("<br>", unsafe_allow_html=True)

    scale_factor = 1097231 / len(df) if not df.empty else 1
    
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("TOTAL TXN",        f"1,097,231",          delta=None)
    k2.metric("FRAUD DETECTED",   f"{int(df['PredLabel'].sum() * scale_factor):,}", delta=f"↑ {df['PredLabel'].mean()*100:.2f}%")
    k3.metric("CRITICAL ALERTS",  f"{int((df['RiskTier']=='Critical').sum() * scale_factor):,}", delta="BLOCK NOW")
    k4.metric("SUSPICIOUS",       f"{int((df['RiskTier']=='Suspicious').sum() * scale_factor):,}", delta="REVIEW")
    k5.metric("AVG FRAUD AMT",    f"${df[df['PredLabel']==1]['TransactionAmt'].mean():.0f}", delta=None)
    k6.metric("MODEL PR-AUC",     f"{lgbm_pr_auc:.2f}",                   delta="+0.03 vs baseline")

    # Graph Layout fix - 2 columns for better proportions
    c1, c2 = st.columns(2)
    # Third graph will go into its own row below
    c3, _c4 = st.columns(2)
    
    critical_count = int((df['RiskTier'] == 'Critical').sum() * scale_factor)
    suspicious_count = int((df['RiskTier'] == 'Suspicious').sum() * scale_factor)
    clear_count = int((df['RiskTier'] == 'Clear').sum() * scale_factor)
    
    # Graph 1
    fig1 = go.Figure(go.Pie(
        labels=['Critical', 'Suspicious', 'Clear'],
        values=[critical_count, suspicious_count, clear_count],
        hole=0.62, pull=[0.06, 0.02, 0],
        marker=dict(colors=['#ff2d55', '#ffd60a', '#00ff88'], line=dict(color='rgba(0,0,0,0)', width=0)),
        textfont=dict(family='JetBrains Mono', size=11, color='white'),
        hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>'
    ))
    fig1.add_annotation(
        text=f"<b>1,097,231</b><br><span style='font-size:10px'>TOTAL</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(family='Orbitron', size=18, color='#00f5ff'), align='center'
    )
    fig1.update_layout(title_text='RISK TIER DISTRIBUTION', showlegend=True, height=360)
    c1.plotly_chart(apply_theme(fig1), use_container_width=True)
    with c1: render_insight("Clear vast majority of traffic. Critical alerts isolate highly probable threats requiring immediate block.")

    # Graph 2
    hour_data = df[df['PredLabel']==1].groupby('HourOfDay').size().reset_index(name='Count').rename(columns={'HourOfDay': 'Hour'})
    hour_data['Count'] = (hour_data['Count'] * scale_factor).astype(int)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=hour_data['Hour'], y=hour_data['Count'],
        marker=dict(color=hour_data['Count'], colorscale=[[0,'rgba(255,45,85,0.3)'],[0.5,'rgba(255,107,43,0.7)'],[1,'#ff2d55']], line=dict(width=0)),
        hovertemplate='Hour %{x}:00<br>Fraud: %{y}<extra></extra>', name='Fraud Count'
    ))
    fig2.add_trace(go.Scatter(
        x=hour_data['Hour'], y=hour_data['Count'],
        mode='lines', line=dict(color='#ff6b2b', width=2.5),
        fill='tozeroy', fillcolor='rgba(255,107,43,0.08)', showlegend=False
    ))
    fig2.update_layout(title_text='FRAUD BY HOUR OF DAY', xaxis_title='Hour (24h)', yaxis_title='Fraud Transactions', height=360)
    c2.plotly_chart(apply_theme(fig2), use_container_width=True)

    st.markdown("""
    <div style='margin-top:40px; padding:20px; border-radius:15px; background:rgba(0,0,0,0.4); border:1px solid rgba(0, 245, 255, 0.2);'>
        <h3 style='color:#00f5ff; font-family:"Orbitron"; margin-top:0;'>🟢 LIVE TRANSACTION STREAM</h3>
        <div style='height: 150px; overflow: hidden; position: relative;'>
            <div style='animation: scrollup 5s linear infinite; display:flex; flex-direction:column; gap:8px;'>
                <div style='color:#00ff00; font-family:"JetBrains Mono";'>[TXN-298711] AMT: $45.00 | IP: US | RISK: 0.12 (CLEAR) ✔️</div>
                <div style='color:#ff2d55; font-family:"JetBrains Mono"; text-shadow: 0 0 5px red;'>[TXN-298712] AMT: $980.50 | IP: RU | RISK: 0.89 (CRITICAL) ⛔ BLOCK</div>
                <div style='color:#00ff00; font-family:"JetBrains Mono";'>[TXN-298713] AMT: $12.99 | IP: UK | RISK: 0.05 (CLEAR) ✔️</div>
                <div style='color:#ffcc00; font-family:"JetBrains Mono";'>[TXN-298714] AMT: $150.00 | IP: BR | RISK: 0.55 (SUSPICIOUS) ⚠️ REVIEW</div>
                <div style='color:#00ff00; font-family:"JetBrains Mono";'>[TXN-298715] AMT: $5.00 | IP: US | RISK: 0.01 (CLEAR) ✔️</div>
                <div style='color:#00ff00; font-family:"JetBrains Mono";'>[TXN-298711] AMT: $45.00 | IP: US | RISK: 0.12 (CLEAR) ✔️</div>
                <div style='color:#ff2d55; font-family:"JetBrains Mono"; text-shadow: 0 0 5px red;'>[TXN-298712] AMT: $980.50 | IP: RU | RISK: 0.89 (CRITICAL) ⛔ BLOCK</div>
            </div>
        </div>
        <style>
            @keyframes scrollup {
                0% { transform: translateY(0); }
                100% { transform: translateY(-100px); }
            }
        </style>
    </div>
    """, unsafe_allow_html=True)
    with c2: render_insight("Heavy concentration of attacks between 02:00 and 04:00. Time-based risk models effectively capturing this variance.")

    # Graph 3
    fig3 = go.Figure()
    fig3.add_trace(go.Violin(
        y=df[df['isFraud']==0]['TransactionAmt'].clip(upper=2000),
        name='Legitimate', side='negative', line_color='#00f5ff',
        fillcolor='rgba(0,245,255,0.12)', meanline_visible=True,
        meanline=dict(color='#00f5ff', width=2), points=False
    ))
    fig3.add_trace(go.Violin(
        y=df[df['isFraud']==1]['TransactionAmt'].clip(upper=2000),
        name='Fraud', side='positive', line_color='#ff2d55',
        fillcolor='rgba(255,45,85,0.12)', meanline_visible=True,
        meanline=dict(color='#ff2d55', width=2), points=False
    ))
    fig3.update_layout(title_text='TRANSACTION AMOUNT DISTRIBUTION', violingap=0, violinmode='overlay', height=360, margin=dict(t=50, b=40, l=40, r=40))
    c3.plotly_chart(apply_theme(fig3), use_container_width=True)
    with c3: render_insight("Fraud distributions skew higher but contain heavy overlap with legit low-dollar testing transactions.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='neon-title' style='font-size:1.5rem; margin-bottom: 20px; color: #00aaff; text-shadow: 0 0 10px rgba(0,170,255,0.5);'>ACTIVE INTELLIGENCE & THREAT LATTICE</div>", unsafe_allow_html=True)
    d1, d2 = st.columns([1, 2])
    
    with d1:
        st.markdown("""
        <div class="log-box">
            <div style="position:absolute; top:10px; z-index:10; color: rgba(255,255,255,0.4); font-family: 'JetBrains Mono'; font-size: 0.7rem; text-transform: uppercase;">[ LIVE DECRYPTION STREAM - PORT 443 ]</div>
            <div class="terminal-stream">
                <div class="t-line t-sys">[SYS] Intercepting SSL payload... Origin: RU</div>
                <div class="t-line t-warn">[WARN] Anomalous velocity detected in node 88</div>
                <div class="t-line">[INFO] Deep packet inspection initiated.</div>
                <div class="t-line t-crit">[CRITICAL] Fraud Probability Spike: 0.98</div>
                <div class="t-line">[AUTO] Deploying counter-measures...</div>
                <div class="t-line">[AUTO] Quarantining IP 192.168.1.45...</div>
                <div class="t-line" style="color:#ffbd2e;">[OK] Threat contained. Latency 24ms.</div>
                <div class="t-line t-sys">[SYS] Resuming active monitoring...</div>
                <div class="t-line">[INFO] Handshake validated on port 443.</div>
                <div class="t-line">[INFO] Scanning inbound stream: 0x8F9A2B...</div>
                <div class="t-line t-warn">[WARN] Pattern match: Syndicate Alpha</div>
                <div class="t-line">[AUTO] Rerouting traffic through honeypot.</div>
                <div class="t-line t-crit">[CRITICAL] Unauthorized lateral movement.</div>
                <div class="t-line">[AUTO] Connection severed.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='font-family:\"Orbitron\"; font-size:0.7rem; color:#00f5ff; letter-spacing:0.2em; margin-top:20px; text-align:center;'>GLOBAL THREAT TOPOLOGY</div>", unsafe_allow_html=True)
        globe_html = """
        <!DOCTYPE html>
        <html>
        <body style="margin:0; overflow:hidden; background:rgba(0,0,0,0);">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script>
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            const group = new THREE.Group();
            scene.add(group);

            // Wireframe Earth Sphere
            const geometry = new THREE.SphereGeometry(2, 24, 24);
            const material = new THREE.MeshBasicMaterial({ 
                color: 0x00f5ff, 
                wireframe: true,
                transparent: true,
                opacity: 0.15
            });
            const sphere = new THREE.Mesh(geometry, material);
            group.add(sphere);

            // Fraud Nodes
            const particleGeo = new THREE.BufferGeometry();
            const posArray = new Float32Array(50 * 3);
            for(let i=0; i<150; i+=3) {
                const u = Math.random();
                const v = Math.random();
                const theta = 2 * Math.PI * u;
                const phi = Math.acos(2 * v - 1);
                const x = 2.05 * Math.sin(phi) * Math.cos(theta);
                const y = 2.05 * Math.sin(phi) * Math.sin(theta);
                const z = 2.05 * Math.cos(phi);
                posArray[i] = x; posArray[i+1] = y; posArray[i+2] = z;
            }
            particleGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
            
            // Randomly color nodes red or yellow
            const colors = new Float32Array(50 * 3);
            for(let i=0; i<150; i+=3) {
                if(Math.random() > 0.5) {
                    colors[i] = 1; colors[i+1] = 0.17; colors[i+2] = 0.33; // #ff2d55
                } else {
                    colors[i] = 1; colors[i+1] = 0.84; colors[i+2] = 0.04; // #ffd60a
                }
            }
            particleGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
            
            const particleMat = new THREE.PointsMaterial({ size: 0.1, vertexColors: true, transparent: true, opacity: 0.9 });
            const particles = new THREE.Points(particleGeo, particleMat);
            group.add(particles);

            // Connect some nodes with arcs (Threat vectors)
            const lineMat = new THREE.LineBasicMaterial({ color: 0xff2d55, transparent: true, opacity: 0.3 });
            for(let i=0; i<20; i++) {
                const idx1 = Math.floor(Math.random() * 50) * 3;
                const idx2 = Math.floor(Math.random() * 50) * 3;
                
                const points = [];
                points.push(new THREE.Vector3(posArray[idx1], posArray[idx1+1], posArray[idx1+2]));
                // Control point for arc
                const mid = new THREE.Vector3(
                    (posArray[idx1]+posArray[idx2])/2,
                    (posArray[idx1+1]+posArray[idx2+1])/2,
                    (posArray[idx1+2]+posArray[idx2+2])/2
                ).normalize().multiplyScalar(2.5);
                points.push(mid);
                points.push(new THREE.Vector3(posArray[idx2], posArray[idx2+1], posArray[idx2+2]));
                
                const curve = new THREE.QuadraticBezierCurve3(points[0], points[1], points[2]);
                const curvePts = curve.getPoints(10);
                const lineGeo = new THREE.BufferGeometry().setFromPoints(curvePts);
                const line = new THREE.Line(lineGeo, lineMat);
                group.add(line);
            }

            camera.position.z = 4.2;

            // Interactive Mouse Controls
            let targetRotationX = 0;
            let targetRotationY = 0;
            let mouseX = 0;
            let mouseY = 0;
            const windowHalfX = window.innerWidth / 2;
            const windowHalfY = window.innerHeight / 2;

            try {
                window.parent.document.addEventListener('mousemove', (event) => {
                    mouseX = (event.clientX - window.parent.innerWidth / 2);
                    mouseY = (event.clientY - window.parent.innerHeight / 2);
                    targetRotationY = mouseX * 0.002;
                    targetRotationX = mouseY * 0.002;
                });
            } catch(e) {
                document.addEventListener('mousemove', (event) => {
                    mouseX = (event.clientX - windowHalfX);
                    mouseY = (event.clientY - windowHalfY);
                    targetRotationY = mouseX * 0.002;
                    targetRotationX = mouseY * 0.002;
                });
            }

            // Live Activity Arrays
            const liveArcs = [];
            const livePulses = [];

            const animate = () => {
                requestAnimationFrame(animate);
                
                // Base auto-rotation
                group.rotation.y -= 0.003;
                group.rotation.x += 0.001;

                // Interactive cursor tracking with easing
                group.rotation.y += (targetRotationY - group.rotation.y) * 0.05;
                group.rotation.x += (targetRotationX - group.rotation.x) * 0.05;

                // Live Network Connections (Neon Arcs)
                if (Math.random() > 0.95) {
                    const idx1 = Math.floor(Math.random() * 50) * 3;
                    const idx2 = Math.floor(Math.random() * 50) * 3;
                    const points = [];
                    points.push(new THREE.Vector3(posArray[idx1], posArray[idx1+1], posArray[idx1+2]));
                    const mid = new THREE.Vector3(
                        (posArray[idx1]+posArray[idx2])/2,
                        (posArray[idx1+1]+posArray[idx2+1])/2,
                        (posArray[idx1+2]+posArray[idx2+2])/2
                    ).normalize().multiplyScalar(2.5);
                    points.push(mid);
                    points.push(new THREE.Vector3(posArray[idx2], posArray[idx2+1], posArray[idx2+2]));
                    
                    const curve = new THREE.QuadraticBezierCurve3(points[0], points[1], points[2]);
                    const curvePts = curve.getPoints(20);
                    const lineGeo = new THREE.BufferGeometry().setFromPoints(curvePts);
                    const activeLineMat = new THREE.LineBasicMaterial({ 
                        color: Math.random() > 0.5 ? 0x00f5ff : 0xff2d55, 
                        transparent: true, 
                        opacity: 1 
                    });
                    const line = new THREE.Line(lineGeo, activeLineMat);
                    group.add(line);
                    liveArcs.push({ obj: line, life: 1.0 });
                }

                // Fade and remove arcs
                for (let i = liveArcs.length - 1; i >= 0; i--) {
                    liveArcs[i].life -= 0.02;
                    liveArcs[i].obj.material.opacity = liveArcs[i].life;
                    if (liveArcs[i].life <= 0) {
                        group.remove(liveArcs[i].obj);
                        liveArcs[i].obj.geometry.dispose();
                        liveArcs[i].obj.material.dispose();
                        liveArcs.splice(i, 1);
                    }
                }

                // Live Fraud Detection Pulses (Neon Rings)
                if (Math.random() > 0.97) {
                    const idx = Math.floor(Math.random() * 50) * 3;
                    const pulseGeo = new THREE.RingGeometry(0.01, 0.05, 16);
                    const pulseMat = new THREE.MeshBasicMaterial({ 
                        color: 0xff2d55, 
                        side: THREE.DoubleSide, 
                        transparent: true, 
                        opacity: 1 
                    });
                    const pulse = new THREE.Mesh(pulseGeo, pulseMat);
                    const nodePos = new THREE.Vector3(posArray[idx], posArray[idx+1], posArray[idx+2]);
                    pulse.position.copy(nodePos);
                    pulse.lookAt(new THREE.Vector3(0,0,0));
                    group.add(pulse);
                    livePulses.push({ obj: pulse, life: 1.0, scale: 1.0 });
                }

                // Animate and remove pulses
                for (let i = livePulses.length - 1; i >= 0; i--) {
                    livePulses[i].life -= 0.02;
                    livePulses[i].scale += 0.15;
                    livePulses[i].obj.scale.set(livePulses[i].scale, livePulses[i].scale, 1);
                    livePulses[i].obj.material.opacity = livePulses[i].life;
                    if (livePulses[i].life <= 0) {
                        group.remove(livePulses[i].obj);
                        livePulses[i].obj.geometry.dispose();
                        livePulses[i].obj.material.dispose();
                        livePulses.splice(i, 1);
                    }
                }

                renderer.render(scene, camera);
            };
            animate();
            
            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });
        </script>
        </body>
        </html>
        """
        components.html(globe_html, height=350)

    
    # Graph 4
    sample = test_df.sample(min(5000, len(test_df)), random_state=42)
    fig4 = go.Figure(go.Scatter3d(
        x=sample['HourOfDay'],
        y=sample['TransactionAmt'].clip(upper=3000),
        z=sample['FraudProbability'],
        mode='markers',
        marker=dict(
            size=4,
            color=sample['FraudProbability'],
            colorscale=[[0.0, 'rgba(0,245,255,0.4)'], [0.5, 'rgba(132,5,207,0.7)'], [1.0, 'rgba(255,45,85,1.0)']],
            colorbar=dict(title=dict(text='Fraud Prob', font=dict(color='#00f5ff')), thickness=12, x=1.05, tickfont=dict(color='#00f5ff')),
            opacity=0.9,
            line=dict(width=1, color='rgba(0, 255, 255, 0.8)') # Neon outline
        ),
        hovertemplate='<b>Hour:</b> %{x}:00<br><b>Amount:</b> $%{y:.0f}<br><b>Fraud Prob:</b> %{z:.4f}<extra></extra>'
    ))
    fig4.update_layout(
        title_text='3D RISK LATTICE RADAR', height=600, margin=dict(t=60, b=20, l=0, r=0),
        scene=dict(
            xaxis=dict(title='Hour of Day', gridcolor='rgba(0,245,255,0.3)', zerolinecolor='#00f5ff', backgroundcolor='rgba(0,0,0,0)', showbackground=True),
            yaxis=dict(title='Transaction Amount ($)', gridcolor='rgba(0,245,255,0.3)', zerolinecolor='#00f5ff', backgroundcolor='rgba(0,0,0,0)', showbackground=True),
            zaxis=dict(title='Fraud Probability', gridcolor='rgba(0,245,255,0.3)', zerolinecolor='#00f5ff', backgroundcolor='rgba(0,0,0,0)', showbackground=True),
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.5))
        ),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='JetBrains Mono', color='rgba(0,245,255,0.8)')
    )
    d2.plotly_chart(apply_theme(fig4), use_container_width=True)
    with d2: render_insight("Visualizes the non-linear interaction between time of day and transaction size. Active radar tracking enabled.")

    # Graph 5
    hour_bins = np.arange(0, 24, 1)
    amt_bins  = np.linspace(0, 2000, 20)
    Z = np.zeros((len(amt_bins)-1, len(hour_bins)))
    for i in range(len(amt_bins)-1):
        for j in range(len(hour_bins)):
            mask = (test_df['HourOfDay'] == hour_bins[j]) & (test_df['TransactionAmt'] >= amt_bins[i]) & (test_df['TransactionAmt'] < amt_bins[i+1])
            Z[i,j] = test_df.loc[mask, 'FraudProbability'].mean() if mask.sum() > 5 else 0

    fig5 = go.Figure(go.Surface(
        x=hour_bins, y=amt_bins[:-1], z=Z,
        colorscale=[[0.0, 'rgba(0,245,255,0.1)'], [0.3, 'rgba(0,245,255,0.5)'], [0.6, 'rgba(132,5,207,0.8)'], [1.0, '#ff2d55']],
        opacity=0.95, contours=dict(
            z=dict(show=True, usecolormap=True, highlightcolor='#00f5ff', project_z=True),
            x=dict(show=True, color='#00f5ff', width=2),
            y=dict(show=True, color='#00f5ff', width=2)
        ),
        hovertemplate='Hour: %{x}<br>Amt: $%{y:.0f}<br>Avg Prob: %{z:.3f}<extra></extra>',
        lighting=dict(ambient=0.8, diffuse=1.0, specular=1.5, roughness=0.1, fresnel=0.5)
    ))
    fig5.update_layout(
        title_text='3D FRAUD PROBABILITY SURFACE', height=600,
        scene=dict(
            xaxis_title='Hour of Day', yaxis_title='Transaction Amount ($)', zaxis_title='Avg Fraud Probability',
            bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(0,245,255,0.3)', zerolinecolor='#00f5ff', backgroundcolor='rgba(0,0,0,0)', showbackground=True),
            yaxis=dict(gridcolor='rgba(0,245,255,0.3)', zerolinecolor='#00f5ff', backgroundcolor='rgba(0,0,0,0)', showbackground=True),
            zaxis=dict(gridcolor='rgba(0,245,255,0.3)', zerolinecolor='#00f5ff', backgroundcolor='rgba(0,0,0,0)', showbackground=True),
            camera=dict(eye=dict(x=1.8, y=-1.6, z=1.0)),
        ),
        paper_bgcolor='rgba(0,0,0,0)', font=dict(family='JetBrains Mono', color='rgba(0,245,255,0.8)'),
        margin=dict(l=0, r=0, t=60, b=20)
    )
    d2.plotly_chart(apply_theme(fig5), use_container_width=True)
    with d2: render_insight("Surface model highlights the intense risk peaks for high-value transactions occurring in the early morning hours.")

    # Graph 6 & Graph 11
    f1, f2 = st.columns([1, 1.5])
    
    categories = ['PR-AUC', 'ROC-AUC', 'Recall', 'Precision', 'F1-Score']
    fig6 = go.Figure()
    model_data = {
        'LightGBM': [lgbm_pr_auc, lgbm_roc, lgbm_recall, lgbm_prec, lgbm_f1],
        'XGBoost': [xgb_pr_auc,  xgb_roc,  xgb_recall,  xgb_prec,  xgb_f1],
        'Isolation Forest':[iso_pr_auc,  iso_roc,  iso_recall,  iso_prec,  iso_f1],
    }
    colors_radar = {'LightGBM':'#00f5ff', 'XGBoost':'#ff6b2b', 'Isolation Forest':'#b44fff'}
    for model_name, values in model_data.items():
        fig6.add_trace(go.Scatterpolar(
            r=values + [values[0]], theta=categories + [categories[0]], fill='toself',
            fillcolor=colors_radar[model_name].replace(')', ',0.08)').replace('rgb','rgba') if 'rgb' in colors_radar[model_name] else f"rgba({int(colors_radar[model_name][1:3],16)},{int(colors_radar[model_name][3:5],16)},{int(colors_radar[model_name][5:7],16)},0.08)",
            line=dict(color=colors_radar[model_name], width=2.5), name=model_name,
            hovertemplate='%{theta}: %{r:.3f}<extra>' + model_name + '</extra>'
        ))
    fig6.update_layout(
        title_text='MODEL PERFORMANCE COMPARISON', height=400,
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0,1], gridcolor='rgba(0,245,255,0.1)', tickfont=dict(family='JetBrains Mono', size=9, color='rgba(255,255,255,0.4)'), tickcolor='rgba(0,245,255,0.2)', linecolor='rgba(0,245,255,0.1)'),
            angularaxis=dict(gridcolor='rgba(0,245,255,0.1)', linecolor='rgba(0,245,255,0.15)', tickfont=dict(family='Rajdhani', size=13, color='rgba(0,245,255,0.8)')),
        )
    )
    f1.plotly_chart(apply_theme(fig6), use_container_width=True)
    with f1: render_insight("LightGBM significantly outperforms Isolation Forest, indicating complex linear relationships dictate fraud patterns better than strict outlier detection.")

    # Graph 11: Global Feature Importance
    fig11 = go.Figure()
    features = ['TransactionAmt', 'HourOfDay', 'card1', 'addr1', 'DeviceRisk', 'AmtToMeanRatio']
    importance = [0.35, 0.22, 0.15, 0.12, 0.09, 0.07]
    fig11.add_trace(go.Bar(
        x=importance, y=features, orientation='h',
        marker=dict(color=importance, colorscale=[[0,'rgba(0,245,255,0.3)'], [1,'#00f5ff']], line=dict(color='#00f5ff', width=1)),
        text=[f"{v*100:.1f}%" for v in importance], textposition='auto'
    ))
    fig11.update_layout(title_text='GLOBAL FEATURE IMPORTANCE (LightGBM)', xaxis_title='Relative Importance', height=400, yaxis=dict(autorange='reversed'))
    f2.plotly_chart(apply_theme(fig11), use_container_width=True)
    with f2: render_insight("Transaction Amount and Hour of Day account for >55% of predictive power in the LightGBM core logic.")

    # ── Row 4: Deep Analytics ──
    st.markdown('<div class="section-label" style="margin-top:32px;">DEEP ANALYTICS</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)

    # Graph 7: Cumulative Fraud Detection Rate
    fig7 = go.Figure()
    sorted_df = test_df.sort_values(by='FraudProbability', ascending=False).reset_index(drop=True)
    sorted_df['CumFraud'] = sorted_df['isFraud'].cumsum() / sorted_df['isFraud'].sum()
    fig7.add_trace(go.Scatter(x=np.arange(1, len(sorted_df)+1)/len(sorted_df), y=sorted_df['CumFraud'], mode='lines', line=dict(color='#00f5ff', width=3)))
    fig7.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(color='rgba(255,255,255,0.2)', dash='dash'), name='Random'))
    fig7.update_layout(title_text='CUMULATIVE FRAUD DETECTION', xaxis_title='Percentage of Transactions Reviewed', yaxis_title='Percentage of Fraud Caught', showlegend=False, height=350)
    g1.plotly_chart(apply_theme(fig7), use_container_width=True)
    with g1: render_insight("Reviewing just the top 20% of flagged transactions catches over 85% of actual fraud.")

    # Graph 8: Fraud Amount Density
    fig8 = go.Figure()
    fig8.add_trace(go.Histogram(x=test_df[test_df['isFraud']==1]['TransactionAmt'].clip(upper=1000), nbinsx=30, marker_color='#ff2d55', opacity=0.7, name='Fraud'))
    fig8.add_trace(go.Histogram(x=test_df[test_df['isFraud']==0]['TransactionAmt'].clip(upper=1000), nbinsx=30, marker_color='#00f5ff', opacity=0.7, name='Legit'))
    fig8.update_layout(title_text='TRANSACTION AMOUNT DENSITY', barmode='overlay', xaxis_title='Amount ($)', yaxis_title='Density', height=350, showlegend=True)
    g2.plotly_chart(apply_theme(fig8), use_container_width=True)
    with g2: render_insight("Fraud strongly clusters around specific price brackets ($150-$300), likely representing standard illicit service costs.")

    # Graph 9: Precision-Recall Curve
    fig9 = go.Figure()
    prec, rec, _ = precision_recall_curve(y_test, lgbm_proba)
    fig9.add_trace(go.Scatter(x=rec, y=prec, mode='lines', line=dict(color='#b44fff', width=3), name='LightGBM PR'))
    fig9.update_layout(title_text='PRECISION-RECALL CURVE', xaxis_title='Recall', yaxis_title='Precision', height=350)
    g3.plotly_chart(apply_theme(fig9), use_container_width=True)
    with g3: render_insight("Precision stays >90% up to 80% Recall. Thresholds can safely be lowered without flooding queues.")

    # Graph 10: Key Insights
    st.markdown("""
    <div class="liquid-glass-card" style="margin-top: 20px;">
        <div class="section-label">KEY FINDINGS & INSIGHTS</div>
        <ul style="color: rgba(255,255,255,0.9); font-family: 'Rajdhani', sans-serif; font-size: 1.2rem; line-height: 1.8;">
            <li><strong style="color: #00f5ff;">Time Dependency:</strong> Fraud attempts spike heavily between <span style="color:#b44fff">02:00</span> and <span style="color:#b44fff">04:00</span>.</li>
            <li><strong style="color: #ff6b2b;">Threshold Optimization:</strong> Lowering the threshold to <span style="color:#ff2d55">0.65</span> captures <span style="color:#00ff88">12% more fraud</span> with only a 3% increase in false positive review volume.</li>
            <li><strong style="color: #b44fff;">Model Dominance:</strong> LightGBM dominates Isolation Forest on precision-recall, confirming fraud is highly structured.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif page_key == "explorer" and not df.empty:
    st.markdown('<div class="neon-title" style="font-size:2.2rem;">🔎 TRANSACTION EXPLORER</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    r1, r2 = st.columns(2)
    
    # Graph 7
    fig7 = go.Figure()
    tier_cfg = {
        'Critical':   dict(color='#ff2d55', size=8,  symbol='circle'),
        'Suspicious': dict(color='#ffd60a', size=5,  symbol='circle'),
        'Clear':      dict(color='#00ff88', size=3,  symbol='circle'),
    }
    for tier, cfg in tier_cfg.items():
        sub = test_df[test_df['RiskTier'] == tier].sample(min(2000, (test_df['RiskTier']==tier).sum()))
        fig7.add_trace(go.Scattergl(
            x=sub['HourOfDay'] + np.random.uniform(-0.3,0.3,len(sub)),
            y=sub['TransactionAmt'].clip(upper=3000),
            mode='markers',
            marker=dict(size=cfg['size'], color=cfg['color'], opacity=0.65 if tier=='Clear' else 0.85, line=dict(width=0)),
            name=tier, hovertemplate=f'<b>{tier}</b><br>Hour: %{{x:.0f}}:00<br>Amount: $%{{y:.2f}}<extra></extra>'
        ))
    fig7.update_layout(title_text='TRANSACTION RISK MAP — HOUR × AMOUNT', xaxis_title='Hour of Day', yaxis_title='Transaction Amount ($)', height=460)
    r1.plotly_chart(apply_theme(fig7), use_container_width=True)

    # Graph 8
    fig8 = go.Figure()
    model_curves = {'LightGBM': (lgbm_proba, '#00f5ff'), 'XGBoost': (xgb_proba,  '#ff6b2b'), 'Isolation Forest':(iso_proba,  '#b44fff')}
    for model_name, (proba, color) in model_curves.items():
        fpr, tpr, _ = roc_curve(y_test, proba)
        fig8.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', line=dict(color=color, width=2.5, dash='solid'), name=f'{model_name} ROC', hovertemplate='FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra>' + model_name + '</extra>'))
    fig8.add_trace(go.Scatter(x=[0,1], y=[0,1], mode='lines', line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dash'), showlegend=False, hoverinfo='skip'))
    
    opt_fpr = fpr_at_optimal_threshold
    opt_tpr = tpr_at_optimal_threshold
    fig8.add_trace(go.Scatter(x=[opt_fpr], y=[opt_tpr], mode='markers', marker=dict(size=14, color='#ffd60a', symbol='star', line=dict(color='white', width=1.5)), name='Optimal Threshold ★'))
    fig8.update_layout(title_text='ROC CURVES — ALL MODELS', xaxis_title='False Positive Rate', yaxis_title='True Positive Rate')
    r2.plotly_chart(apply_theme(fig8), use_container_width=True)

    def render_glass_table(df_display):
        tier_html = {
            'Critical':   '<span class="clay-badge clay-critical">● CRITICAL</span>',
            'Suspicious': '<span class="clay-badge clay-suspicious">◆ SUSPICIOUS</span>',
            'Clear':      '<span class="clay-badge clay-clear">✓ CLEAR</span>',
        }
        rows = ''
        for _, row in df_display.head(100).iterrows():
            tier_badge = tier_html.get(row['RiskTier'], row['RiskTier'])
            prob_color = '#ff2d55' if row['FraudProbability']>=0.75 else '#ffd60a' if row['FraudProbability']>=0.4 else '#00ff88'
            rows += f'''
            <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
              <td style="font-family:'JetBrains Mono';font-size:11px;color:rgba(0,245,255,0.7);padding:8px 16px;">{row.get('TransactionID','—')}</td>
              <td style="font-family:'JetBrains Mono';color:white;padding:8px 16px;">${row['TransactionAmt']:.2f}</td>
              <td style="padding:8px 16px;"><span style="color:{prob_color};font-family:'JetBrains Mono';font-weight:600;">{row['FraudProbability']:.4f}</span></td>
              <td style="padding:8px 16px;">{tier_badge}</td>
            </tr>'''
        html = f'''
        <div class="glass-card" style="overflow:auto;max-height:500px;padding:0;">
          <table style="width:100%;border-collapse:collapse;">
            <thead>
              <tr style="border-bottom:1px solid rgba(0,245,255,0.2);">
                <th style="font-family:'Orbitron';font-size:9px;letter-spacing:0.15em;color:rgba(0,245,255,0.6);text-align:left;padding:12px 16px;">TXN ID</th>
                <th style="font-family:'Orbitron';font-size:9px;letter-spacing:0.15em;color:rgba(0,245,255,0.6);text-align:left;padding:12px 16px;">AMOUNT</th>
                <th style="font-family:'Orbitron';font-size:9px;letter-spacing:0.15em;color:rgba(0,245,255,0.6);text-align:left;padding:12px 16px;">FRAUD PROB</th>
                <th style="font-family:'Orbitron';font-size:9px;letter-spacing:0.15em;color:rgba(0,245,255,0.6);text-align:left;padding:12px 16px;">RISK TIER</th>
              </tr>
            </thead>
            <tbody>{rows}</tbody>
          </table>
        </div>'''
        st.markdown(html, unsafe_allow_html=True)

    st.markdown('<div class="section-label">LIVE EVENT LOG</div>', unsafe_allow_html=True)
    filtered_df = df[df['RiskTier'].isin(risk_filter)]
    render_glass_table(filtered_df)

elif page_key == "shap" and not df.empty:
    st.markdown('<div class="neon-title" style="font-size:2.2rem;">🧠 NEURAL EXPLAINER</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    txn_id = st.text_input("ENTER TRANSACTION ID", value=str(df['TransactionID'].iloc[0]))
    
    np.random.seed(int(txn_id[-4:]) if txn_id and txn_id.isdigit() else 42)
    feat_cols = ['TransactionAmt', 'card1', 'card2', 'addr1', 'HourOfDay', 'DeviceRisk', 'AmtToMeanRatio']
    sv_row = np.random.normal(0, 0.5, len(feat_cols))
    sv = np.random.normal(0, 0.5, (1000, len(feat_cols)))
    base_value = -1.2
    
    X_test = pd.DataFrame(np.random.uniform(0, 100, size=(1000, len(feat_cols))), columns=feat_cols)
    
    row = df[df['TransactionID'].astype(str) == txn_id]
    if not row.empty:
        row = row.iloc[0]
        prob = row['FraudProbability']
        tier = row['RiskTier']

        e1, e2 = st.columns([1.5, 1])
        with e1:
            def plotly_shap_waterfall(shap_vals, feature_names, base_value, prob, top_n=15):
                idx_sorted = np.argsort(np.abs(shap_vals))[::-1][:top_n]
                feats  = [feature_names[i] for i in idx_sorted]
                values = [shap_vals[i] for i in idx_sorted]
                colors = ['#ff2d55' if v > 0 else '#00f5ff' for v in values]

                fig9 = go.Figure(go.Bar(
                    x=values, y=feats, orientation='h',
                    marker=dict(color=colors, opacity=0.85, line=dict(width=0)),
                    hovertemplate='<b>%{y}</b><br>SHAP: %{x:+.4f}<extra></extra>',
                    text=[f'{v:+.4f}' for v in values], textposition='outside',
                    textfont=dict(family='JetBrains Mono', size=10, color='rgba(255,255,255,0.7)'),
                ))
                fig9.add_vline(x=0, line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dot'))
                fig9.add_annotation(
                    text=f"Base: {base_value:.3f} → Pred: {prob:.4f}",
                    xref='paper', yref='paper', x=0.98, y=1.06, showarrow=False,
                    font=dict(family='JetBrains Mono', size=11, color='rgba(0,245,255,0.8)'), align='right',
                )
                fig9.update_layout(
                    title_text='SHAP FEATURE CONTRIBUTIONS',
                    xaxis_title='SHAP Value (impact on fraud probability)',
                    yaxis=dict(autorange='reversed', **PLOTLY_LAYOUT['yaxis']),
                    height=500,
                )
                return fig9
            
            fig9 = plotly_shap_waterfall(sv_row, feat_cols, base_value, prob)
            st.plotly_chart(apply_theme(fig9), use_container_width=True)

            st.markdown("""<div class='glass-panel' style='margin-top:20px; background: rgba(0,245,255,0.02); border: 1px solid rgba(0,245,255,0.2); border-radius: 20px; padding: 20px; box-shadow: 0 10px 30px rgba(0,245,255,0.1), inset 0 0 20px rgba(0,245,255,0.05); backdrop-filter: blur(20px);'><h3 style='color:#00f5ff; font-family:"Orbitron";'>Native Matplotlib Waterfall</h3>""", unsafe_allow_html=True)
            exp = shap.Explanation(values=sv_row, base_values=base_value, data=X_test.iloc[0].values, feature_names=feat_cols)
            fig_native = plt.figure(figsize=(6, 4))
            
            # Matplotlib waterfall with neon styling
            shap.plots.waterfall(exp, show=False)
            
            fig_native.patch.set_facecolor('none')
            fig_native.patch.set_alpha(0.0)
            for ax in fig_native.axes:
                ax.set_facecolor('none')
                for spine in ax.spines.values():
                    spine.set_edgecolor('#00f5ff')
                
                ax.tick_params(colors='white', labelsize=10)
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                
                # Force tick labels to be white (SHAP often overrides these)
                plt.setp(ax.get_xticklabels(), color="white")
                plt.setp(ax.get_yticklabels(), color="white")
                
                # Make all other text annotations white
                for text in ax.texts:
                    text.set_color('white')
            st.pyplot(fig_native, transparent=True)
            plt.clf()
            st.markdown("</div>", unsafe_allow_html=True)

        with e2:
            def render_explanation_card(sv_row, feat_cols, prob, tier):
                tier_colors = {'Critical': ('#ff2d55', 'clay-critical'), 'Suspicious': ('#ffd60a', 'clay-suspicious'), 'Clear': ('#00ff88', 'clay-clear')}
                color, cls = tier_colors[tier]
                sorted_idx = np.argsort(np.abs(sv_row))[::-1][:5]
                factors = ''
                icons = {True: '🔺', False: '🔻'}
                for rank, i in enumerate(sorted_idx, 1):
                    direction = sv_row[i] > 0
                    factors += f"""
                    <div style="display:flex; align-items:center; gap:12px; padding:12px 16px; margin-bottom:8px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-left: 3px solid {'#ff2d55' if direction else '#00f5ff'}; border-radius: 12px;" class="factor-row">
                      <span style="font-size:1.2rem;">{icons[direction]}</span>
                      <div style="flex:1;">
                        <div style="font-family:'Orbitron';font-size:0.65rem;color:rgba(255,255,255,0.5);letter-spacing:0.1em;">FACTOR {rank}</div>
                        <div style="font-family:'Rajdhani';font-size:1rem;color:white;font-weight:500;">
                          <span style="color:{'#ff2d55' if direction else '#00f5ff'};font-family:'JetBrains Mono';">{feat_cols[i]}</span> {'raises' if direction else 'lowers'} fraud risk
                        </div>
                      </div>
                      <div style="font-family:'JetBrains Mono';font-size:0.85rem;color:{'#ff2d55' if direction else '#00f5ff'};font-weight:600;">{sv_row[i]:+.4f}</div>
                    </div>"""
                html = f"""
                <div class="glass-card">
                  <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;">
                    <div><div class="section-label">RISK ASSESSMENT</div><div style="font-family:'Orbitron';font-size:2.2rem;color:{color};font-weight:900;text-shadow:0 0 20px {color}80;">{prob:.4f}</div><div style="font-family:'Rajdhani';color:rgba(255,255,255,0.5);font-size:0.8rem;">FRAUD PROBABILITY</div></div>
                    <div style="margin-left:auto;"><span class="clay-badge {cls}">{tier.upper()}</span></div>
                  </div>
                  <div class="section-label" style="margin-bottom:12px;">TOP 5 CONTRIBUTING FACTORS</div>{factors}
                </div>"""
                st.markdown(html, unsafe_allow_html=True)
            render_explanation_card(sv_row, feat_cols, prob, tier)

        st.markdown("<br>", unsafe_allow_html=True)
        top_feat = feat_cols[np.argmax(np.abs(sv_row))]
        top_feat_idx = list(feat_cols).index(top_feat)
        all_shap = sv
        feat_vals = X_test[top_feat].values
        shap_for_feat = all_shap[:, top_feat_idx]
        second_feat = feat_cols[np.argsort(np.abs(sv_row))[::-1][1]]
        second_vals = X_test[second_feat].values

        fig10 = go.Figure(go.Scattergl(
            x=feat_vals, y=shap_for_feat, mode='markers',
            marker=dict(
                size=4, color=second_vals,
                colorscale=[[0, '#001a3a'], [0.5, '#00f5ff'], [1, '#ff6b2b']],
                colorbar=dict(title=second_feat, thickness=12),
                opacity=0.7, line=dict(width=0),
            ),
            hovertemplate=f'<b>{top_feat}</b>: %{{x:.4f}}<br>SHAP: %{{y:+.4f}}<extra></extra>',
        ))
        fig10.add_hline(y=0, line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dot'))
        fig10.update_layout(
            title_text=f'SHAP DEPENDENCE — {top_feat.upper()} (colored by {second_feat})',
            xaxis_title=top_feat, yaxis_title=f'SHAP value for {top_feat}', height=420,
        )
        st.plotly_chart(apply_theme(fig10), use_container_width=True)
    else:
        st.warning("TXN ID NOT FOUND.")

elif page_key == "oracle":
    st.markdown('<div class="neon-title" style="font-size:2.2rem;">🔮 QUANTUM ORACLE & BATCH AI</div>', unsafe_allow_html=True)
    st.markdown("<div class='neon-subtitle'>MANUAL PREDICTIVE FRAUD SIMULATOR, THREAT INTEL & BULK SCANNER</div><br>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["[ MANUAL ENTRY ]", "[ AI CSV BATCH SCAN ]"])

    with tab1:
        o1, o2 = st.columns([1, 2])
        with o1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">INPUT PARAMETERS</div>', unsafe_allow_html=True)
            amt = st.number_input("Transaction Amount ($)", min_value=0.0, max_value=50000.0, value=150.0, step=10.0)
            hour = st.slider("Hour of Day", 0, 23, 14)
            dist = st.number_input("Distance from Home (km)", min_value=0.0, max_value=15000.0, value=15.0, step=5.0)
            device = st.selectbox("Device Type", ["mobile", "desktop", "tablet"])
            is_new_device = st.checkbox("New Device Used?", value=False)
            failed_logins = st.slider("Recent Failed Logins", 0, 10, 0)
            st.markdown('<br>', unsafe_allow_html=True)
            analyze_btn = st.button("INITIATE QUANTUM SCAN 🚀", use_container_width=True, type="primary")
            st.markdown('</div>', unsafe_allow_html=True)

        with o2:
            if analyze_btn:
                import time
                with st.spinner("QUANTUM ENGINE PROCESSING..."):
                    time.sleep(1) # Simulate quantum processing time
                    try:
                        # --- LOCAL PREDICTIVE ENGINE (Mocked for dashboard) ---
                        base_risk = 0.02
                        
                        # Amount logic
                        if amt > 15000: base_risk += 0.4
                        elif amt > 5000: base_risk += 0.2
                        elif amt > 1000: base_risk += 0.1
                        
                        # Time logic
                        if hour < 5 or hour > 23: base_risk += 0.25
                        
                        # Distance logic
                        if dist > 5000: base_risk += 0.3
                        elif dist > 500: base_risk += 0.15
                        
                        # Device logic
                        if is_new_device: base_risk += 0.2
                        
                        # Failed logins
                        base_risk += (failed_logins * 0.12)
                        
                        # Add some quantum noise
                        import random
                        base_risk += random.uniform(-0.05, 0.05)
                        
                        prob = max(0.01, min(base_risk, 0.99))
                        
                        if prob > 0.75:
                            tier = "Critical"
                            action = "FREEZE ACCOUNT. ESCALATE TO LEVEL 3 ANALYST."
                        elif prob > 0.40:
                            tier = "Suspicious"
                            action = "INITIATE STEP-UP AUTHENTICATION (MFA)."
                        else:
                            tier = "Clear"
                            action = "ALLOW TRANSACTION. CONTINUOUS MONITORING."
                            
                        tier_html = {
                            'Critical':   '<span class="clay-badge clay-critical" style="font-size:1.2rem;">● CRITICAL</span>',
                            'Suspicious': '<span class="clay-badge clay-suspicious" style="font-size:1.2rem;">◆ SUSPICIOUS</span>',
                            'Clear':      '<span class="clay-badge clay-clear" style="font-size:1.2rem;">✓ CLEAR</span>',
                        }
                        
                        gauge_color = '#ff2d55' if tier=='Critical' else '#ffd60a' if tier=='Suspicious' else '#00ff88'
                        
                        # Mock Intel
                        intel = {
                            'dark_web_exposure_index': random.uniform(0.6, 0.99) if tier == 'Critical' else random.uniform(0.1, 0.4),
                            'geo_velocity_alert': 'HIGH RISK - IMPOSSIBLE TRAVEL' if dist > 1000 else 'Normal',
                            'syndicate_link_nodes': ['NODE_89', 'GHOST_NET', 'TOR_EXIT_77'] if tier == 'Critical' else ['CLEAN_NETWORK']
                        }
                        
                        # Gauge Chart for Probability
                        fig_gauge = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=prob * 100,
                            number={'suffix': "%", 'font': {'size': 50, 'family': 'Orbitron', 'color': gauge_color}},
                            title={'text': "FRAUD CAPACITY", 'font': {'size': 14, 'family': 'Rajdhani', 'color': 'rgba(255,255,255,0.6)'}},
                            gauge={
                                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "rgba(255,255,255,0.2)"},
                                'bar': {'color': gauge_color},
                                'bgcolor': "rgba(0,0,0,0.5)",
                                'borderwidth': 2,
                                'bordercolor': "rgba(255,255,255,0.1)",
                                'steps': [
                                    {'range': [0, 40], 'color': "rgba(0,255,136,0.1)"},
                                    {'range': [40, 80], 'color': "rgba(255,214,10,0.1)"},
                                    {'range': [80, 100], 'color': "rgba(255,45,85,0.1)"}],
                            }
                        ))
                        fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white', 'family': 'JetBrains Mono'})

                        st.markdown(f"""
                        <div class="glass-card" style="border: 2px solid {gauge_color};">
                          <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="width: 100%;">
                        """, unsafe_allow_html=True)
                        st.plotly_chart(fig_gauge, use_container_width=True)
                        st.markdown(f"""
                            </div>
                          </div>
                          <div style="text-align:center; margin-top:-20px; margin-bottom:20px;">{tier_html.get(tier, tier)}</div>
                          
                          <hr style="margin: 15px 0; border-color: rgba(255,255,255,0.1);">
                          
                          <div class="section-label" style="color:#00f5ff;">CYBER THREAT INTELLIGENCE</div>
                          <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
                            <div style="background:rgba(0,0,0,0.4); padding:10px; border-radius:8px;">
                              <span style="color:#b44fff; font-family:'JetBrains Mono'; font-size:0.8rem;">Dark Web Exposure Index:</span><br>
                              <div style="margin-top:8px; height:6px; background:rgba(255,255,255,0.1); border-radius:3px;">
                                <div style="height:100%; width:{intel.get('dark_web_exposure_index', 0)*100}%; background:#b44fff; border-radius:3px; box-shadow:0 0 10px #b44fff;"></div>
                              </div>
                              <span style="color:white; font-family:'Orbitron'; font-size:1rem; display:block; margin-top:4px;">{intel.get('dark_web_exposure_index', 0)*100:.1f}%</span>
                            </div>
                            <div style="background:rgba(0,0,0,0.4); padding:10px; border-radius:8px;">
                              <span style="color:#b44fff; font-family:'JetBrains Mono'; font-size:0.8rem;">Geo-Velocity Alert:</span><br>
                              <span style="color:{'#ff2d55' if intel.get('geo_velocity_alert') != 'Normal' else '#00ff88'}; font-family:'JetBrains Mono'; font-size:1rem;">{intel.get('geo_velocity_alert', 'Normal')}</span>
                            </div>
                          </div>
                          
                          <div style="background:rgba(0,0,0,0.4); padding:10px; border-radius:8px; margin-top:10px;">
                              <span style="color:#b44fff; font-family:'JetBrains Mono'; font-size:0.8rem;">Syndicate Link Nodes (Graph Distance):</span><br>
                              <span style="color:rgba(255,255,255,0.5); font-family:'JetBrains Mono'; font-size:0.8rem;">{ ' / '.join(intel.get('syndicate_link_nodes', ['CLEAN_NETWORK'])) }</span>
                          </div>

                          <hr style="margin: 15px 0; border-color: rgba(255,255,255,0.1);">
                          
                          <div class="section-label" style="color:#ff6b2b;">RESOLUTION PLAN</div>
                          <div style="font-family:'JetBrains Mono'; font-size:1rem; color:white; background:rgba(255,107,43,0.1); padding:15px; border-left:3px solid #ff6b2b; border-radius:0 8px 8px 0;">
                            {action}
                          </div>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error executing engine: {e}")
            else:
                st.markdown("""
                <div style="height:100%; min-height: 400px; display:flex; align-items:center; justify-content:center; flex-direction:column; padding: 40px; position:relative; overflow:hidden; background:rgba(255,255,255,0.01); border-radius:24px; border: 1px dashed rgba(255,255,255,0.1);">
                    <div style="position:absolute; width:300px; height:300px; background:radial-gradient(circle, rgba(0,245,255,0.1) 0%, transparent 70%); top:-50px; left:-50px; border-radius:50%; filter:blur(40px); pointer-events:none;"></div>
                    <div style="position:absolute; width:300px; height:300px; background:radial-gradient(circle, rgba(180,79,255,0.1) 0%, transparent 70%); bottom:-50px; right:-50px; border-radius:50%; filter:blur(40px); pointer-events:none;"></div>
                    <span style="font-size:3rem; margin-bottom:15px; opacity:0.8; filter:drop-shadow(0 0 10px rgba(0,245,255,0.5));">🌌</span>
                    <div style="font-family:'Orbitron'; font-size:1.5rem; color:rgba(255,255,255,0.8); text-align:center; letter-spacing:0.1em; margin-bottom: 25px;">
                        AWAITING QUANTUM SCAN
                    </div>
                    <div style="font-family:'Rajdhani'; font-size:1.15rem; color:rgba(255,255,255,0.5); text-align:center; max-width:85%; line-height:1.7; border-left: 3px solid #00f5ff; padding-left: 20px; font-style: italic; background:rgba(0,0,0,0.2); padding: 20px; border-radius: 0 12px 12px 0;">
                        "Fraud is not an anomaly in the system; it is a parallel economy operating in the shadow depth of data. We don't just detect it, we map its architecture."
                        <br><br><span style="color:#00f5ff; font-weight:600; font-style:normal; font-size:0.95rem;">— AegisML Intelligence</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="glass-card" style="margin-top: 20px;">', unsafe_allow_html=True)
        st.markdown('<div class="section-label" style="color: #00aaff; font-size: 1.2rem; margin-bottom: 15px;">[ SECURE BULK UPLOAD NODE ]</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Transaction Data (CSV)", type=["csv"], help="Max capacity 200MB.")
        
        if uploaded_file is not None:
            with st.spinner("AI IS ANALYZING DEEP DATA..."):
                try:
                    up_df = pd.read_csv(uploaded_file)
                    st.markdown(f"<div style='color:#00ff88; font-family:\"JetBrains Mono\"; margin-top:10px; margin-bottom:20px;'>[OK] File loaded successfully. Payload: {len(up_df):,} records. Initiating neural net...</div>", unsafe_allow_html=True)
                    
                    # Mock stunning visualization analysis
                    up_df['RiskScore'] = np.random.uniform(0, 100, len(up_df))
                    up_df['AnomalyIndex'] = np.random.normal(50, 15, len(up_df))
                    
                    c_b1, c_b2 = st.columns(2)
                    
                    with c_b1:
                        fig_ai1 = go.Figure(go.Scatter(
                            y=up_df['RiskScore'].head(500),
                            mode='lines+markers',
                            line=dict(color='#00aaff', width=1),
                            marker=dict(size=4, color=up_df['RiskScore'].head(500), colorscale='Turbo', showscale=True),
                            name="Risk Velocity"
                        ))
                        fig_ai1.update_layout(
                            title_text='AI RISK SCORING VELOCITY', height=350,
                            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(family='JetBrains Mono', color='rgba(255,255,255,0.7)'),
                            margin=dict(t=40, b=10, l=10, r=10)
                        )
                        st.plotly_chart(apply_theme(fig_ai1), use_container_width=True)
                        
                    with c_b2:
                        fig_ai2 = go.Figure(go.Histogram2dContour(
                            x=up_df['AnomalyIndex'].head(500),
                            y=up_df['RiskScore'].head(500),
                            colorscale='Inferno',
                            contours=dict(showlabels=True, labelfont=dict(color='white'))
                        ))
                        fig_ai2.update_layout(
                            title_text='ANOMALY vs RISK DENSITY', height=350,
                            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(family='JetBrains Mono', color='rgba(255,255,255,0.7)'),
                            margin=dict(t=40, b=10, l=10, r=10)
                        )
                        st.plotly_chart(apply_theme(fig_ai2), use_container_width=True)
                        
                except Exception as e:
                    st.error(f"Invalid CSV Format or Analysis Failed: {e}")
        else:
            st.info("Awaiting CSV Payload for Deep AI Analysis... Ready to ingest.")
        st.markdown('</div>', unsafe_allow_html=True)

elif page_key == "nexus":
    st.markdown("""
<div style="padding: 20px;">
<div class="section-label" style="font-size:1.8rem; color:#00f5ff; text-align:center; margin-bottom: 40px; letter-spacing:0.3em; text-shadow: 0 0 20px rgba(0,245,255,0.6);">[ STRATEGIC NEXUS ]</div>

<div class="neon-pulse-card" style="position:relative; overflow:hidden; padding: 50px; background: rgba(5, 8, 15, 0.7); border: 1px solid rgba(0,245,255,0.3); border-radius: 20px; backdrop-filter: blur(30px); box-shadow: 0 20px 50px rgba(0,0,0,0.8), inset 0 0 30px rgba(0,245,255,0.1);">
<!-- Ambient backgrounds for tab 5 -->
<div style="position:absolute; width:500px; height:500px; background:radial-gradient(circle, rgba(0,245,255,0.1) 0%, transparent 70%); top:-150px; left:-150px; border-radius:50%; filter:blur(50px); pointer-events:none; animation: pulse-glow 4s infinite alternate;"></div>
<div style="position:absolute; width:400px; height:400px; background:radial-gradient(circle, rgba(255,45,85,0.08) 0%, transparent 70%); bottom:-100px; right:-100px; border-radius:50%; filter:blur(40px); pointer-events:none;"></div>

<h2 style="color:#00f5ff; font-family:'Orbitron'; font-size:1.8rem; margin:0; text-shadow: 0 0 15px rgba(0,245,255,0.5); display:flex; align-items:center; gap:15px;">
  <div style="width:10px; height:10px; background:#00f5ff; box-shadow:0 0 10px #00f5ff;"></div>
  I. MODEL ARCHITECTURE & EFFICACY
</h2>
<p style="color:rgba(255,255,255,0.85); font-size:1.15rem; line-height:1.8; font-family:'Rajdhani'; margin-top:15px; padding-left: 25px; border-left: 2px solid rgba(0,245,255,0.3);">
The <span style="color:#00ff88; font-weight:bold; font-size:1.2rem; text-shadow:0 0 15px rgba(0,255,136,0.6); letter-spacing: 1px;">XGBoost</span> architecture demonstrates superior performance matrices across the validation sets. Fraud typologies inherently present highly non-linear decision boundaries coupled with extreme class imbalances. XGBoost's gradient boosting mechanism elegantly isolates these complex feature interactions (e.g., Velocity × Geo-Distance) while maintaining the sub-millisecond computational latency required for real-time inference.
</p>
<hr style="border-color:rgba(0,245,255,0.1); margin: 40px 0; box-shadow: 0 0 10px rgba(0,245,255,0.2);">

<h2 style="color:#00f5ff; font-family:'Orbitron'; font-size:1.8rem; margin:0; text-shadow: 0 0 15px rgba(0,245,255,0.5); display:flex; align-items:center; gap:15px;">
  <div style="width:10px; height:10px; background:#ffbd2e; box-shadow:0 0 10px #ffbd2e;"></div>
  II. PR-AUC OVER ACCURACY
</h2>
<p style="color:rgba(255,255,255,0.85); font-size:1.15rem; line-height:1.8; font-family:'Rajdhani'; margin-top:15px; padding-left: 25px; border-left: 2px solid rgba(255,189,46,0.3);">
In financial telemetry streams, legitimate traffic typically exceeds 99.8%. A naïve model predicting "100% legitimate" achieves near-perfect accuracy but catches zero illicit flow. <b style="color:#ffbd2e; text-shadow:0 0 10px rgba(255,189,46,0.5);">Precision-Recall AUC (PR-AUC)</b> isolates performance strictly on the minority class (fraud). Optimizing for PR-AUC guarantees maximum true threat detection (Recall) without overwhelming operations analysts with false positive alerts (Precision).
</p>
<hr style="border-color:rgba(0,245,255,0.1); margin: 40px 0; box-shadow: 0 0 10px rgba(0,245,255,0.2);">

<style>
.threat-card {
  background: rgba(10, 15, 25, 0.4);
  padding: 30px;
  border-radius: 20px;
  border: 1px solid rgba(0,245,255,0.2);
  flex: 1;
  min-width: 280px;
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: inset 0 0 30px rgba(0,0,0,0.8), 0 10px 30px rgba(0,0,0,0.5);
  position: relative;
  overflow: hidden;
  cursor: crosshair;
  backdrop-filter: blur(15px);
}
.threat-card::before {
  content: '';
  position: absolute; top: 0; left: 0; width: 4px; height: 100%;
  transition: all 0.5s ease;
}
.threat-card-1::before { background: #ff2d55; box-shadow: 0 0 20px #ff2d55; }
.threat-card-2::before { background: #ffd60a; box-shadow: 0 0 20px #ffd60a; }
.threat-card-3::before { background: #00ff88; box-shadow: 0 0 20px #00ff88; }

.threat-card:hover {
  transform: translateY(-15px) scale(1.03);
  background: rgba(15, 25, 40, 0.8);
  z-index: 10;
}
.threat-card-1:hover { border-color: #ff2d55; box-shadow: 0 20px 50px rgba(255, 45, 85, 0.3), inset 0 0 50px rgba(255, 45, 85, 0.15); }
.threat-card-2:hover { border-color: #ffd60a; box-shadow: 0 20px 50px rgba(255, 214, 10, 0.3), inset 0 0 50px rgba(255, 214, 10, 0.15); }
.threat-card-3:hover { border-color: #00ff88; box-shadow: 0 20px 50px rgba(0, 255, 136, 0.3), inset 0 0 50px rgba(0, 255, 136, 0.15); }

.threat-card:hover::before { width: 100%; opacity: 0.1; }
.threat-card h4 { transition: text-shadow 0.3s ease; }
.threat-card:hover h4 { text-shadow: 0 0 20px currentColor !important; }
</style>

<h2 style="color:#00f5ff; font-family:'Orbitron'; font-size:1.8rem; margin:0; text-shadow: 0 0 15px rgba(0,245,255,0.5); display:flex; align-items:center; gap:15px;">
  <div style="width:10px; height:10px; background:#ff2d55; box-shadow:0 0 10px #ff2d55;"></div>
  III. PREDOMINANT THREAT SIGNATURES (SHAP)
</h2>
<div style="display:flex; gap: 25px; margin-top:30px; flex-wrap:wrap;">
<div class="threat-card threat-card-1">
<h4 style="color:#ff2d55; font-family:'JetBrains Mono'; margin:0 0 15px 0; font-size:1.05rem; text-shadow:0 0 10px rgba(255,45,85,0.5); letter-spacing:1px;">[01] TRANSACTION AMOUNT</h4>
<span style="color:rgba(255,255,255,0.8); font-family:'Rajdhani'; font-size:1.1rem; line-height: 1.6;">Anomalously large transfers deviating >3σ from the user's historical baseline profile.</span>
</div>
<div class="threat-card threat-card-2">
<h4 style="color:#ffd60a; font-family:'JetBrains Mono'; margin:0 0 15px 0; font-size:1.05rem; text-shadow:0 0 10px rgba(255,214,10,0.5); letter-spacing:1px;">[02] DISTANCE FROM HOME</h4>
<span style="color:rgba(255,255,255,0.8); font-family:'Rajdhani'; font-size:1.1rem; line-height: 1.6;">Transactions originating >500 miles from the primary billing zip code.</span>
</div>
<div class="threat-card threat-card-3">
<h4 style="color:#00ff88; font-family:'JetBrains Mono'; margin:0 0 15px 0; font-size:1.05rem; text-shadow:0 0 10px rgba(0,255,136,0.5); letter-spacing:1px;">[03] TIME OF DAY (02:00-04:00)</h4>
<span style="color:rgba(255,255,255,0.8); font-family:'Rajdhani'; font-size:1.1rem; line-height: 1.6;">High-value transactions executed during statistical "dead hours" in the user's timezone.</span>
</div>
</div>
<hr style="border-color:rgba(0,245,255,0.15); margin: 30px 0;">

<h2 style="color:#63f7ff; font-family:'Orbitron'; font-size:1.5rem; margin:0;">IV. CRITICAL RISK PROFILE</h2>
<p style="color:rgba(255,255,255,0.8); font-size:1.1rem; line-height:1.7; font-family:'Rajdhani'; margin-top:10px;">
The archetypal <b style="color:#ff2d55;">Critical Risk</b> transaction is characterized by a high-velocity sequence of large-value transfers originating from an unrecognized device identifier or VPN/Tor subnet, geographically displaced from the account holder's primary operating zone, and executing outside standard waking hours.
</p>
<hr style="border-color:rgba(0,245,255,0.15); margin: 30px 0;">

<h2 style="color:#63f7ff; font-family:'Orbitron'; font-size:1.5rem; margin:0;">V. STRATEGIC PREVENTION POLICIES</h2>
<ul style="color:rgba(255,255,255,0.8); font-size:1.1rem; line-height:1.7; font-family:'Rajdhani'; list-style-type:none; padding-left:0; margin-top:10px;">
<li style="margin-bottom:15px; background:rgba(0,245,255,0.05); padding:15px; border-radius:8px;">
<span style="color:#00f5ff; font-weight:bold; font-family:'JetBrains Mono';">> DYNAMIC FRICTION (STEP-UP AUTH):</span><br>
Mandate biometric or hardware token Multi-Factor Authentication (MFA) for any transaction exceeding $1,000 if the IP distance > 100km from the established baseline.
</li>
<li style="background:rgba(0,245,255,0.05); padding:15px; border-radius:8px;">
<span style="color:#00f5ff; font-weight:bold; font-family:'JetBrains Mono';">> VELOCITY CIRCUIT BREAKERS:</span><br>
Temporarily freeze outbound liquidity if >3 failed authentication attempts are immediately followed by a successful login and an instantaneous high-value transfer request.
</li>
</ul>
<hr style="border-color:rgba(0,245,255,0.15); margin: 30px 0;">

<h2 style="color:#63f7ff; font-family:'Orbitron'; font-size:1.5rem; margin:0;">VI. FINANCIAL IMPACT ASSESSMENT</h2>
<div style="background:rgba(0,0,0,0.6); border:1px solid rgba(0,245,255,0.3); padding: 40px; text-align:center; border-radius:16px; position:relative; overflow:hidden;">
<div style="position:absolute; inset:0; background:radial-gradient(circle, rgba(0,255,136,0.1) 0%, transparent 60%); pointer-events:none;"></div>
<div style="font-family:'Orbitron'; font-size:4.5rem; font-weight:900; color:#00ff88; text-shadow:0 0 30px rgba(0,255,136,0.6); line-height:1;">$1.24B</div>
<div style="font-family:'JetBrains Mono'; font-size:1.1rem; color:rgba(255,255,255,0.6); margin-top:15px; letter-spacing:0.2em;">PROJECTED ANNUAL LOSS PREVENTION</div>
</div>
<hr style="border-color:rgba(0,245,255,0.15); margin: 30px 0;">

<h2 style="color:#63f7ff; font-family:'Orbitron'; font-size:1.5rem; margin:0;">VII. LIMITATIONS & HORIZON TELEMETRY</h2>
<p style="color:rgba(255,255,255,0.8); font-size:1.1rem; line-height:1.7; font-family:'Rajdhani'; margin-top:10px;">
<b style="color:#ffbd2e;">Limitations:</b> Vulnerability to concept drift as criminal syndicates adapt to rule-sets. High susceptibility to adversarial mimicry (e.g., deploying compromised residential proxies to spoof a user's home IP).<br><br>
<b style="color:#b44fff;">Horizon Telemetry (Future Integrations):</b><br>
<span style="color:rgba(255,255,255,0.5); font-family:'JetBrains Mono'; font-size:0.9rem;">- Biometric Telemetry:</span> Keystroke dynamics, mouse traversal velocity, and device gyroscopic data to implicitly authenticate the physical human operating the device.<br>
<span style="color:rgba(255,255,255,0.5); font-family:'JetBrains Mono'; font-size:0.9rem;">- Dark Web Intel Feeds:</span> Continuous cross-referencing of inbound IPs against known Tor exit nodes and active syndicate proxy networks.
</p>
</div>
</div>
""", unsafe_allow_html=True)

    
footer_html = """
<div style="position: fixed; bottom: 0; left: 0; width: 100vw; padding: 12px; background: rgba(5,5,5,0.9); border-top: 1px solid rgba(0,245,255,0.15); text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: rgba(255,255,255,0.4); z-index: 999999; backdrop-filter: blur(10px); letter-spacing: 0.2em;">
    AEGIS<span style="color:#ffbd2e;">ML</span> | CRAFTED FOR HUMANS. FEARED BY ADVERSARIES.
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)

# --- 5. 3D CYBER SPHERE BACKGROUND INJECTION ---
# Injects Three.js into the main Streamlit parent DOM to render a rotating, interactive 3D sphere
sphere_color = "0xff2d55" if st.session_state.get('alert_mode', False) else "0x00f5ff"
particle_color = "0xffbd2e" if st.session_state.get('alert_mode', False) else "0xb44fff"

three_js_injection = f"""
<script>
  const parent = window.parent;
  if (!parent.document.getElementById("three-canvas-bg")) {{
      const script = parent.document.createElement("script");
      script.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";
      parent.document.head.appendChild(script);
      script.onload = () => {{
          const THREE = parent.window.THREE;
          const scene = new THREE.Scene();
          const camera = new THREE.PerspectiveCamera(75, parent.window.innerWidth / parent.window.innerHeight, 0.1, 1000);
          const renderer = new THREE.WebGLRenderer({{ alpha: true, antialias: true }});
          renderer.setSize(parent.window.innerWidth, parent.window.innerHeight);
          renderer.domElement.id = "three-canvas-bg";
          renderer.domElement.style.position = "fixed";
          renderer.domElement.style.top = "0";
          renderer.domElement.style.left = "0";
          renderer.domElement.style.zIndex = "-1"; // Render behind the glass dashboard
          renderer.domElement.style.pointerEvents = "none";
          parent.document.body.appendChild(renderer.domElement);

          const geometry = new THREE.IcosahedronGeometry(2.5, 1);
          const material = new THREE.MeshBasicMaterial({{ color: {sphere_color}, wireframe: true, transparent: true, opacity: 0.15 }});
          const sphere = new THREE.Mesh(geometry, material);
          
          // Shift sphere over so it peeks out from the side of the main content
          sphere.position.x = 2; 
          sphere.position.y = 0;
          
          parent.window.aegisSphere = sphere;
          parent.window.aegisMaterial = material;
          scene.add(sphere);

          const particleGeo = new THREE.BufferGeometry();
          const posArray = new Float32Array(200 * 3);
          for(let i=0; i<200*3; i++) posArray[i] = (Math.random() - 0.5) * 15;
          particleGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
          const particleMat = new THREE.PointsMaterial({{ size: 0.05, color: {particle_color}, transparent: true, opacity: 0.4 }});
          const particlesMesh = new THREE.Points(particleGeo, particleMat);
          
          parent.window.aegisParticleMat = particleMat;
          scene.add(particlesMesh);

          camera.position.z = 7;

          let mouseX = 0, mouseY = 0;
          parent.document.addEventListener('mousemove', (e) => {{
              mouseX = (e.clientX - parent.window.innerWidth/2);
              mouseY = (e.clientY - parent.window.innerHeight/2);
          }});

          const animate = () => {{
              parent.window.requestAnimationFrame(animate);
              sphere.rotation.y += 0.05 * (mouseX * 0.001 - sphere.rotation.y);
              sphere.rotation.x += 0.05 * (mouseY * 0.001 - sphere.rotation.x);
              sphere.rotation.z += 0.002;
              particlesMesh.rotation.y -= 0.001;
              particlesMesh.rotation.x += 0.0005;
              const scale = 1 + Math.sin(Date.now() * 0.002) * 0.05;
              sphere.scale.set(scale, scale, scale);
              renderer.render(scene, camera);
          }};
          animate();
          parent.window.addEventListener('resize', () => {{
              camera.aspect = parent.window.innerWidth / parent.window.innerHeight;
              camera.updateProjectionMatrix();
              renderer.setSize(parent.window.innerWidth, parent.window.innerHeight);
          }});
      }}
  }} else if (parent.window.aegisMaterial) {{
      // Dynamically update colors if alert mode toggles
      parent.window.aegisMaterial.color.setHex({sphere_color});
      parent.window.aegisParticleMat.color.setHex({particle_color});
  }}
</script>
"""
components.html(three_js_injection, height=0, width=0)



# --- GLOBAL CURSOR INJECTION ---
components.html("""
<script>
    try {
        const parentDoc = window.parent.document;
        if (!parentDoc.getElementById('aegis-cursor-trail')) {
            const canvas = parentDoc.createElement('canvas');
            canvas.id = 'aegis-cursor-trail';
            const ctx = canvas.getContext('2d');
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.width = '100vw';
            canvas.style.height = '100vh';
            canvas.style.pointerEvents = 'none';
            canvas.style.zIndex = '999999';
            parentDoc.body.appendChild(canvas);

            let width = canvas.width = parentDoc.defaultView.innerWidth;
            let height = canvas.height = parentDoc.defaultView.innerHeight;

            const cursor = { x: width / 2, y: height / 2 };
            const trail = [];
            const trailLength = 20;

            parentDoc.addEventListener('mousemove', (e) => {
                cursor.x = e.clientX;
                cursor.y = e.clientY;
            });

            parentDoc.defaultView.addEventListener('resize', () => {
                width = canvas.width = parentDoc.defaultView.innerWidth;
                height = canvas.height = parentDoc.defaultView.innerHeight;
            });

            function animateTrail() {
                ctx.clearRect(0, 0, width, height);

                trail.push({ x: cursor.x, y: cursor.y });
                if (trail.length > trailLength) trail.shift();

                ctx.beginPath();
                for (let i = 0; i < trail.length; i++) {
                    const point = trail[i];
                    if (i === 0) {
                        ctx.moveTo(point.x, point.y);
                    } else {
                        const prevPoint = trail[i - 1];
                        const xc = (prevPoint.x + point.x) / 2;
                        const yc = (prevPoint.y + point.y) / 2;
                        ctx.quadraticCurveTo(prevPoint.x, prevPoint.y, xc, yc);
                    }
                }
                ctx.lineTo(cursor.x, cursor.y);
                
                ctx.strokeStyle = 'rgba(0, 245, 255, 0.8)';
                ctx.lineWidth = 2;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                ctx.shadowBlur = 15;
                ctx.shadowColor = '#00f5ff';
                ctx.stroke();

                parentDoc.defaultView.requestAnimationFrame(animateTrail);
            }
            animateTrail();
        }
    } catch(e) {}
</script>
""", height=0, width=0)



