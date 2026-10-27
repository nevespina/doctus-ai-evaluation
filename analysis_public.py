"""Analise publica do estudo Doctus AI.

Entrada: CSV longo com participante, acessou_copilot, sistema, criterio,
nota_original. Colunas nota e exclusao_metodologica, se presentes, sao
conferidas contra a regra de exclusao. Nenhum dado e simulado ou imputado.
Uso: python analysis_public.py --input data/ratings_anonymized.csv
"""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
import sys
from itertools import combinations
from pathlib import Path
import numpy as np
import pandas as pd
import scipy
from scipy.stats import friedmanchisquare, rankdata, wilcoxon
import statsmodels
from statsmodels.stats.multitest import multipletests
SYSTEMS = ["Doctus AI", "GitHub Copilot", "NotebookLM"]
CRITERIA = ["Didatica", "Praticidade", "Confiabilidade", "Completude", "Acessibilidade"]
CONTENT_CRITERIA = CRITERIA[:4]


def parse_bool(value):
    if pd.isna(value):
        raise ValueError("Indicador booleano ausente.")
    key = str(value).strip().lower()
    if key in {"true", "1", "1.0", "sim"}: return True
    if key in {"false", "0", "0.0", "nao", "não"}: return False
    raise ValueError(f"Indicador booleano invalido: {value!r}")


def load_public_base(path):
    raw = pd.read_csv(path, encoding="utf-8-sig", dtype={"participante": "string"})
    required = ["participante", "acessou_copilot", "sistema", "criterio", "nota_original"]
    missing = set(required) - set(raw.columns)
    if missing: raise ValueError(f"Colunas ausentes: {sorted(missing)}")
    df = raw[required].copy()
    if df.empty: raise ValueError("Base vazia.")
    if df["participante"].isna().any(): raise ValueError("Participante ausente.")
    df["participante"] = df["participante"].str.strip()
    if df["participante"].eq("").any(): raise ValueError("Participante vazio.")
    if not df["sistema"].isin(SYSTEMS).all(): raise ValueError("Sistema desconhecido.")
    if not df["criterio"].isin(CRITERIA).all(): raise ValueError("Criterio desconhecido.")
    df["acessou_copilot"] = df["acessou_copilot"].map(parse_bool)
    if df.groupby("participante")["acessou_copilot"].nunique().ne(1).any():
        raise ValueError("Acesso inconsistente dentro do participante.")
    df["nota_original"] = pd.to_numeric(df["nota_original"], errors="raise")
    if not df["nota_original"].dropna().isin([1,2,3,4,5]).all():
        raise ValueError("Notas devem ser inteiros de 1 a 5.")
    if df.duplicated(["participante", "sistema", "criterio"]).any():
        raise ValueError("Observacoes duplicadas.")
    if len(df) != df["participante"].nunique()*15:
        raise ValueError("Cada participante deve ter 15 linhas, incluindo notas ausentes.")
    mask = (~df["acessou_copilot"] & df["sistema"].eq("GitHub Copilot")
            & df["criterio"].isin(CONTENT_CRITERIA) & df["nota_original"].notna())
    df["nota"] = df["nota_original"].mask(mask)
    df["exclusao_metodologica"] = mask
    if "nota" in raw:
        supplied = pd.to_numeric(raw["nota"], errors="raise")
        if not np.allclose(supplied, df["nota"], equal_nan=True):
            raise ValueError("Coluna nota diverge da regra de exclusao.")
    if "exclusao_metodologica" in raw:
        if not raw["exclusao_metodologica"].map(parse_bool).eq(mask).all():
            raise ValueError("Indicador de exclusao inconsistente.")
    return df

def descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for criterion in CRITERIA:
        for system in SYSTEMS:
            values = df.loc[
                (df["criterio"] == criterion) & (df["sistema"] == system), "nota"
            ].dropna()
            rows.append({
                "criterio": criterion,
                "sistema": system,
                "n_valido": int(values.size),
                "mediana": values.median() if len(values) else np.nan,
                "q1": values.quantile(0.25) if len(values) else np.nan,
                "q3": values.quantile(0.75) if len(values) else np.nan,
                "iqr": values.quantile(0.75) - values.quantile(0.25) if len(values) else np.nan,
                "media": values.mean() if len(values) else np.nan,
                "desvio_padrao_amostral": values.std(ddof=1) if len(values) > 1 else np.nan,
            })
    return pd.DataFrame(rows)


def magnitude_w(value: float) -> str:
    if pd.isna(value): return "Nao calculado"
    if value < 0.10: return "Trivial"
    if value < 0.30: return "Pequeno"
    if value < 0.50: return "Moderado"
    return "Elevado"


def friedman_results(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for criterion in CRITERIA:
        wide = (
            df[df["criterio"] == criterion]
            .pivot(index="participante", columns="sistema", values="nota")
            .reindex(columns=SYSTEMS)
            .dropna(how="any")
        )
        n = len(wide)
        if n < 2:
            rows.append({"criterio": criterion, "n_casos_completos": n,
                         "Q": np.nan, "p_assintotico": np.nan, "W_kendall": np.nan,
                         "magnitude_W": "Nao calculado", "observacao": "Casos insuficientes"})
            continue
        result = friedmanchisquare(*(wide[s].to_numpy() for s in SYSTEMS))
        q, p = float(result.statistic), float(result.pvalue)
        w = q / (n * (len(SYSTEMS) - 1))
        rows.append({
            "criterio": criterion,
            "n_casos_completos": n,
            "Q": q,
            "p_assintotico": p,
            "W_kendall": w,
            "magnitude_W": magnitude_w(w),
            "observacao": "p assintotico; cautela em amostra pequena",
        })
    return pd.DataFrame(rows)


def rank_biserial(differences: np.ndarray) -> dict:
    differences = np.asarray(differences, dtype=float)
    differences = differences[~np.isnan(differences)]
    nonzero = differences[differences != 0]
    n_total = int(len(differences))
    n_zero = int(np.sum(differences == 0))
    if len(nonzero) == 0:
        return {"rbc": 0.0, "postos_positivos": 0.0, "postos_negativos": 0.0,
                "n_pares_validos": n_total, "n_diferencas_nulas": n_zero,
                "n_diferencas_nao_nulas": 0}
    ranks = rankdata(np.abs(nonzero), method="average")
    pos = float(ranks[nonzero > 0].sum())
    neg = float(ranks[nonzero < 0].sum())
    return {
        "rbc": (pos - neg) / (pos + neg),
        "postos_positivos": pos,
        "postos_negativos": neg,
        "n_pares_validos": n_total,
        "n_diferencas_nulas": n_zero,
        "n_diferencas_nao_nulas": int(len(nonzero)),
    }


def pairwise_results(df: pd.DataFrame, zero_method: str) -> pd.DataFrame:
    rows = []
    for criterion in CRITERIA:
        criterion_rows, pvals = [], []
        for a, b in combinations(SYSTEMS, 2):
            wide = (
                df[df["criterio"] == criterion]
                .pivot(index="participante", columns="sistema", values="nota")
                .reindex(columns=[a, b])
                .dropna(how="any")
            )
            differences = wide[a].to_numpy(float) - wide[b].to_numpy(float)
            effect = rank_biserial(differences)
            if len(wide) == 0:
                stat, p, note = np.nan, np.nan, "Sem pares validos"
            elif np.all(differences == 0):
                stat, p, note = 0.0, 1.0, "Todas as diferencas sao nulas"
            else:
                result = wilcoxon(differences, zero_method=zero_method,
                                  correction=False, alternative="two-sided", method="auto")
                stat, p, note = float(result.statistic), float(result.pvalue), ""
            criterion_rows.append({
                "criterio": criterion,
                "sistema_1": a,
                "sistema_2": b,
                "estatistica_wilcoxon": stat,
                "p_bruto": p,
                "zero_method": zero_method,
                "direcao_rbc": f"{a} > {b}" if effect["rbc"] > 0 else
                               (f"{b} > {a}" if effect["rbc"] < 0 else "Sem direcao"),
                "observacao": note,
                **effect,
            })
            pvals.append(p)

        valid = [i for i, p in enumerate(pvals) if not pd.isna(p)]
        if valid:
            reject, adjusted, _, _ = multipletests([pvals[i] for i in valid],
                                                    alpha=0.05, method="holm")
            for i, adj, rej in zip(valid, adjusted, reject):
                criterion_rows[i]["p_holm"] = float(adj)
                criterion_rows[i]["significativo_holm_0_05"] = bool(rej)
        for row in criterion_rows:
            row.setdefault("p_holm", np.nan)
            row.setdefault("significativo_holm_0_05", False)
            rows.append(row)
    return pd.DataFrame(rows)


def exclusion_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["criterio", "sistema"], as_index=False)
        .agg(
            n_linhas=("participante", "size"),
            n_notas_originais=("nota_original", "count"),
            n_exclusoes_metodologicas=("exclusao_metodologica", "sum"),
            n_notas_validas_analise=("nota", "count"),
        )
    )



def main():
    parser = argparse.ArgumentParser(description="Analise a partir da base publica")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results_reproduced"))
    args = parser.parse_args()
    df = load_public_base(args.input)
    args.output.mkdir(parents=True, exist_ok=True)
    def save(table, name):
        table.to_csv(args.output / name, index=False, encoding="utf-8-sig")
    save(df, "base_analise_verificada.csv")
    save(exclusion_summary(df), "auditoria_exclusoes_resumo.csv")
    save(descriptive_statistics(df), "descritivas.csv")
    save(friedman_results(df), "friedman.csv")
    main_results = pairwise_results(df, "wilcox")
    sensitivity = pairwise_results(df, "pratt")
    save(main_results, "wilcoxon_holm_rbc.csv")
    save(sensitivity, "wilcoxon_pratt.csv")
    keys = ["criterio", "sistema_1", "sistema_2"]
    cols = keys + ["p_bruto", "p_holm", "rbc", "n_pares_validos"]
    comparison = main_results[cols].merge(sensitivity[cols], on=keys,
                                         suffixes=("_wilcox", "_pratt"), validate="one_to_one")
    comparison["mesma_conclusao_holm"] = (comparison["p_holm_wilcox"].lt(.05)
                                             == comparison["p_holm_pratt"].lt(.05))
    save(comparison, "comparacao_wilcox_pratt.csv")
    metadata = {
        "python": sys.version, "platform": platform.platform(),
        "pandas": pd.__version__, "numpy": np.__version__,
        "scipy": scipy.__version__, "statsmodels": statsmodels.__version__,
        "input_file": args.input.name,
        "input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "wilcoxon_zero_methods": ["wilcox", "pratt"],
        "wilcoxon_p_method": "auto", "wilcoxon_correction": False,
        "wilcoxon_alternative": "two-sided",
        "holm_family": "tres contrastes por criterio",
        "rbc": "postos das diferencas nao nulas, igual nas duas analises",
        "quartis": "interpolacao linear do pandas", "desvio_padrao_ddof": 1,
        "nota_magnitude_W": "Rotulos legados preservados do script original; nao validam limites bibliograficos."
    }
    (args.output / "versoes_e_parametros.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Participantes: {df.participante.nunique()}")
    print(f"Avaliacoes invalidadas: {int(df.exclusao_metodologica.sum())}")
    print(f"Resultados: {args.output.resolve()}")

if __name__ == "__main__":
    main()
