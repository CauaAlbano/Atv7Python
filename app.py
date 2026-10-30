import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from scipy import stats

st.set_page_config(
    page_title="Dashboard — Atividade 06",
    layout="wide"
)

sns.set_theme(style="whitegrid")

with st.sidebar:
    st.title("Informações do Aluno")
    st.markdown("---")


    nome = "Cauã Albano de Sousa Kamei"
    numero_chamada = "08"
    turma = "3b2"

    st.markdown(f"**Nome:** {nome}")
    st.markdown(f"**Número da chamada:** {numero_chamada}")
    st.markdown(f"**Turma:** {turma}")

# ============================================================
# FUNÇÕES DE GRÁFICOS (uma para cada tipo)
# ============================================================

# ---------- 1. DISPERSÃO ----------
def grafico_dispersao():
    df = pd.read_csv("dados_dispersao.csv")
    fem = df[df["sexo"] == "Feminino"]
    masc = df[df["sexo"] == "Masculino"]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(fem["altura_cm"], fem["peso_kg"], color="crimson",
               alpha=0.7, label="Feminino", edgecolor="black", s=60)
    ax.scatter(masc["altura_cm"], masc["peso_kg"], color="steelblue",
               alpha=0.7, label="Masculino", edgecolor="black", s=60)
    ax.set_title("Dispersão: Altura × Peso por Sexo", fontweight="bold")
    ax.set_xlabel("Altura (cm)")
    ax.set_ylabel("Peso (kg)")
    ax.legend()
    plt.tight_layout()
    return fig

# ---------- 2. DISTRIBUIÇÃO ----------
def grafico_distribuicao():
    df = pd.read_csv("dados_distribuicao.csv")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data=df, x="idade", bins=15, kde=True,
                 color="steelblue", edgecolor="black", alpha=0.7, ax=ax)
    media = df["idade"].mean()
    mediana = df["idade"].median()
    ax.axvline(media, color="crimson", linestyle="--", linewidth=2,
               label=f"Média = {media:.1f}")
    ax.axvline(mediana, color="darkgreen", linestyle=":", linewidth=2,
               label=f"Mediana = {mediana:.1f}")
    ax.set_title("Distribuição das Idades dos Clientes", fontweight="bold")
    ax.set_xlabel("Idade (anos)")
    ax.set_ylabel("Frequência")
    ax.legend()
    plt.tight_layout()
    return fig

# ---------- 3. FREQUÊNCIA ----------
def grafico_frequencia():
    df = pd.read_csv("dados_frequencia.csv")
    freq = df["tipo_atendimento"].value_counts()
    percentuais = (freq / freq.sum() * 100).round(1)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=freq.values, y=freq.index, hue=freq.index,
                palette="viridis", legend=False, edgecolor="black", ax=ax)
    for i, (v, p) in enumerate(zip(freq.values, percentuais.values)):
        ax.text(v + 1, i, f"{v} ({p}%)", va="center", fontsize=10)
    ax.set_title("Frequência dos Tipos de Atendimento", fontweight="bold")
    ax.set_xlabel("Número de chamados")
    ax.set_ylabel("")
    ax.set_xlim(0, freq.max() * 1.18)
    plt.tight_layout()
    return fig

# ---------- 4. HEATMAP ----------
def grafico_heatmap():
    df = pd.read_csv("dados_heatmap.csv")
    pivot = df.pivot(index="dia_semana", columns="horario",
                     values="movimento_clientes")
    ordem = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    pivot = pivot.reindex(ordem)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(pivot, annot=True, fmt="d", cmap="YlOrRd",
                linewidths=0.5, linecolor="white",
                cbar_kws={"label": "Nº de clientes"}, ax=ax)
    ax.set_title("Movimento por Dia e Horário", fontweight="bold")
    ax.set_xlabel("Horário")
    ax.set_ylabel("")
    plt.tight_layout()
    return fig

# ---------- 5. LINHAS ----------
def grafico_linhas():
    df = pd.read_csv("dados_linhas.csv", parse_dates=["data"])
    df = df.sort_values("data")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=df, x="data", y="vendas", hue="loja",
                 marker="o", markersize=4, linewidth=1.5, ax=ax)
    df["mm7"] = df.groupby("loja")["vendas"].transform(
        lambda s: s.rolling(7).mean())
    for loja, grupo in df.groupby("loja"):
        ax.plot(grupo["data"], grupo["mm7"], linestyle="--",
                linewidth=2, alpha=0.9, label=f"{loja} (MM7)")
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    plt.xticks(rotation=45, ha="right")
    ax.set_title("Evolução das Vendas Diárias", fontweight="bold")
    ax.set_xlabel("Data")
    ax.set_ylabel("Vendas (R$)")
    ax.legend(fontsize=8)
    plt.tight_layout()
    return fig

# ---------- 6. PIZZA ----------
def grafico_pizza():
    df = pd.read_csv("dados_pizza.csv")
    df = df.sort_values("faturamento", ascending=False).reset_index(drop=True)
    cores = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#6A994E"]
    explode = [0.06] + [0] * (len(df) - 1)

    fig, ax = plt.subplots(figsize=(8, 5))
    wedges, texts, autotexts = ax.pie(
        df["faturamento"], labels=df["canal_venda"], colors=cores,
        autopct=lambda p: f"{p:.1f}%", startangle=90, counterclock=False,
        explode=explode, wedgeprops={"edgecolor": "white", "linewidth": 2},
        textprops={"fontsize": 10})
    for at in autotexts:
        at.set_color("white")
        at.set_fontweight("bold")
    total = df["faturamento"].sum()
    ax.set_title(f"Faturamento por Canal\nTotal: R$ {total:,.0f}", fontweight="bold")
    legendas = [f"{c}: R$ {f:,.0f}" for c, f in zip(df["canal_venda"], df["faturamento"])]
    ax.legend(wedges, legendas, loc="center left",
              bbox_to_anchor=(1.0, 0.5), fontsize=8)
    plt.tight_layout()
    return fig

# ---------- 7. REGRESSÃO ----------
def grafico_regressao():
    df = pd.read_csv("dados_regressao.csv")
    res = stats.linregress(df["renda_mensal"], df["gasto_mensal"])
    a, b, r = res.intercept, res.slope, res.rvalue
    r2 = r ** 2

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x="renda_mensal", y="gasto_mensal",
                    color="steelblue", alpha=0.7, s=50,
                    edgecolor="black", ax=ax, label="Clientes")
    x_vals = np.linspace(df["renda_mensal"].min(), df["renda_mensal"].max(), 100)
    ax.plot(x_vals, a + b * x_vals, color="crimson", linewidth=2.5,
            label=f"y = {a:.0f} + {b:.3f}·x")
    ax.text(0.05, 0.95, f"R² = {r2:.4f}", transform=ax.transAxes,
            fontsize=11, va="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.85))
    ax.set_title("Regressão: Gasto × Renda", fontweight="bold")
    ax.set_xlabel("Renda mensal (R$)")
    ax.set_ylabel("Gasto mensal (R$)")
    ax.legend(loc="lower right", fontsize=8)
    plt.tight_layout()
    return fig

# ---------- 8. BARRAS AGRUPADAS ----------
def grafico_barras():
    df = pd.read_csv("dados_barras.csv")
    ordem = (df.groupby("categoria")["vendas_medias"]
               .mean().sort_values(ascending=False).index)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=df, x="categoria", y="vendas_medias", hue="regiao",
                order=ordem, palette="Set2", edgecolor="black",
                linewidth=0.8, ax=ax)
    ax.set_title("Vendas Médias por Categoria e Região", fontweight="bold")
    ax.set_xlabel("Categoria")
    ax.set_ylabel("Vendas médias (R$)")
    ax.legend(title="Região", loc="upper left",
              bbox_to_anchor=(1.0, 1.0), fontsize=8)
    plt.setp(ax.get_xticklabels(), rotation=15, ha="right")
    plt.tight_layout()
    return fig

# ---------- 9. BOXPLOT ----------
def grafico_boxplot():
    df = pd.read_csv("dados_boxplot.csv")
    ordem = (df.groupby("departamento")["salario"]
               .median().sort_values(ascending=False).index)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="departamento", y="salario", order=ordem,
                palette="Set3", width=0.6, linewidth=1.5,
                flierprops=dict(marker="o", markerfacecolor="crimson",
                                markeredgecolor="black", markersize=6,
                                alpha=0.8), ax=ax)
    sns.stripplot(data=df, x="departamento", y="salario", order=ordem,
                  color="black", alpha=0.3, size=3, jitter=True, ax=ax)
    ax.set_title("Distribuição Salarial por Departamento", fontweight="bold")
    ax.set_xlabel("Departamento")
    ax.set_ylabel("Salário mensal (R$)")
    plt.tight_layout()
    return fig

graficos = [
    {
        "titulo": "1. Dispersão — Altura × Peso",
        "funcao": grafico_dispersao,
        "analise": (
            "Há uma tendência positiva clara: pessoas mais altas tendem a pesar mais. "
            "Os grupos feminino e masculino se sobrepõem bastante na faixa de 160–180 cm, "
            "mas o masculino concentra os maiores pesos. Destacam-se outliers como uma mulher "
            "com ~193 cm e um homem com 145 cm. A dispersão sugere correlação positiva forte, "
            "que será quantificada no gráfico de regressão."
        )
    },
    {
        "titulo": "2. Distribuição — Idades dos Clientes",
        "funcao": grafico_distribuicao,
        "analise": (
            "A distribuição é claramente bimodal: há um pico entre 18–32 anos e outro entre 33–55 anos, "
            "com uma queda no meio. A média (~35 anos) cai justamente no vale entre os dois grupos, "
            "não representando nenhum cliente típico. A mediana é mais robusta aqui. Esse padrão "
            "sugere que a base de clientes é composta por dois segmentos distintos, o que pode "
            "orientar estratégias de marketing separadas."
        )
    },
    {
        "titulo": "3. Frequência — Tipos de Atendimento",
        "funcao": grafico_frequencia,
        "analise": (
            "Dúvida é a categoria mais frequente (~38%), seguida de Reclamação (~29%). Juntas, "
            "representam cerca de 67% dos chamados — um sinal de atrito com o cliente. "
            "Cancelamento (~9%) é a categoria mais crítica em termos de receita perdida. "
            "Elogio é a menor (~8%). A prioridade de ação é clara: investir em documentação "
            "e autoatendimento para reduzir Dúvidas, e investigar as causas das Reclamações."
        )
    },
    {
        "titulo": "4. Heatmap — Movimento por Dia e Horário",
        "funcao": grafico_heatmap,
        "analise": (
            "Fim de semana concentra os picos: Domingo 12:00 (199 clientes) e 18:00 (197) são os "
            "máximos. Quinta-feira é atipicamente fraca em todos os horários (exceto 20:00). "
            "O horário de almoço (12:00) é forte no fim de semana, mas fraco nos dias úteis. "
            "Esses padrões são valiosos para alocação de equipe e promoções segmentadas por dia/horário."
        )
    },
    {
        "titulo": "5. Linhas — Evolução das Vendas",
        "funcao": grafico_linhas,
        "analise": (
            "As vendas crescem de forma consistente e acelerada no trimestre: de ~R$ 100–150/dia "
            "em janeiro para ~R$ 200–260/dia em março. A média móvel de 7 dias revela a tendência "
            "sem o ruído semanal. Destaca-se uma anomalia em 16/03 (Loja B, R$ 185), muito abaixo "
            "dos vizinhos — vale investigar feriado, falta de estoque ou erro de registro."
        )
    },
    {
        "titulo": "6. Pizza — Faturamento por Canal",
        "funcao": grafico_pizza,
        "analise": (
            "Site (37,5%) e Loja Física (26,7%) dominam. Site + Aplicativo = 55% do faturamento, "
            "confirmando a força dos canais digitais. Telefone (6,7%) é o menor e provavelmente "
            "legado. A leitura é de 'parte de um todo': se o objetivo fosse comparar canais, "
            "barras seriam mais eficazes. Para decisão de investimento, porém, a pizza deixa claro "
            "onde está o volume."
        )
    },
    {
        "titulo": "7. Regressão — Gasto × Renda",
        "funcao": grafico_regressao,
        "analise": (
            "A relação é fortíssima: R² ≈ 0,93, ou seja, 93% da variação do gasto é explicada pela renda. "
            "A inclinação (~0,58) indica que cada R$ 1.000 a mais de renda gera ~R$ 580 a mais de gasto. "
            "O p-valor < 0,001 confirma significância estatística. Cuidado: correlação não implica "
            "causalidade. O outlier de renda ~R$ 2.900 e gasto ~R$ 2.830 (quase 100% da renda) "
            "merece investigação individual."
        )
    },
    {
        "titulo": "8. Barras Agrupadas — Vendas por Categoria e Região",
        "funcao": grafico_barras,
        "analise": (
            "Oeste é a região mais forte em 4 das 5 categorias (Roupas, Alimentos, Livros, Brinquedos), "
            "com média ~R$ 225. Leste lidera apenas em Eletrônicos (R$ 259), onde Sul tem o pior "
            "desempenho (R$ 73) — uma disparidade de 3,5×. Livros tem a maior média geral (R$ 187), "
            "puxada por Oeste (R$ 284). Esses padrões orientam expansão e mix de produto por região."
        )
    },
    {
        "titulo": "9. Boxplot — Salários por Departamento",
        "funcao": grafico_boxplot,
        "analise": (
            "Dois grupos claros: TI e Vendas têm medianas ~R$ 7.000; RH e Marketing ~R$ 4.100 "
            "(diferença de ~70%). TI e Vendas também são mais dispersos (IQR ~R$ 2.600–2.900), "
            "indicando trilhas de carreira mais amplas. Todos os departamentos têm outliers "
            "idênticos (19.600/21.000 em TI e Vendas; 11.200/12.000 em RH e Marketing), "
            "o que sugere dados sintéticos ou valores de diretoria incluídos na base. "
            "A equidade salarial entre funções merece análise de benchmarking externo."
        )
    },
]

st.title("Dashboard — Atividade 07")
st.markdown("Visualização dos 9 gráficos elaborados")
st.markdown("---")

for i in range(0, len(graficos), 3):
    bloco = graficos[i:i + 3]
    colunas = st.columns(3)

    for j, g in enumerate(bloco):
        with colunas[j]:
            st.subheader(g["titulo"])
            fig = g["funcao"]()
            st.pyplot(fig)
            plt.close(fig) 

    for g in bloco:
        with st.expander(f"Análise — {g['titulo']}", expanded=True):
            st.write(g["analise"])

    st.markdown("---")

