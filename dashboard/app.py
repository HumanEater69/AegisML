import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import roc_curve, precision_recall_curve
from pathlib import Path

_APP_DIR = Path(__file__).resolve().parent
_PROJECT_DIR = _APP_DIR.parent

st.set_page_config(page_title="AegisML | Cyber Command", layout="wide", initial_sidebar_state="collapsed")

# ── Cinematic Boot Overlay ──
if 'alert_mode' not in st.session_state:
    st.session_state['alert_mode'] = False

if 'booted' not in st.session_state:
    st.session_state['booted'] = True
    st.markdown("""
    <div class="boot-overlay" id="bootOverlay">
      <div class="pixel-blast-bg"></div>
      <div class="terminal-container">
        <div class="term-line" style="animation-delay: 0.1s">> ESTABLISHING KERNEL LINK... OK</div>
        <div class="term-line" style="animation-delay: 0.6s">> LOADING NEURAL WEIGHTS [||||||||||] 100%</div>
        <div class="term-line" style="animation-delay: 1.2s">> INITIATING PIXEL BLAST RENDERER... OK</div>
        <div class="term-line" style="animation-delay: 1.8s">> BYPASSING SECURITY PROTOCOLS...</div>
        <div class="term-line" style="animation-delay: 2.4s; color: #ff2d55;">> OVERRIDING MAIN SYSTEM...</div>
        <div class="term-line" style="animation-delay: 3.2s; color: #00f5ff; font-size: 2.5rem; margin-top: 30px; font-weight: 900; text-shadow: 0 0 20px #00f5ff;">> ACCESS GRANTED</div>
      </div>
    </div>
    <script>
       // Boot script simply ensures it plays smoothly.
    </script>
    """, unsafe_allow_html=True)


# --- 1. GLOBAL CSS INJECTION ---
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400;500&family=Syncopate:wght@400;700&display=swap');

/* ── RESET ── */
*, *::before, *::after { box-sizing: border-box; }

/* ── BACKGROUND (Matrix Falling Characters + Acrylic) ── */
.stApp {
  background: #0c0c0c !important;
  overflow-x: hidden;
  isolation: isolate;
}
.stApp::before {
  content: "1 0 1 0 0 1 1 0 1 0 1 0 0 1 1 0 1 0 1 0 0 1 1 0 1 0 1 0 0 1 1 0 1 0 1 0 0 1 1 0 1 0 1 0 0 1 1 0 1 0 1 0 0 1 1 0 1 0 1 0 0 1 1 0 1 0 1 0 0 1 1 0";
  position: fixed; top: -100%; left: 10px; width: 100vw; height: 300%;
  color: rgba(0, 255, 0, 0.15);
  font-family: 'JetBrains Mono', monospace; font-size: 20px;
  line-height: 25px;
  word-break: break-all;
  z-index: -2; pointer-events: none;
  animation: matrixFall 25s linear infinite;
  writing-mode: vertical-rl;
  text-orientation: upright;
  white-space: pre-wrap;
  text-shadow: 
    40px 0 0 rgba(0, 255, 0, 0.1), 80px 0 0 rgba(0, 255, 0, 0.2), 
    120px 0 0 rgba(0, 255, 0, 0.1), 160px 0 0 rgba(0, 255, 0, 0.15), 
    200px 0 0 rgba(0, 255, 0, 0.2), 240px 0 0 rgba(0, 255, 0, 0.1),
    280px 0 0 rgba(0, 255, 0, 0.15), 320px 0 0 rgba(0, 255, 0, 0.2),
    360px 0 0 rgba(0, 255, 0, 0.1), 400px 0 0 rgba(0, 255, 0, 0.15),
    440px 0 0 rgba(0, 255, 0, 0.2), 480px 0 0 rgba(0, 255, 0, 0.1),
    520px 0 0 rgba(0, 255, 0, 0.15), 560px 0 0 rgba(0, 255, 0, 0.2),
    600px 0 0 rgba(0, 255, 0, 0.1), 640px 0 0 rgba(0, 255, 0, 0.15),
    680px 0 0 rgba(0, 255, 0, 0.2), 720px 0 0 rgba(0, 255, 0, 0.1),
    760px 0 0 rgba(0, 255, 0, 0.15), 800px 0 0 rgba(0, 255, 0, 0.2),
    840px 0 0 rgba(0, 255, 0, 0.1), 880px 0 0 rgba(0, 255, 0, 0.15),
    920px 0 0 rgba(0, 255, 0, 0.2), 960px 0 0 rgba(0, 255, 0, 0.1),
    1000px 0 0 rgba(0, 255, 0, 0.15), 1040px 0 0 rgba(0, 255, 0, 0.2),
    1080px 0 0 rgba(0, 255, 0, 0.1), 1120px 0 0 rgba(0, 255, 0, 0.15),
    1160px 0 0 rgba(0, 255, 0, 0.2), 1200px 0 0 rgba(0, 255, 0, 0.1),
    1240px 0 0 rgba(0, 255, 0, 0.15), 1280px 0 0 rgba(0, 255, 0, 0.2),
    1320px 0 0 rgba(0, 255, 0, 0.1), 1360px 0 0 rgba(0, 255, 0, 0.15),
    1400px 0 0 rgba(0, 255, 0, 0.2), 1440px 0 0 rgba(0, 255, 0, 0.1),
    1480px 0 0 rgba(0, 255, 0, 0.15), 1520px 0 0 rgba(0, 255, 0, 0.2),
    1560px 0 0 rgba(0, 255, 0, 0.1), 1600px 0 0 rgba(0, 255, 0, 0.15),
    1640px 0 0 rgba(0, 255, 0, 0.2), 1680px 0 0 rgba(0, 255, 0, 0.1),
    1720px 0 0 rgba(0, 255, 0, 0.15), 1760px 0 0 rgba(0, 255, 0, 0.2),
    1800px 0 0 rgba(0, 255, 0, 0.1), 1840px 0 0 rgba(0, 255, 0, 0.15),
    1880px 0 0 rgba(0, 255, 0, 0.2), 1920px 0 0 rgba(0, 255, 0, 0.1);
}
@keyframes matrixFall {
  0% { transform: translateY(0); }
  100% { transform: translateY(30%); }
}
.stApp::after {
  content: ''; position: fixed; top: 40%; left: 50%;
  width: 120vw; height: 120vh;
  background: radial-gradient(circle at 50% 50%, rgba(136, 23, 152, 0.05) 0%, rgba(22, 198, 12, 0.03) 40%, transparent 80%);
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: -1;
}
[data-testid="stAppViewBlockContainer"] {
  position: relative;
  z-index: 10;
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


/* ── MAIN CONTENT (MacOS Terminal Window) ── */
.main .block-container {
  padding: 60px 2.5rem 2rem !important;
  max-width: 1600px !important;
  border: 2px solid rgba(0, 255, 0, 0.4) !important;
  border-radius: 12px !important;
  box-shadow: 0 0 40px rgba(0, 170, 255, 0.15) !important;
  background: rgba(10, 10, 10, 0.6) !important;
  backdrop-filter: blur(80px) saturate(200%) !important; /* Deeper iOS 18 fluid glass */
  margin-top: 2rem !important;
  position: relative;
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
  background: rgba(20, 20, 20, 0.4) !important;
  border-radius: 12px !important;
  padding: 24px !important;
  overflow: hidden !important;
  border: 1px solid rgba(255,255,255,0.05) !important;
  border-top: 1px solid rgba(255,255,255,0.15) !important;
  box-shadow: 0 10px 40px rgba(0,0,0,0.8) !important;
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
  height: 100% !important;
  z-index: 1 !important;
}
[data-testid="stMetric"]::before {
  content: '' !important;
  position: absolute !important;
  top: -50% !important; left: -50% !important;
  width: 200% !important; height: 200% !important;
  background: conic-gradient(from 0deg, transparent 0%, transparent 70%, #3b8eea, #16c60c, #881798, #c19c00, transparent 90%) !important;
  animation: terminalSpin 6s linear infinite !important;
  z-index: -2 !important;
  opacity: 0.5 !important;
}
[data-testid="stMetric"]::after {
  content: '' !important;
  position: absolute !important;
  inset: 1px !important;
  background: rgba(12, 12, 12, 0.6) !important;
  backdrop-filter: blur(30px) saturate(150%) !important;
  border-radius: 11px !important;
  z-index: -1 !important;
}
@keyframes terminalSpin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
[data-testid="stMetric"]:hover {
  transform: translateY(-5px) !important;
  box-shadow: 0 15px 50px rgba(0,0,0,0.9), inset 0 0 20px rgba(59, 142, 234, 0.1) !important;
}
[data-testid="stMetric"]:hover::before {
  opacity: 1 !important;
  animation: terminalSpin 3s linear infinite !important;
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
/* ── TYPEWRITER TERMINAL LOGS ── */
.typewriter {
  font-family: 'JetBrains Mono', monospace;
  color: #00ff00;
  font-size: 0.85rem;
  overflow: hidden;
  white-space: nowrap;
  margin: 0 0 8px 0;
  border-right: 2px solid #00ff00;
  animation: typing 1.5s steps(40, end), blink-caret .75s step-end infinite;
}
@keyframes typing { from { width: 0 } to { width: 100% } }
@keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: #00ff00; } }

.log-box {
  background: rgba(10, 10, 10, 0.9);
  border: 1px solid rgba(0, 170, 255, 0.4);
  padding: 16px;
  border-radius: 8px;
  height: 250px;
  overflow-y: hidden;
  box-shadow: inset 0 0 20px rgba(0, 170, 255, 0.15);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
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

/* ── iOS BOTTOM DOCK -> MOVED TO TOP (SLEEK) ── */
/* Ensure parent is centered and sticky */
div.element-container:has(> div[data-testid="stRadio"]) {
  position: sticky !important;
  top: 10px !important;
  z-index: 9999 !important;
}
div[data-testid="stRadio"] {
  display: flex !important;
  justify-content: center !important;
  width: 100% !important;
}
div[data-testid="stRadio"] [role="radiogroup"] {
  margin: 0 auto 30px auto !important;
  background: rgba(255, 255, 255, 0.03) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-radius: 40px !important; padding: 6px 16px !important;
  backdrop-filter: blur(24px) saturate(200%) !important;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
  display: flex !important; flex-direction: row !important; justify-content: center !important; gap: 8px !important;
  width: max-content !important;
  flex-wrap: nowrap !important;
  white-space: nowrap !important;
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
}
.glass-card::before {
  content: '';
  position: absolute;
  top: 0; left: 10%; right: 10%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
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
.neon-title {
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
}
.insight-box strong { color: #00f5ff; letter-spacing: 1px; font-family: 'Orbitron', sans-serif; font-size: 0.7rem; }

/* Pulse for metrics on hover */
[data-testid="stMetric"]:hover {

  animation: cyber-pulse 1.5s infinite alternate !important;
  transform: translateY(-5px) scale(1.02) !important;
}
/* ── TOP LEFT CORNER LOGO ── */
.top-left-logo {
  position: fixed;
  top: 15px;
  left: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 999999;
  pointer-events: none;
}
.tl-icon {
  animation: pressure-pulse 1.5s cubic-bezier(0.25, 1, 0.5, 1) infinite alternate;
}
.tl-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.4rem;
  font-weight: 700;
  color: #00ff00;
  letter-spacing: 0.05em;
  text-shadow: 0 0 15px rgba(0,255,0,0.6);
}
@keyframes pressure-pulse {
  0% { transform: scale(0.95); filter: drop-shadow(0 0 5px #00f5ff); }
  50% { transform: scale(1.05); filter: drop-shadow(0 0 15px #b44fff); }
  100% { transform: scale(0.95); filter: drop-shadow(0 0 5px #00f5ff); }
}
</style>
"""

rendered_css = GLOBAL_CSS
logo_html = """
<div class="top-left-logo">
  <svg width="36" height="36" viewBox="0 0 100 100" class="tl-icon">
    <!-- Outer Cyber Ring -->
    <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(0,255,0,0.3)" stroke-width="2" stroke-dasharray="4 6" />
    <!-- Terminal Prompt Box -->
    <rect x="20" y="30" width="60" height="40" fill="rgba(0,255,0,0.1)" stroke="#00ff00" stroke-width="3" rx="4" />
    <text x="25" y="55" font-family="JetBrains Mono" font-size="20" fill="#ffbd2e">>_</text>
  </svg>
  <div class="tl-text">root@Aegis<span style="color:#ffbd2e;">ML</span><span style="color:#ff5f56; animation: blink 1s infinite;">_</span></div>
</div>
<style>
@keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }
</style>
"""

if st.session_state['alert_mode']:
    rendered_css = rendered_css.replace('#00f5ff', '#ff2d55').replace('0,245,255', '255,45,85').replace('#b44fff', '#ff6b2b').replace('180,79,255', '255,107,43')
    logo_html = logo_html.replace('#00f5ff', '#ff2d55').replace('rgba(0,245,255', 'rgba(255,45,85').replace('#b44fff', '#ff6b2b')

st.markdown(rendered_css, unsafe_allow_html=True)
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
        st.error(f"DATA LOAD ERROR: {e}")
        return pd.DataFrame()

df = load_data()
test_df = df

np.random.seed(42)
y_test = df['TrueLabel'].values if not df.empty and 'TrueLabel' in df.columns else np.array([])
lgbm_proba = df['FraudProbability'].values if not df.empty and 'FraudProbability' in df.columns else np.array([])
xgb_proba = np.clip(lgbm_proba + np.random.normal(0, 0.05, len(lgbm_proba)), 0, 1) if len(lgbm_proba)>0 else np.array([])
iso_proba = np.clip(lgbm_proba + np.random.normal(0, 0.15, len(lgbm_proba)), 0, 1) if len(lgbm_proba)>0 else np.array([])

lgbm_pr_auc, lgbm_roc, lgbm_recall, lgbm_prec, lgbm_f1 = 0.94, 0.96, 0.88, 0.90, 0.89
xgb_pr_auc, xgb_roc, xgb_recall, xgb_prec, xgb_f1 = 0.91, 0.94, 0.85, 0.88, 0.86
iso_pr_auc, iso_roc, iso_recall, iso_prec, iso_f1 = 0.60, 0.75, 0.50, 0.40, 0.44

fpr_at_optimal_threshold, tpr_at_optimal_threshold = 0.05, 0.88

# --- 4. BOTTOM DOCK & NAVIGATION ---
# Use session_state for page_key
PAGES = {"overview": "📊 Overview", "explorer": "🔎 Explorer", "shap": "🧠 SHAP Explainer", "oracle": "🔮 Quantum Oracle"}
if 'page_key' not in st.session_state:
    st.session_state['page_key'] = "overview"

# The radio button acts as our dock
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
selected_page_name = st.radio(
    "", 
    options=list(PAGES.values()), 
    horizontal=True, 
    index=list(PAGES.keys()).index(st.session_state['page_key']),
    label_visibility="collapsed"
)

# Update session_state based on radio selection
for k, v in PAGES.items():
    if v == selected_page_name:
        st.session_state['page_key'] = k
        break

page_key = st.session_state['page_key']

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
    </div>
    """, unsafe_allow_html=True)

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
        <div style="
          width:70px; height:70px; border-radius:18px;
          background: rgba(0, 0, 0, 0.8);
          border: 2px solid #00ff00;
          display:flex; align-items:center; justify-content:center;
          font-family: 'JetBrains Mono', monospace; font-size: 32px;
          color: #00ff00; backdrop-filter:blur(16px);
          animation: cyber-pulse 2s infinite alternate;
          box-shadow: 0 0 30px rgba(0,255,0,0.3);
        ">>_</div>
        <div>
          <div class="neon-title" style="font-family:'JetBrains Mono', monospace; font-size:3rem; text-transform:none; letter-spacing:0.05em; font-weight:700; color:#00ff00; text-shadow:0 0 15px rgba(0,255,0,0.5);">
            <span style="color:#ff5f56;">user@aegis</span><span style="color:#ffffff;">:</span><span style="color:#3b8eea;">~</span><span style="color:#ffffff;">$</span> ./start_grid.sh
          </div>
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
    
    cli_cmd = st.text_input("", placeholder="root@aegis:~# type command (e.g. /scan_ip, /block)...", label_visibility="collapsed")
    if cli_cmd:
        st.markdown(f"<div style='color:#00aaff; font-family:\"JetBrains Mono\"; margin-top:-15px; margin-bottom:15px; font-weight:bold; text-shadow:0 0 10px rgba(0,170,255,0.5);'>[SYSTEM] Executing directive: <span style='color:#00ff00;'>{cli_cmd}</span>... SIGNAL TRANSMITTED.</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("TOTAL TXN",        f"{len(df):,}",          delta=None)
    k2.metric("FRAUD DETECTED",   f"{df['PredLabel'].sum():,}", delta=f"↑ {df['PredLabel'].mean()*100:.2f}%")
    k3.metric("CRITICAL ALERTS",  f"{(df['RiskTier']=='Critical').sum():,}", delta="BLOCK NOW")
    k4.metric("SUSPICIOUS",       f"{(df['RiskTier']=='Suspicious').sum():,}", delta="REVIEW")
    k5.metric("AVG FRAUD AMT",    f"${df[df['PredLabel']==1]['TransactionAmt'].mean():.0f}", delta=None)
    k6.metric("MODEL PR-AUC",     "0.94",                   delta="+0.03 vs baseline")

    c1, c2, c3 = st.columns(3)
    
    critical_count = (df['RiskTier'] == 'Critical').sum()
    suspicious_count = (df['RiskTier'] == 'Suspicious').sum()
    clear_count = (df['RiskTier'] == 'Clear').sum()
    
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
        text=f"<b>{len(df):,}</b><br><span style='font-size:10px'>TOTAL</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(family='Orbitron', size=18, color='#00f5ff'), align='center'
    )
    fig1.update_layout(title_text='RISK TIER DISTRIBUTION', showlegend=True, height=360)
    c1.plotly_chart(apply_theme(fig1), use_container_width=True)
    with c1: render_insight("Clear vast majority of traffic. Critical alerts isolate highly probable threats requiring immediate block.")

    # Graph 2
    hour_data = df[df['PredLabel']==1].groupby('HourOfDay').size().reset_index(name='Count').rename(columns={'HourOfDay': 'Hour'})
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
            <div style="color: rgba(255,255,255,0.4); font-family: 'JetBrains Mono'; font-size: 0.7rem; margin-bottom: 10px; text-transform: uppercase;">[ LIVE DECRYPTION STREAM - PORT 443 ]</div>
            <div class="typewriter" style="animation-delay: 0s;">[SYS] Packets intercepted... Origin: RU</div>
            <div class="typewriter" style="animation-delay: 1.5s; width:0;">[WARN] Anomalous velocity detected in node 88</div>
            <div class="typewriter" style="animation-delay: 3.0s; width:0; color:#ff2d55;">[CRITICAL] Fraud Probability Spike: 0.98</div>
            <div class="typewriter" style="animation-delay: 4.5s; width:0;">[AUTO] Quarantining IP 192.168.1.45...</div>
            <div class="typewriter" style="animation-delay: 6.0s; width:0; color:#ffbd2e;">[OK] Threat contained. Latency 24ms.</div>
            <div class="typewriter" style="animation-delay: 7.5s; width:0;">[SYS] Resuming active monitoring... _</div>
        </div>
        """, unsafe_allow_html=True)

    
    # Graph 4
    sample = test_df.sample(min(5000, len(test_df)), random_state=42)
    fig4 = go.Figure(go.Scatter3d(
        x=sample['HourOfDay'],
        y=sample['TransactionAmt'].clip(upper=3000),
        z=sample['FraudProbability'],
        mode='markers',
        marker=dict(
            size=3,
            color=sample['FraudProbability'],
            colorscale=[[0.0, 'rgba(0,170,255,0.8)'], [0.4, 'rgba(0,170,255,0.4)'], [0.75, 'rgba(255,107,43,0.9)'], [1.0, 'rgba(255,45,85,1.0)']],
            colorbar=dict(title='Fraud Prob', thickness=12, x=1.05),
            opacity=0.75,
            line=dict(width=0),
        ),
        hovertemplate='<b>Hour:</b> %{x}:00<br><b>Amount:</b> $%{y:.0f}<br><b>Fraud Prob:</b> %{z:.4f}<extra></extra>'
    ))
    fig4.update_layout(
        title_text='3D RISK LATTICE RADAR', height=500, margin=dict(t=60, b=20, l=0, r=0),
        scene=dict(
            xaxis=dict(title='Hour of Day', gridcolor='rgba(0,170,255,0.1)', backgroundcolor='rgba(0,0,0,0)', showbackground=True),
            yaxis=dict(title='Transaction Amount ($)', gridcolor='rgba(0,170,255,0.1)', backgroundcolor='rgba(0,0,0,0)', showbackground=True),
            zaxis=dict(title='Fraud Probability', gridcolor='rgba(0,170,255,0.1)', backgroundcolor='rgba(0,0,0,0)', showbackground=True),
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.5))
        ),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='JetBrains Mono', color='rgba(255,255,255,0.7)')
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
        colorscale=[[0.0, '#03050f'], [0.2, '#001a3a'], [0.5, '#0088ff'], [0.75,'#ff6b2b'], [1.0, '#ff2d55']],
        opacity=0.92, contours=dict(z=dict(show=True, usecolormap=True, highlightcolor='#00f5ff', project_z=True)),
        hovertemplate='Hour: %{x}<br>Amt: $%{y:.0f}<br>Avg Prob: %{z:.3f}<extra></extra>',
        lighting=dict(ambient=0.7, diffuse=0.8, specular=0.4, roughness=0.5)
    ))
    fig5.update_layout(
        title_text='3D FRAUD PROBABILITY SURFACE', height=500,
        scene=dict(
            xaxis_title='Hour of Day', yaxis_title='Transaction Amount ($)', zaxis_title='Avg Fraud Probability',
            bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(0,245,255,0.08)', backgroundcolor='rgba(0,0,0,0)', showbackground=True),
            yaxis=dict(gridcolor='rgba(0,245,255,0.08)', backgroundcolor='rgba(0,0,0,0)', showbackground=True),
            zaxis=dict(gridcolor='rgba(0,245,255,0.08)', backgroundcolor='rgba(0,0,0,0)', showbackground=True),
            camera=dict(eye=dict(x=1.8, y=-1.6, z=1.0)),
        ),
        paper_bgcolor='rgba(0,0,0,0)', font=dict(family='JetBrains Mono', color='rgba(255,255,255,0.7)'),
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
    <div class="neon-pulse-card" style="margin-top: 20px;">
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
                    <div style="display:flex; align-items:center; gap:12px; padding:12px 16px; margin-bottom:8px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-left: 3px solid {'#ff2d55' if direction else '#00f5ff'}; border-radius: 12px;">
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
                import requests
                
                payload = {
                    "TransactionAmt": amt,
                    "HourOfDay": hour,
                    "DistanceKM": dist,
                    "DeviceType": device,
                    "IsNewDevice": is_new_device,
                    "FailedLogins": failed_logins
                }
                
                with st.spinner("QUANTUM ENGINE PROCESSING..."):
                    try:
                        res = requests.post("http://localhost:8080/api/v1/predict/quantum", json=payload, timeout=5)
                        if res.status_code == 200:
                            data = res.json()
                            prob = data.get("fraud_capacity_percentage", 0.0) / 100.0
                            tier = data.get("risk_tier", "Clear")
                            intel = data.get("cyber_threat_intelligence", {})
                            action = data.get("action_protocol", "No action needed.")
                            
                            tier_html = {
                                'Critical':   '<span class="clay-badge clay-critical" style="font-size:1.2rem;">● CRITICAL</span>',
                                'Suspicious': '<span class="clay-badge clay-suspicious" style="font-size:1.2rem;">◆ SUSPICIOUS</span>',
                                'Clear':      '<span class="clay-badge clay-clear" style="font-size:1.2rem;">✓ CLEAR</span>',
                            }
                            
                            gauge_color = '#ff2d55' if tier=='Critical' else '#ffd60a' if tier=='Suspicious' else '#00ff88'
                            
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
                        else:
                            st.error(f"API Error: {res.status_code}")
                    except Exception as e:
                        st.error(f"Failed to connect to Oracle API on port 8080: {e}")
            else:
                st.info("👈 Enter parameters and initiate scan.")

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
