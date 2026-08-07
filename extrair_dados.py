from seleniumbase import SB
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import time
import os

URL_STATS = "https://fbref.com/en/comps/24/2025/2025-Serie-A-Stats"
URL_PLAYERS = "https://fbref.com/en/comps/24/2025/stats/2025-Serie-A-Stats"
URL_SCHEDULE = "https://fbref.com/en/comps/24/2025/schedule/2025-Serie-A-Scores-and-Fixtures"


def get_page_html(sb, url):
    sb.uc_open_with_reconnect(url, reconnect_time=10)
    return sb.get_page_source()


def scrape_classificacao(html):
    dfs = pd.read_html(StringIO(html), attrs={"id": "results2025241_overall"})
    if not dfs:
        return pd.DataFrame()
    df = dfs[0]
    df = df[["Rk", "Squad", "MP", "W", "D", "L", "GF", "GA", "GD", "Pts"]]
    df.columns = ["Posicao", "Time", "J", "V", "E", "D", "GP", "GC", "SG", "Pts"]
    return df


def scrape_desempenho(html):
    dfs = pd.read_html(StringIO(html), attrs={"id": "results2025241_home_away"})
    if not dfs:
        return pd.DataFrame()
    df = dfs[0]

    home = pd.DataFrame({
        "Time": df[("Unnamed: 1_level_0", "Squad")],
        "J_Casa": df[("Home", "MP")],
        "V_Casa": df[("Home", "W")],
        "E_Casa": df[("Home", "D")],
        "D_Casa": df[("Home", "L")],
        "GP_Casa": df[("Home", "GF")],
        "GC_Casa": df[("Home", "GA")],
    })

    away = pd.DataFrame({
        "Time": df[("Unnamed: 1_level_0", "Squad")],
        "J_Fora": df[("Away", "MP")],
        "V_Fora": df[("Away", "W")],
        "E_Fora": df[("Away", "D")],
        "D_Fora": df[("Away", "L")],
        "GP_Fora": df[("Away", "GF")],
        "GC_Fora": df[("Away", "GA")],
    })

    result = home.merge(away, on="Time")
    return result


def scrape_jogadores(html):
    dfs = pd.read_html(StringIO(html), attrs={"id": "stats_standard"})
    if not dfs:
        return pd.DataFrame()
    df = dfs[0]

    jogadores = pd.DataFrame({
        "Jogador": df[("Unnamed: 1_level_0", "Player")],
        "Time": df[("Unnamed: 4_level_0", "Squad")],
        "Pos": df[("Unnamed: 3_level_0", "Pos")],
        "Gols": pd.to_numeric(df[("Performance", "Gls")], errors="coerce"),
        "Assistencias": pd.to_numeric(df[("Performance", "Ast")], errors="coerce"),
    })

    jogadores = jogadores.dropna(subset=["Gols", "Assistencias"])

    top_gols = (
        jogadores.sort_values(["Time", "Gols"], ascending=[True, False])
        .groupby("Time")
        .head(3)
        .assign(Tipo="Artilheiro")
    )

    top_asts = (
        jogadores.sort_values(["Time", "Assistencias"], ascending=[True, False])
        .groupby("Time")
        .head(3)
        .assign(Tipo="Assistente")
    )

    return pd.concat([top_gols, top_asts], ignore_index=True)


def scrape_cartoes(html):
    dfs = pd.read_html(StringIO(html), attrs={"id": "stats_squads_misc_for"})
    if not dfs:
        return pd.DataFrame()
    df = dfs[0]
    cartoes = pd.DataFrame({
        "Time": df[("Unnamed: 0_level_0", "Squad")],
        "Amarelos": pd.to_numeric(df[("Performance", "CrdY")], errors="coerce"),
        "Vermelhos": pd.to_numeric(df[("Performance", "CrdR")], errors="coerce"),
    })
    return cartoes


def scrape_rodadas(html):
    dfs = pd.read_html(StringIO(html), attrs={"id": "sched_2025_24_1"})
    if not dfs:
        return pd.DataFrame()
    df = dfs[0]

    rodadas = pd.DataFrame({
        "Rodada": df["Wk"],
        "Data": df["Date"],
        "Casa": df["Home"],
        "Placar": df["Score"],
        "Fora": df["Away"],
    })
    rodadas = rodadas.dropna(subset=["Placar"])
    return rodadas


def main():
    pass

    print("=" * 60)
    print("  SCRAPING BRASILEIRAO SERIE A 2025 — FBref")
    print("=" * 60)

    with SB(uc=True, headless=True) as sb:
        print("\n[1/4] Acessando stats gerais...")
        html_stats = get_page_html(sb, URL_STATS)
        time.sleep(2)

        print("  Classificacao...")
        df_class = scrape_classificacao(html_stats)

        print("  Cartoes (amarelos/vermelhos)...")
        df_cartoes = scrape_cartoes(html_stats)
        df_class = df_class.merge(df_cartoes, on="Time", how="left")

        df_class.to_csv("classificacao.csv", index=False, encoding="utf-8-sig")
        print(f"  OK classificacao.csv ({len(df_class)} times)")

        print("  Desempenho casa/fora...")
        df_desempenho = scrape_desempenho(html_stats)
        df_desempenho.to_csv("desempenho.csv", index=False, encoding="utf-8-sig")
        print(f"  OK desempenho.csv ({len(df_desempenho)} registros)")

        print("\n[2/4] Acessando stats de jogadores...")
        html_players = get_page_html(sb, URL_PLAYERS)
        time.sleep(2)

        print("  Jogadores (top 3 gols + assistencias por time)...")
        df_jogadores = scrape_jogadores(html_players)
        df_jogadores.to_csv("jogadores.csv", index=False, encoding="utf-8-sig")
        print(f"  OK jogadores.csv ({len(df_jogadores)} registros)")

        print("\n[3/4] Acessando schedule (rodadas)...")
        html_sched = get_page_html(sb, URL_SCHEDULE)
        time.sleep(2)

        print("  Rodadas...")
        df_rodadas = scrape_rodadas(html_sched)
        df_rodadas.to_csv("rodadas.csv", index=False, encoding="utf-8-sig")
        print(f"  OK rodadas.csv ({len(df_rodadas)} partidas)")

    print("\n" + "=" * 60)
    print("  TODOS OS CSVs GERADOS")
    print("=" * 60)


if __name__ == "__main__":
    main()
