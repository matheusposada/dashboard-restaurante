import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard · Cantina Italiana",
    page_icon="🍝",
    layout="wide",
)

# ── Estilo customizado ──────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #1a1a18;
        color: #e8e0d0;
    }
    .main { background-color: #1a1a18; }

    /* Título principal */
    .titulo-principal {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        color: #e8c97e;
        margin-bottom: 0;
        line-height: 1.1;
    }
    .subtitulo {
        font-size: 0.9rem;
        color: #8a8070;
        margin-top: 4px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* Cards de KPI */
    .kpi-card {
        background: #252520;
        border: 1px solid #333328;
        border-left: 3px solid #e8c97e;
        border-radius: 6px;
        padding: 20px 24px;
        margin-bottom: 8px;
    }
    .kpi-label {
        font-size: 0.78rem;
        color: #8a8070;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-family: 'Playfair Display', serif;
        font-size: 1.9rem;
        color: #e8c97e;
        line-height: 1;
    }
    .kpi-delta {
        font-size: 0.8rem;
        margin-top: 6px;
    }
    .delta-pos { color: #6fcf97; }
    .delta-neg { color: #eb5757; }

    /* Divisor */
    hr { border-color: #333328; margin: 1.5rem 0; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #141412;
        border-right: 1px solid #333328;
    }
    section[data-testid="stSidebar"] * { color: #e8e0d0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Carregamento dos dados ──────────────────────────────────────────────────
@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/vendas.csv", parse_dates=["data"])
    df["receita"] = df["quantidade"] * df["preco_unitario"]
    df["custo"]   = df["quantidade"] * df["custo_unitario"]
    df["lucro"]   = df["receita"] - df["custo"]
    df["margem"]  = (df["lucro"] / df["receita"] * 100).round(1)
    df["mes"]     = df["data"].dt.to_period("M").astype(str)
    df["dia_semana"] = df["data"].dt.day_name()
    return df

df = carregar_dados()

# ── Sidebar: filtros ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🍝 Filtros")
    st.markdown("---")

    meses_disponiveis = sorted(df["mes"].unique())
    meses_sel = st.multiselect(
        "Período (mês)",
        options=meses_disponiveis,
        default=meses_disponiveis,
    )

    categorias_disponiveis = sorted(df["categoria"].unique())
    cats_sel = st.multiselect(
        "Categoria",
        options=categorias_disponiveis,
        default=categorias_disponiveis,
    )

    st.markdown("---")
    st.markdown("<small style='color:#8a8070'>Dados: Jan – Jun 2024</small>", unsafe_allow_html=True)

# ── Filtro aplicado ─────────────────────────────────────────────────────────
df_f = df[df["mes"].isin(meses_sel) & df["categoria"].isin(cats_sel)]

# ── Cabeçalho ───────────────────────────────────────────────────────────────
st.markdown('<p class="titulo-principal">Cantina Italiana</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">Dashboard de Vendas & Lucratividade · 2024</p>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── KPIs ────────────────────────────────────────────────────────────────────
receita_total  = df_f["receita"].sum()
lucro_total    = df_f["lucro"].sum()
margem_media   = df_f["margem"].mean()
ticket_medio   = df_f.groupby(["data","mesa"])["receita"].sum().mean()
total_itens    = df_f["quantidade"].sum()

# Variação mês a mês (último vs penúltimo mês selecionado)
receita_por_mes = df_f.groupby("mes")["receita"].sum()
if len(receita_por_mes) >= 2:
    delta_pct = ((receita_por_mes.iloc[-1] - receita_por_mes.iloc[-2]) / receita_por_mes.iloc[-2] * 100)
    delta_label = f"{'▲' if delta_pct >= 0 else '▼'} {abs(delta_pct):.1f}% vs mês anterior"
    delta_class = "delta-pos" if delta_pct >= 0 else "delta-neg"
else:
    delta_label, delta_class = "", "delta-pos"

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Receita Total</div>
        <div class="kpi-value">R$ {receita_total:,.0f}</div>
        <div class="kpi-delta {delta_class}">{delta_label}</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Lucro Total</div>
        <div class="kpi-value">R$ {lucro_total:,.0f}</div>
        <div class="kpi-delta delta-pos">Margem média: {margem_media:.1f}%</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Ticket Médio / Mesa</div>
        <div class="kpi-value">R$ {ticket_medio:,.0f}</div>
        <div class="kpi-delta" style="color:#8a8070">por visita</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Itens Vendidos</div>
        <div class="kpi-value">{total_itens:,}</div>
        <div class="kpi-delta" style="color:#8a8070">no período selecionado</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Gráfico 1: Receita mensal (linha) + Lucro (barra) ─────────────────────
col_a, col_b = st.columns([3, 2])

with col_a:
    st.markdown("#### Evolução Mensal — Receita & Lucro")
    mensal = df_f.groupby("mes")[["receita","lucro"]].sum().reset_index()

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=mensal["mes"], y=mensal["lucro"],
        name="Lucro", marker_color="#4a7c59", opacity=0.85
    ))
    fig1.add_trace(go.Scatter(
        x=mensal["mes"], y=mensal["receita"],
        name="Receita", mode="lines+markers",
        line=dict(color="#e8c97e", width=2.5),
        marker=dict(size=7, color="#e8c97e")
    ))
    fig1.update_layout(
        plot_bgcolor="#1a1a18", paper_bgcolor="#1a1a18",
        font_color="#e8e0d0", legend=dict(orientation="h", y=1.1),
        xaxis=dict(gridcolor="#2a2a25"), yaxis=dict(gridcolor="#2a2a25"),
        margin=dict(t=10, b=10), height=280,
    )
    st.plotly_chart(fig1, use_container_width=True)

# ── Gráfico 2: Receita por categoria (rosca) ───────────────────────────────
with col_b:
    st.markdown("#### Receita por Categoria")
    por_cat = df_f.groupby("categoria")["receita"].sum().reset_index()

    CORES = ["#e8c97e","#c4773b","#6fcf97","#4a7c59","#8a8070"]
    fig2 = px.pie(
        por_cat, names="categoria", values="receita",
        hole=0.55, color_discrete_sequence=CORES
    )
    fig2.update_traces(textposition="outside", textfont_color="#e8e0d0")
    fig2.update_layout(
        plot_bgcolor="#1a1a18", paper_bgcolor="#1a1a18",
        font_color="#e8e0d0", showlegend=True,
        legend=dict(orientation="v", font_size=12),
        margin=dict(t=10, b=10), height=280,
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Gráfico 3: Top produtos por receita ────────────────────────────────────
col_c, col_d = st.columns([2, 3])

with col_c:
    st.markdown("#### Top 8 Produtos por Receita")
    por_prod = (
        df_f.groupby("produto")["receita"].sum()
        .sort_values(ascending=True).tail(8).reset_index()
    )
    fig3 = px.bar(
        por_prod, x="receita", y="produto", orientation="h",
        color="receita", color_continuous_scale=["#333328","#e8c97e"]
    )
    fig3.update_layout(
        plot_bgcolor="#1a1a18", paper_bgcolor="#1a1a18",
        font_color="#e8e0d0", coloraxis_showscale=False,
        xaxis=dict(gridcolor="#2a2a25"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        margin=dict(t=10, b=10), height=300,
    )
    st.plotly_chart(fig3, use_container_width=True)

# ── Gráfico 4: Formas de pagamento ─────────────────────────────────────────
with col_d:
    st.markdown("#### Formas de Pagamento & Margem por Categoria")

    tab1, tab2 = st.tabs(["Pagamento", "Margem"])

    with tab1:
        por_pag = df_f.groupby("forma_pagamento")["receita"].sum().reset_index()
        fig4 = px.bar(
            por_pag.sort_values("receita", ascending=False),
            x="forma_pagamento", y="receita",
            color="forma_pagamento", color_discrete_sequence=CORES,
            labels={"forma_pagamento": "", "receita": "Receita (R$)"}
        )
        fig4.update_layout(
            plot_bgcolor="#1a1a18", paper_bgcolor="#1a1a18",
            font_color="#e8e0d0", showlegend=False,
            xaxis=dict(gridcolor="#2a2a25"), yaxis=dict(gridcolor="#2a2a25"),
            margin=dict(t=10, b=10), height=240,
        )
        st.plotly_chart(fig4, use_container_width=True)

    with tab2:
        margem_cat = df_f.groupby("categoria")["margem"].mean().reset_index()
        fig5 = px.bar(
            margem_cat.sort_values("margem", ascending=False),
            x="categoria", y="margem",
            color="margem", color_continuous_scale=["#c4773b","#6fcf97"],
            labels={"categoria": "", "margem": "Margem (%)"}
        )
        fig5.update_layout(
            plot_bgcolor="#1a1a18", paper_bgcolor="#1a1a18",
            font_color="#e8e0d0", coloraxis_showscale=False,
            xaxis=dict(gridcolor="#2a2a25"), yaxis=dict(gridcolor="#2a2a25"),
            margin=dict(t=10, b=10), height=240,
        )
        st.plotly_chart(fig5, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Tabela detalhada ────────────────────────────────────────────────────────
with st.expander("📋 Ver dados detalhados por produto"):
    resumo = df_f.groupby(["categoria","produto"]).agg(
        Qtd_Vendida=("quantidade","sum"),
        Receita=("receita","sum"),
        Lucro=("lucro","sum"),
        Margem_Pct=("margem","mean"),
    ).round(1).reset_index()
    resumo["Receita"] = resumo["Receita"].apply(lambda x: f"R$ {x:,.2f}")
    resumo["Lucro"]   = resumo["Lucro"].apply(lambda x: f"R$ {x:,.2f}")
    resumo["Margem_Pct"] = resumo["Margem_Pct"].apply(lambda x: f"{x:.1f}%")
    st.dataframe(resumo, use_container_width=True, hide_index=True)

st.markdown("<br><small style='color:#333328'>Dashboard desenvolvido com Python · Pandas · Plotly · Streamlit</small>", unsafe_allow_html=True)
