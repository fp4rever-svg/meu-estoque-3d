import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="📦 Otimizador de Estoque 3D", layout="centered")

# Função para desenhar as caixas no gráfico 3D
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
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=0.5, edgecolors='black', alpha=alpha))

st.title("📦 Otimizador de Estoque 3D")
st.markdown("Calcule a capacidade máxima e visualize a melhor forma de organizar suas caixas.")

# --- ENTRADA DE DADOS ---
with st.container():
    st.subheader("📏 Dimensões da Caixa A (Destino)")
    col_a1, col_a2, col_a3 = st.columns(3)
    la = col_a1.number_input("Largura A (cm)", min_value=1.0, value=60.0)
    aa = col_a2.number_input("Profundidade A (cm)", min_value=1.0, value=40.0)
    pa = col_a3.number_input("Altura A (cm)", min_value=1.0, value=40.0)

    st.divider()

    st.subheader("💊 Dimensões da Caixa B (Produto)")
    nome_b = st.text_input("Nome do Produto", value="Caixa de Remédio")
    col_b1, col_b2, col_b3 = st.columns(3)
    lb = col_b1.number_input("Largura B (cm)", min_value=0.1, value=10.0)
    ab = col_b2.number_input("Profundidade B (cm)", min_value=0.1, value=5.0)
    pb = col_b3.number_input("Altura B (cm)", min_value=0.1, value=3.0)

st.write("")
modo_vis = st.radio("Modo de Visualização:", ["Apenas uma unidade (Posição Inicial)", "Preenchimento Total (Simulação)"], horizontal=True)

# --- CÁLCULO ---
if st.button("CALCULAR E VISUALIZAR", type="primary", use_container_width=True):
    # Testar as 6 orientações possíveis
    orientacoes = [
        (lb, ab, pb, "Deitado (Padrão)"), (lb, pb, ab, "De lado (Horizontal)"),
        (ab, lb, pb, "Girado 90º"), (ab, pb, lb, "Em pé (Lateral)"),
        (pb, lb, ab, "Em pé (Frente)"), (pb, ab, lb, "Vertical (Topo)")
    ]

    melhor_qtd = -1
    melhor_config = None

    for l, a, p, nome in orientacoes:
        nx, ny, nz = la // l, aa // a, pa // p
        qtd = int(nx * ny * nz)
        if qtd > melhor_qtd:
            melhor_qtd = qtd
            melhor_config = (l, a, p, nome, nx, ny, nz)

    l, a, p, nome, nx, ny, nz = melhor_config
    aproveitamento = (melhor_qtd * (lb * ab * pb) / (la * aa * pa)) * 100

    # Resultados em métricas
    m1, m2 = st.columns(2)
    m1.metric("Capacidade Máxima", f"{melhor_qtd} un")
    m2.metric("Aproveitamento de Volume", f"{aproveitamento:.1f}%")
    st.success(f"💡 **Sugestão de Organização:** Coloque a caixa na posição **{nome}**.")

    # --- GRÁFICO 3D ---
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Desenhar Caixa A (Container)
    desenhar_caixa(ax, [0,0,0], [la, aa, pa], color='lightgray', alpha=0.1)
    
    if modo_vis == "Apenas uma unidade (Posição Inicial)":
        desenhar_caixa(ax, [0,0,0], [l, a, p], color='green', alpha=0.8)
    else:
        # Desenhar preenchimento (limitado para performance visual)
        limite_desenho = 500
        count = 0
        for xi in range(int(nx)):
            for yi in range(int(ny)):
                for zi in range(int(nz)):
                    if count < limite_desenho:
                        desenhar_caixa(ax, [xi*l, yi*a, zi*p], [l, a, p], color='green', alpha=0.3)
                        count += 1
        if melhor_qtd > limite_desenho:
            st.warning(f"Exibindo apenas as primeiras {limite_desenho} unidades para manter a fluidez do gráfico.")

    # Ajustes de visualização
    max_dim = max(la, aa, pa)
    ax.set_xlim([0, max_dim]); ax.set_ylim([0, max_dim]); ax.set_zlim([0, max_dim])
    ax.set_xlabel('Largura (cm)'); ax.set_ylabel('Altura (cm)'); ax.set_zlabel('Profundidade (cm)')
    
    st.pyplot(fig)
