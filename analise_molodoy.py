import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import streamlit as st
from PIL import Image
import os

# 🧠 Cartão Estatístico
def gerar_cartao_estatistico(df, img_path):
    player_img = mpimg.imread(img_path)

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

    ax.text(5, 9.5, "Cartão Estatístico - Danil 'molodoy' Golubenko",
            ha="center", va="center", fontsize=14, fontweight='bold')

    player_box = OffsetImage(player_img, zoom=0.25)
    ab_player = AnnotationBbox(player_box, (1.5, 6), frameon=False)
    ax.add_artist(ab_player)

    info = (
        "Nickname: molodoy\n"
        "Nome: Danil Golubenko\n"
        "Função: AWPer\n"
        "Idade: 20 anos\n"
        "Nacionalidade: Cazaquistão\n"
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
    ax.text(5, 0.5, "Desempenho baseado nas partidas da IEM Cologne 2025",
            fontsize=9, ha="center", color='gray')

    plt.tight_layout()
    plt.close(fig)
    return fig

# 📊 Gráfico de barras genérico
def grafico_barra(df, coluna, titulo, cor, ylabel, sufixo=""):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["mapa"], df[coluna], color=cor)
    ax.set_title(titulo)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Mapa")
    ax.set_ylim(0, df[coluna].max() * 1.2)

    for i, v in enumerate(df[coluna]):
        ax.text(i, v + (df[coluna].max() * 0.05), f"{v:.2f}{sufixo}", ha='center')

    plt.tight_layout()
    plt.close(fig)
    return fig

# 📉 Gráfico de diferença de kills
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
    plt.tight_layout()
    plt.close(fig)
    return fig

# 🚀 App principal
def main():
    st.set_page_config(layout="wide")
    st.title("📊 Dashboard - Desempenho do jogador molodoy")

    # 📥 Carregar e preparar dados
    df = pd.read_csv("molodoy_partidas.csv", sep=";", encoding="latin1")
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)
    df["kast"] = df["kast"].astype(str).str.replace('%', '').astype(float)
    df["kd_ratio"] = (df["kills"] / df["deaths"]).round(2)
    df["kd_diff"] = df["kills"] - df["deaths"]

    # 📇 Cartão
    st.subheader("📇 Cartão Estatístico")
    st.pyplot(gerar_cartao_estatistico(df, "images/molodoy.png"), use_container_width=True)

    # 📊 Agregação por mapa
    df_agg = df.groupby("mapa").agg({
        "kd_ratio": "mean",
        "rating": "mean",
        "adr": "mean",
        "kast": "mean",
        "kd_diff": "sum"
    }).reset_index()

    # 📈 Análises
    st.subheader("📈 Análises por Mapa")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(grafico_barra(df_agg, "kd_ratio", "KD Ratio por Mapa", "skyblue", "KD Ratio"), use_container_width=True)
    with col2:
        st.pyplot(grafico_barra(df_agg, "rating", "Rating HLTV por Mapa", "lightgreen", "Rating"), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.pyplot(grafico_barra(df_agg, "adr", "ADR por Mapa", "orange", "Dano Médio por Round (ADR)"), use_container_width=True)
    with col4:
        st.pyplot(grafico_barra(df_agg, "kast", "KAST (%) por Mapa", "purple", "KAST (%)", sufixo="%"), use_container_width=True)

    # 📉 Diferença de Kills
    st.subheader("📉 Diferença de Kills")
    st.pyplot(grafico_kd_diff(df_agg), use_container_width=True)

    # 📋 Dados brutos
    st.subheader("📋 Dados brutos")
    st.dataframe(df)

    # 📅 Resultados com logos e nomes
    st.subheader("📅 Resultados das Séries (IEM Cologne 2025)")
    resultados_df = pd.read_csv("resultados_series.csv")
    resultados_df["cor"] = resultados_df["resultado"].apply(
        lambda r: "#2ecc71" if r.startswith("2") else "#e74c3c"
    )

    logos = {
        "FURIA": "images/furia_logo.png",
        "G2": "images/g2_logo.png",
        "Astralis": "images/astralis_logo.png",
        "Falcons": "images/falcons_logo.png",
        "MOUZ": "images/mouz_logo.png"
    }

    for _, row in resultados_df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])

        time1_logo = Image.open(logos.get(row["time"]))
        time2_logo = Image.open(logos.get(row["oponente"]))
        cor_resultado = row["cor"]

        with col1:
            st.image(time1_logo, width=30)
        with col2:
            st.markdown(f"<h5 style='color:white'>{row['time']}</h5>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<h5 style='color:{cor_resultado}'>{row['resultado']}</h5>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<h5 style='color:white'>{row['oponente']}</h5>", unsafe_allow_html=True)
        with col5:
            st.image(time2_logo, width=30)

if __name__ == "__main__":
    main()
