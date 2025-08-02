import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import streamlit as st

# 📥 Carrega imagem do jogador
player_img = mpimg.imread("molodoy.png")

# 🧮 Função do cartão estatístico
def gerar_cartao_estatistico(df):
    total_partidas = len(df)
    vitorias = (df["vitoria"] == "S").sum()
    winrate = (vitorias / total_partidas) * 100
    media_rating = df["rating"].mean()
    media_adr = df["adr"].mean()
    media_kd_ratio = (df["kills"] / df["deaths"]).mean()
    melhor_mapa = df.loc[df["rating"].idxmax(), "mapa"]
    melhor_rating = df["rating"].max()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    ax.text(5, 9.5, "Cartão Estatístico - Danil 'molodoy' Golubenko", ha="center", va="center", fontsize=14, fontweight='bold')

    # Foto
    player_box = OffsetImage(player_img, zoom=0.25)
    ab_player = AnnotationBbox(player_box, (1.5, 6), frameon=False)
    ax.add_artist(ab_player)

    info = (
        "Nacionalidade: Cazaquistão\n"
        "Idade: 20 anos\n"
        "Time: FURIA\n"
        "Evento: IEM Cologne 2025"
    )
    ax.text(0.5, 4.3, info, fontsize=11, va="top")

    stats = (
        f"Partidas: {total_partidas}\n"
        f"Vitórias: {vitorias} ({winrate:.1f}%)\n"
        f"Média de Rating: {media_rating:.2f}\n"
        f"Média de ADR: {media_adr:.1f}\n"
        f"K/D Ratio Médio: {media_kd_ratio:.2f}\n"
        f"Melhor mapa: {melhor_mapa} (Rating {melhor_rating:.2f})"
    )
    ax.text(5.5, 8, stats, fontsize=11, va="top")

    ax.text(5, 0.5, "Desempenho baseado nas partidas da IEM Cologne 2025", fontsize=9, ha="center", color='gray')

    return fig

# 📊 Funções de gráficos
def grafico_kd_ratio(df):
    df["kd_ratio"] = df["kills"] / df["deaths"]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["mapa"], df["kd_ratio"], color='skyblue')
    ax.set_title("KD Ratio por Mapa")
    ax.set_ylabel("KD Ratio")
    ax.set_xlabel("Mapa")
    ax.set_ylim(0, max(df["kd_ratio"]) + 0.5)
    for i, v in enumerate(df["kd_ratio"]):
        ax.text(i, v + 0.05, f"{v:.2f}", ha='center')
    return fig

def grafico_rating(df):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["mapa"], df["rating"], color='lightgreen')
    ax.set_title("Rating HLTV por Mapa")
    ax.set_ylabel("Rating")
    ax.set_xlabel("Mapa")
    ax.set_ylim(0, max(df["rating"]) + 0.5)
    for i, v in enumerate(df["rating"]):
        ax.text(i, v + 0.05, f"{v:.2f}", ha='center')
    return fig

def grafico_adr(df):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["mapa"], df["adr"], color='orange')
    ax.set_title("ADR por Mapa")
    ax.set_ylabel("Dano Médio por Round (ADR)")
    ax.set_xlabel("Mapa")
    ax.set_ylim(0, max(df["adr"]) + 10)
    for i, v in enumerate(df["adr"]):
        ax.text(i, v + 1, f"{v:.1f}", ha='center')
    return fig

def grafico_kast(df):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["mapa"], df["kast"], color='purple')
    ax.set_title("KAST (%) por Mapa")
    ax.set_ylabel("KAST (%)")
    ax.set_xlabel("Mapa")
    ax.set_ylim(0, max(df["kast"]) + 10)
    for i, v in enumerate(df["kast"]):
        ax.text(i, v + 1, f"{v:.1f}%", ha='center')
    return fig

def grafico_kd_diff(df):
    colors = ['green' if v >= 0 else 'red' for v in df["kd_diff"]]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["mapa"], df["kd_diff"], color=colors)
    ax.set_title("Diferença de Kills (K - D) por Mapa")
    ax.set_ylabel("Kills - Deaths")
    ax.set_xlabel("Mapa")
    ax.axhline(0, color='black', linestyle='--')
    for i, v in enumerate(df["kd_diff"]):
        ax.text(i, v + (1 if v >= 0 else -2), f"{v}", ha='center')
    return fig

# 🚀 Streamlit App
def main():
    st.set_page_config(layout="wide")
    st.title("📊 Dashboard - Desempenho do jogador molodoy")
    df = pd.read_csv("molodoy_partidas.csv", sep=";", encoding="latin1")
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)
    df["kast"] = df["kast"].astype(str).str.replace('%', '').astype(float)

    st.subheader("📇 Cartão Estatístico")
    st.pyplot(gerar_cartao_estatistico(df))

    st.subheader("📈 Análises por Mapa")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(grafico_kd_ratio(df))
    with col2:
        st.pyplot(grafico_rating(df))
    col3, col4 = st.columns(2)
    with col3:
        st.pyplot(grafico_adr(df))
    with col4:
        st.pyplot(grafico_kast(df))

    st.subheader("📉 Diferença de Kills")
    st.pyplot(grafico_kd_diff(df))

    st.subheader("📋 Dados brutos")
    st.dataframe(df)

if __name__ == "__main__":
    main()
