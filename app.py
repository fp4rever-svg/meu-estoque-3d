import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Otimizador de Estoque", layout="centered")

st.title("📦 Otimizador de Estoque (Posição Vertical)")
st.markdown("Cálculo de capacidade máxima mantendo as caixas **em pé**.")

# --- DADOS DA CAIXA A (PADRÃO FIXO) ---
st.subheader("📏 Medidas da Caixa A (Fixas)")
col_a1, col_a2, col_a3 = st.columns(3)
la = 18.5
pa = 46.5
aa = 17.0

col_a1.metric("Largura", f"{la} cm")
col_a2.metric("Profundidade", f"{pa} cm")
col_a3.metric("Altura", f"{aa} cm")

st.divider()

# --- INPUTS DA CAIXA B ---
st.subheader("💊 Medidas da Caixa de Remédio (B)")
nome_b = st.text_input("Nome do Produto", value="Medicamento X")
c1, c2, c3 = st.columns(3)
lb = c1.number_input("Largura B (cm)", min_value=0.1, value=3.0, step=0.1)
pb = c2.number_input("Profundidade B (cm)", min_value=0.1, value=5.0, step=0.1)
ab = c3.number_input("Altura B (cm) - Eixo Vertical", min_value=0.1, value=10.0, step=0.1)

if st.button("CALCULAR CAPACIDADE MÁXIMA", type="primary", use_container_width=True):
    # Cálculo considerando a altura fixa (caixa em pé)
    # Testamos apenas a rotação da base (X e Y)
    
    # Opção 1: Largura B alinhada com Largura A
    n1_l = la // lb
    n1_p = pa // pb
    n1_a = aa // ab # Verifica se cabe uma em cima da outra "em pé"
    total1 = int(n1_l * n1_p * n1_a)
    
    # Opção 2: Girar a base (Profundidade B alinhada com Largura A)
    n2_l = la // pb
    n2_p = pa // lb
    n2_a = aa // ab
    total2 = int(n2_l * n2_p * n2_a)

    # Resultado Final
    if total1 >= total2:
        res_total = total1
        posicao = "Frente da Caixa B voltada para a Frente da Caixa A"
        sobra_l = la - (n1_l * lb)
        sobra_p = pa - (n1_p * pb)
    else:
        res_total = total2
        posicao = "Girar a Caixa B (Lateral voltada para a Frente)"
        sobra_l = la - (n2_l * pb)
        sobra_p = pa - (n2_p * lb)

    if res_total > 0:
        st.success(f"### ✅ Resultado: Cabem {res_total} unidades!")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.write(f"**Organização:** {posicao}")
            st.write(f"**Camadas Verticais:** {int(aa // ab)} nível(is)")
        with col_res2:
            vol_util = (res_total * (lb * pb * ab)) / (la * pa * aa) * 100
            st.write(f"**Aproveitamento:** {vol_util:.1f}%")
            st.write(f"**Folga lateral:** {sobra_l:.1f} cm")
            
        st.info(f"Dica: Organize em {int(la // (lb if total1>=total2 else pb))} fileiras ao longo da profundidade.")
    else:
        st.error("❌ O remédio é maior que a Caixa A ou a altura excede o limite.")

