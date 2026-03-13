import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

st.set_page_config(page_title="Otimizador de Estoque Vertical", layout="centered")

def desenhar_caixa(ax, pos, size, color='green', alpha=0.2):
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

st.title("📦 Otimizador de Estoque (Posição Vertical)")
st.write("Calculando o máximo de caixas B mantendo todas obrigatoriamente **em pé**.")

# --- DADOS DA CAIXA A (PADRÃO) ---
st.subheader("📏 Medidas Fixas da Caixa A")
col_a = st.columns(3)
la = col_a[0].number_input("Largura A", value=18.5, disabled=True)
pa = col_a[1].number_input("Profundidade A", value=46.5, disabled=True)
aa = col_a[2].number_input("Altura A", value=17.0, disabled=True)

st.divider()

# --- INPUTS DA CAIXA B ---
st.subheader("💊 Medidas da Caixa B (Produto)")
nome_b = st.text_input("Nome do Produto", value="Remédio X")
col_b = st.columns(3)
lb = col_b[0].number_input("Largura B", value=3.0)
pb = col_b[1].number_input("Profundidade B", value=5.0)
ab = col_b[2].number_input("Altura B (Eixo Vertical)", value=10.0)

if st.button("CALCULAR MELHOR ENCAIXE VERTICAL", type="primary", use_container_width=True):
    # Como elas devem ficar "em pé", a Altura B (ab) é fixa no eixo Z.
    # Só podemos rotacionar a base (lb e pb) no plano horizontal.
    
    # Opção 1: Largura B com Largura A
    qtd1_l = la // lb
    qtd1_p = pa // pb
    qtd1_a = aa // ab
    total1 = int(qtd1_l * qtd1_p * qtd1_a)
    
    # Opção 2: Girar a base em 90 graus (Profundidade B com Largura A)
    qtd2_l = la // pb
    qtd2_p = pa // lb
    qtd2_a = aa // ab
    total2 = int(qtd2_l * qtd2_p * qtd2_a)

    # Escolher a melhor das duas
    if total1 >= total2:
        res_total, res_l, res_p, res_a = total1, lb, pb, ab
        orientacao = "Base padrão (Largura com Largura)"
    else:
        res_total, res_l, res_p, res_a = total2, pb, lb, ab
        orientacao = "Base girada (Profundidade com Largura)"

    aproveitamento = (res_total * (lb * ab * pb) / (la * aa * pa)) * 100

    # Exibição
    st.metric("Capacidade Máxima", f"{res_total} unidades")
    st.info(f"💡 **Como posicionar:** {orientacao}")
    st.write(f"Aproveitamento de volume: {aproveitamento:.2f}%")

    # Visualização
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    desenhar_caixa(ax, [0,0,0], [la, pa, aa], color='lightgray', alpha=0.1)
    
    # Desenhar exemplo de preenchimento
    count = 0
    for xi in range(int(la // res_l)):
        for yi in range(int(pa // res_p)):
            for zi in range(int(aa // res_a)):
                if count < 300: # Limite visual
                    desenhar_caixa(ax, [xi*res_l, yi*res_p, zi*res_a], [res_l, res_p, res_a], color='green', alpha=0.3)
                    count += 1
    
    ax.set_xlim([0, 50]); ax.set_ylim([0, 50]); ax.set_zlim([0, 50])
    st.pyplot(fig)

