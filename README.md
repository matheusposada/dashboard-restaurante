# 🍝 Dashboard de Vendas — Cantina Italiana

Dashboard interativo de análise de vendas e lucratividade para restaurante, desenvolvido em Python com Streamlit e Plotly.

## 📊 Funcionalidades

- **KPIs em tempo real**: Receita total, lucro, ticket médio por mesa e itens vendidos
- **Evolução mensal**: Gráfico combinado de receita (linha) e lucro (barras)
- **Receita por categoria**: Pizza/Massa/Carne/Bebida/Sobremesa
- **Ranking de produtos**: Top 8 itens por receita
- **Formas de pagamento**: Distribuição por método (Pix, Cartão, Dinheiro)
- **Margem por categoria**: Comparativo de rentabilidade
- **Filtros dinâmicos**: Por período (mês) e categoria de produto
- **Tabela detalhada**: Resumo por produto com receita, lucro e margem

## 🛠️ Tecnologias

| Biblioteca | Uso |
|---|---|
| `pandas` | Leitura e processamento dos dados |
| `plotly` | Gráficos interativos |
| `streamlit` | Interface web do dashboard |

## 🚀 Como rodar localmente

### 1. Clone o repositório
```bash
git clone https://github.com/matheusposada/dashboard-restaurante
cd dashboard-restaurante
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute o dashboard
```bash
streamlit run app.py
```

O dashboard abrirá automaticamente em `http://localhost:8501`

## 📁 Estrutura do projeto

```
dashboard-restaurante/
│
├── app.py              # Aplicação principal (Streamlit)
├── requirements.txt    # Dependências do projeto
├── README.md           # Este arquivo
│
└── data/
    └── vendas.csv      # Dataset de vendas (Jan–Jun 2024)
```

## 📂 Estrutura dos dados (`vendas.csv`)

| Coluna | Tipo | Descrição |
|---|---|---|
| `data` | date | Data da venda |
| `categoria` | string | Categoria do produto |
| `produto` | string | Nome do produto |
| `quantidade` | int | Quantidade vendida |
| `preco_unitario` | float | Preço de venda (R$) |
| `custo_unitario` | float | Custo do item (R$) |
| `mesa` | int | Número da mesa |
| `forma_pagamento` | string | Método de pagamento |

## 💡 Contexto

Este projeto foi desenvolvido como portfólio para a área de **Dados e Business Intelligence**, aplicando conceitos de ETL, análise exploratória e visualização de dados — conectando experiência real em gestão de restaurante com ferramentas modernas de análise em Python.

---

*Desenvolvido por [Matheus Posada](https://github.com/matheusposada)*
