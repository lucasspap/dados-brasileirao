# Análise do Brasileirão Série A 2025

Projeto de coleta e análise de dados do Campeonato Brasileiro Série A 2025, com foco em visualização interativa no Power BI.

## Fonte de dados

Todos os dados são coletados do [FBref](https://fbref.com) via web scraping.

## Tecnologias utilizadas

- **Python 3.10+** — linguagem principal
- **SeleniumBase** (UC Mode) — bypass do Cloudflare para acessar o FBref
- **BeautifulSoup4** — parsing do HTML
- **Pandas** — manipulação de dados
- **Power BI** — construção do dashboard interativo

## Estrutura do projeto

```
dados-brasileirao/
├── classificacao.csv        # Classificação geral + cartões
├── desempenho.csv           # Desempenho dentro e fora de casa
├── jogadores.csv            # Top 3 artilheiros e assistentes por time
├── rodadas.csv              # Resultados de todas as rodadas
├── extrair_dados.py         # Script de scraping
├── .gitignore
├── requirements.txt
└── README.md
```

## Como rodar

### 1. Pré-requisitos

- Python 3.10+
- Google Chrome instalado

### 2. Configurar ambiente virtual

```bash
cd dados-brasileirao
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o scraping

```bash
python extrair_dados.py
```

Os 4 CSVs serão gerados na pasta do projeto.

## Arquivos gerados

| Arquivo | Conteúdo |
|---------|----------|
| `classificacao.csv` | Posição, time, jogos, vitórias, empates, derrotas, gols, saldo, pontos, amarelos, vermelhos |
| `desempenho.csv` | Jogos, vitórias, empates, derrotas, gols sofridos/feitos — dentro e fora de casa |
| `jogadores.csv` | Top 3 goleadores e top 3 assistentes de cada time |
| `rodadas.csv` | Rodada, data, time da casa, placar, time de fora |

## Dashboard interativo no Power BI

O dashboard inclui:

- **Tabela de classificação** — clicável para selecionar time
- **Perfil do time** — desempenho casa/fora, cartões, artilheiros e assistentes
- **Gráfico de linha** — evolução da posição ao longo das rodadas

## Notas

- O scraping utiliza SeleniumBase com ChromeDriver stealth para contornar a proteção Cloudflare do FBref, devido a diversos erros 403.

