import textwrap

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("import time\n", "import time\nimport textwrap\n")
content = content.replace('st.markdown("""', 'st.markdown(textwrap.dedent("""')
content = content.replace('""", unsafe_allow_html=True)', '"""), unsafe_allow_html=True)')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
