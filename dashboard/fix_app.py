import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

landing_page_html = '''
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Manrope:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');
    .stApp { background: #03050f; overflow: hidden; }
    
    .landing-btn {
        background: linear-gradient(135deg, #00dce5, #00696e) !important;
        box-shadow: inset 0 2px 4px rgba(255,255,255,0.4), 0 8px 16px rgba(0, 220, 229, 0.4) !important;
        border-radius: 9999px !important; color: #002021 !important;
        font-family: 'JetBrains Mono', monospace !important; font-weight: 700 !important;
        padding: 15px 40px !important; border: none !important; cursor: pointer;
        transition: all 0.3s;
    }
    .landing-btn:hover { transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)
    
    st.components.v1.html("""
    <canvas id='matrix-canvas'></canvas>
    <script>
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const letters = '01ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        const fontSize = 14; const columns = canvas.width / fontSize;
        const drops = Array.from({ length: columns }).fill(1);
        setInterval(() => {
            ctx.fillStyle = 'rgba(3, 5, 15, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.font = fontSize + 'px "JetBrains Mono"';
            for (let i = 0; i < drops.length; i++) {
                const text = letters[Math.floor(Math.random() * letters.length)];
                ctx.fillStyle = Math.random() > 0.95 ? '#8405cf' : '#00dce5';
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }, 33);
        window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; });
    </script>
    <style>
        body { margin:0; overflow:hidden; background: #03050f; }
        #matrix-canvas { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; opacity: 0.3; pointer-events: none; }
    </style>
    """, height=0, width=0)
    
    st.markdown("""
    <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; pointer-events: none;">
        <style>iframe[title="st.iframe"] { position: fixed !important; top: 0 !important; left: 0 !important; width: 100vw !important; height: 100vh !important; z-index: -999 !important; border: none !important; pointer-events: none !important; }</style>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-family: \\'Sora\\', sans-serif; font-size: 5rem; font-weight: 800; color: #e9feff; text-align: center; margin-top: 20vh; text-shadow: 0 0 15px rgba(0,245,255,0.4);">The Ghost in the Ledger.</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family: \\'Manrope\\', sans-serif; font-size: 1.2rem; color: #b9caca; text-align: center; max-width: 600px; margin: 0 auto 40px auto;">Deploying state-of-the-art cryptographic telemetry and machine learning kernels to secure the next frontier of decentralized financial infrastructure.</div>', unsafe_allow_html=True)
'''

# Replace the landing page logic
content = re.sub(r"if not st\.session_state\.get\('entered', False\):.*?st\.stop\(\)", 
                 "if not st.session_state.get('entered', False):\n" + landing_page_html + "\n    col1, col2, col3 = st.columns([1,1,1])\n    with col2:\n        if st.button('Initialize Core', use_container_width=True):\n            st.session_state['entered'] = True\n            st.rerun()\n    st.stop()", 
                 content, flags=re.DOTALL)

# Fix CSS: Remove absolute positioning from top dock
content = content.replace('position: absolute !important;', 'position: relative !important;')
content = content.replace('top: 15px !important;', '')
content = content.replace('left: 50% !important;', '')
content = content.replace('transform: translateX(-50%) !important;', '')

# Fix CSS matrix overlay causing vertical text: remove sidebar display:none
content = content.replace('[data-testid="stSidebar"] { display:none !important; }', '')
content = content.replace('[data-testid="stSidebarCollapsedControl"] { display:none !important; }', '')

# Apply colors to global CSS
content = content.replace('background: #0c0e10 !important;', 'background: #03050f !important;')
content = content.replace('rgba(57, 255, 20, 0.2)', 'rgba(0, 220, 229, 0.2)') 
content = content.replace('rgba(57, 255, 20, 0.15)', 'rgba(0, 220, 229, 0.15)') 
content = content.replace('#39ff14', '#00dce5') # neon green -> cyber blue
content = content.replace('#efffe3', '#e9feff') # white
content = content.replace('#baccb0', '#b9caca') # grey
content = content.replace('rgba(57, 255, 20, 0.05)', 'rgba(0, 220, 229, 0.05)') 
content = content.replace('rgba(57, 255, 20, 0.4)', 'rgba(0, 220, 229, 0.4)') 

# Fix glassmorphism liquid graphs
content = content.replace("plot_bgcolor='rgba(255,255,255,0.02)'", "plot_bgcolor='rgba(0,0,0,0)'")

# Fix plotly colors
content = content.replace('#00f5ff', '#00dce5')
content = content.replace('#ff6b2b', '#ff6b2b') # orange
content = content.replace('#ff2d55', '#ff2d55') # red
content = content.replace('#ffd60a', '#ffd60a') # yellow
content = content.replace('#00ff88', '#00ff88') # green
content = content.replace('#b44fff', '#8405cf') # purple

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
