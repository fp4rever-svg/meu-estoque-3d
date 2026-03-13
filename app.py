# 1. Instalações
!pip install py3dbp streamlit -q

# 2. Criar o arquivo do App de forma robusta
import os

app_code = """
import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

st.set_page_config(page_title="Otimizador 3D", layout="centered")

# Função de desenho
def desenhar_caixa(ax, pos, size, color='blue', alpha=0.3):
    x, y, z = pos
    dx, dy, dz = size
    vertices = np.array([[x, y, z], [x+dx, y, z], [x+dx, y+dy, z], [x, y+dy, z],
                         [x, y, z+dz], [x+dx, y, z+dz], [x+dx, y+dy, z+dz], [x, y+dy, z+dz]])
    faces = [[vertices[0], vertices[1], vertices[2], vertices[3]],
             [vertices[4], vertices[5], vertices[6], vertices[7]], 
             [vertices[0], vertices[1], vertices[5], vertices[4]],
             [vertices[2], vertices[3], vertices[7], vertices[6]], 
             [vertices[0], vertices[3], vertices[7], vertices[4]],
             [vertices[1], vertices[2], vertices[6], vertices[5]]]
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='black', alpha=alpha))

st.title("📦 Otimizador de Estoque 3D")

# --- CAMPOS DE ENTRADA ---
st.subheader("📏 Dimensões da Caixa A")
c1, c2, c3 = st.columns(3)
la = c1.number_input("Largura A", 1.0, 500.0, 60.0)
aa = c2.number_input("Altura A", 1.0, 500.0, 40.0)
pa = c3.number_input("Profundidade A", 1.0, 500.0, 40.0)

st.divider()

st.subheader("💊 Dimensões da Caixa B")
col_b1, col_b2, col_b3 = st.columns(3)
lb = col_b1.number_input("Largura B", 0.1, 500.0, 10.0)
ab = col_b2.number_input("Altura B", 0.1, 500.0, 5.0)
pb = col_b3.number_input("Profundidade B", 0.1, 500.0, 3.0)

if st.button("CALCULAR MELHOR POSIÇÃO", type="primary", use_container_width=True):
    orientacoes = [
        (lb, ab, pb, "Deitado"), (lb, pb, ab, "De lado"),
        (ab, lb, pb, "Girado"), (ab, pb, lb, "Em pé (Lateral)"),
        (pb, lb, ab, "Em pé (Frente)"), (pb, ab, lb, "Vertical")
    ]
    melhor_qtd = -1
    melhor_config = None

    for l, a, p, nome in orientacoes:
        qtd = (la // l) * (aa // a) * (pa // p)
        if qtd > melhor_qtd:
            melhor_qtd = int(qtd)
            melhor_config = (l, a, p, nome)

    l, a, p, nome = melhor_config
    
    st.metric("Capacidade Máxima", f"{melhor_qtd} unidades")
    st.info(f"💡 Posicione a caixa: **{nome}**")

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    desenhar_caixa(ax, [0,0,0], [la, aa, pa], color='lightgray', alpha=0.1)
    desenhar_caixa(ax, [0,0,0], [l, a, p], color='green', alpha=0.8)
    
    max_dim = max(la, aa, pa)
    ax.set_xlim([0, max_dim]); ax.set_ylim([0, max_dim]); ax.set_zlim([0, max_dim])
    st.pyplot(fig)
"""

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

# 3. Gerar link de acesso via LocalTunnel de forma estável
import urllib
print("SENHA (IP):", urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip())

!streamlit run app.py & npx localtunnel --port 8501