"""
Gera data/fixtures.json com os 104 jogos da Copa do Mundo 2026.

Fonte dos dados:
  - Fase de grupos: calendário oficial FIFA / DAZN (datas, sedes, times)
  - Mata-mata: chaveamento oficial FIFA (Wikipedia / regulamento)

Uso:
    python scripts/build_static_fixtures.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from scripts.helpers import save_json, utc_now

# ---------------------------------------------------------------------------
# FASE DE GRUPOS — 72 jogos
# Formato: (id, data_utc, grupo, mandante, visitante, estadio, cidade)
# ---------------------------------------------------------------------------

GROUP_STAGE: list[tuple] = [

    # ── GRUPO A: México, África do Sul, Coreia do Sul, República Tcheca ─────
    (9001, "2026-06-11T18:00:00+00:00", "A", "México",          "África do Sul",    "Estadio Azteca",          "Mexico City"),
    (9002, "2026-06-11T22:00:00+00:00", "A", "Coreia do Sul",   "República Tcheca", "Estadio Akron",           "Guadalajara"),
    (9003, "2026-06-18T18:00:00+00:00", "A", "República Tcheca","África do Sul",    "Mercedes-Benz Stadium",   "Atlanta, GA"),
    (9004, "2026-06-18T22:00:00+00:00", "A", "México",          "Coreia do Sul",    "Estadio Akron",           "Guadalajara"),
    (9005, "2026-06-24T21:00:00+00:00", "A", "República Tcheca","México",           "Estadio Azteca",          "Mexico City"),
    (9006, "2026-06-24T21:00:00+00:00", "A", "África do Sul",   "Coreia do Sul",    "Estadio BBVA",            "Monterrey"),

    # ── GRUPO B: Canadá, Bósnia e Herzegovina, Qatar, Suíça ─────────────────
    (9007, "2026-06-12T18:00:00+00:00", "B", "Canadá",              "Bósnia e Herzegovina","BMO Field",      "Toronto"),
    (9008, "2026-06-12T22:00:00+00:00", "B", "Qatar",               "Suíça",               "Levi's Stadium", "Santa Clara, CA"),
    (9009, "2026-06-18T18:00:00+00:00", "B", "Suíça",               "Bósnia e Herzegovina","SoFi Stadium",   "Los Angeles, CA"),
    (9010, "2026-06-18T22:00:00+00:00", "B", "Canadá",              "Qatar",               "BC Place",        "Vancouver"),
    (9011, "2026-06-24T17:00:00+00:00", "B", "Suíça",               "Canadá",              "BC Place",        "Vancouver"),
    (9012, "2026-06-24T17:00:00+00:00", "B", "Bósnia e Herzegovina","Qatar",               "Lumen Field",     "Seattle, WA"),

    # ── GRUPO C: Brasil, Marrocos, Haiti, Escócia ────────────────────────────
    (9013, "2026-06-13T18:00:00+00:00", "C", "Brasil",  "Marrocos", "Gillette Stadium",        "Foxborough, MA"),
    (9014, "2026-06-13T22:00:00+00:00", "C", "Haiti",   "Escócia",  "MetLife Stadium",          "East Rutherford, NJ"),
    (9015, "2026-06-19T18:00:00+00:00", "C", "Brasil",  "Haiti",    "Lincoln Financial Field",  "Philadelphia, PA"),
    (9016, "2026-06-19T22:00:00+00:00", "C", "Escócia", "Marrocos", "Gillette Stadium",         "Foxborough, MA"),
    (9017, "2026-06-25T01:00:00+00:00", "C", "Escócia", "Brasil",   "Hard Rock Stadium",        "Miami Gardens, FL"),
    (9018, "2026-06-25T01:00:00+00:00", "C", "Marrocos","Haiti",    "Mercedes-Benz Stadium",    "Atlanta, GA"),

    # ── GRUPO D: EUA, Paraguai, Austrália, Turquia ───────────────────────────
    (9019, "2026-06-12T18:00:00+00:00", "D", "EUA",      "Paraguai",  "SoFi Stadium",   "Los Angeles, CA"),
    (9020, "2026-06-12T22:00:00+00:00", "D", "Austrália","Turquia",   "BC Place",        "Vancouver"),
    (9021, "2026-06-19T18:00:00+00:00", "D", "Turquia",  "Paraguai",  "Levi's Stadium",  "Santa Clara, CA"),
    (9022, "2026-06-19T22:00:00+00:00", "D", "EUA",      "Austrália", "Lumen Field",     "Seattle, WA"),
    (9023, "2026-06-25T21:00:00+00:00", "D", "Turquia",  "EUA",       "SoFi Stadium",    "Los Angeles, CA"),
    (9024, "2026-06-25T21:00:00+00:00", "D", "Paraguai", "Austrália", "Levi's Stadium",  "Santa Clara, CA"),

    # ── GRUPO E: Alemanha, Curaçao, Costa do Marfim, Equador ────────────────
    (9025, "2026-06-14T18:00:00+00:00", "E", "Alemanha",       "Curaçao",        "Lincoln Financial Field","Philadelphia, PA"),
    (9026, "2026-06-14T22:00:00+00:00", "E", "Costa do Marfim","Equador",         "NRG Stadium",            "Houston, TX"),
    (9027, "2026-06-20T18:00:00+00:00", "E", "Alemanha",       "Costa do Marfim", "BMO Field",              "Toronto"),
    (9028, "2026-06-20T22:00:00+00:00", "E", "Equador",        "Curaçao",         "Arrowhead Stadium",      "Kansas City, MO"),
    (9029, "2026-06-25T17:00:00+00:00", "E", "Equador",        "Alemanha",        "Lincoln Financial Field","Philadelphia, PA"),
    (9030, "2026-06-25T17:00:00+00:00", "E", "Curaçao",        "Costa do Marfim", "MetLife Stadium",        "East Rutherford, NJ"),

    # ── GRUPO F: Países Baixos, Japão, Suécia, Tunísia ──────────────────────
    (9031, "2026-06-14T18:00:00+00:00", "F", "Países Baixos","Japão",         "AT&T Stadium",    "Arlington, TX"),
    (9032, "2026-06-14T22:00:00+00:00", "F", "Suécia",       "Tunísia",        "Estadio BBVA",    "Monterrey"),
    (9033, "2026-06-20T18:00:00+00:00", "F", "Países Baixos","Suécia",         "NRG Stadium",     "Houston, TX"),
    (9034, "2026-06-20T22:00:00+00:00", "F", "Tunísia",      "Japão",          "Estadio BBVA",    "Monterrey"),
    (9035, "2026-06-26T01:00:00+00:00", "F", "Tunísia",      "Países Baixos",  "AT&T Stadium",    "Arlington, TX"),
    (9036, "2026-06-26T01:00:00+00:00", "F", "Japão",        "Suécia",         "Arrowhead Stadium","Kansas City, MO"),

    # ── GRUPO G: Bélgica, Egito, Irã, Nova Zelândia ─────────────────────────
    (9037, "2026-06-15T18:00:00+00:00", "G", "Bélgica",      "Egito",        "SoFi Stadium", "Los Angeles, CA"),
    (9038, "2026-06-15T22:00:00+00:00", "G", "Irã",          "Nova Zelândia", "Lumen Field",  "Seattle, WA"),
    (9039, "2026-06-21T18:00:00+00:00", "G", "Bélgica",      "Irã",           "SoFi Stadium", "Los Angeles, CA"),
    (9040, "2026-06-21T22:00:00+00:00", "G", "Nova Zelândia","Egito",          "BC Place",     "Vancouver"),
    (9041, "2026-06-26T21:00:00+00:00", "G", "Nova Zelândia","Bélgica",        "Lumen Field",  "Seattle, WA"),
    (9042, "2026-06-26T21:00:00+00:00", "G", "Egito",        "Irã",            "BC Place",     "Vancouver"),

    # ── GRUPO H: Espanha, Cabo Verde, Arábia Saudita, Uruguai ───────────────
    (9043, "2026-06-15T18:00:00+00:00", "H", "Espanha",       "Cabo Verde",    "Hard Rock Stadium",      "Miami Gardens, FL"),
    (9044, "2026-06-15T22:00:00+00:00", "H", "Arábia Saudita","Uruguai",       "Mercedes-Benz Stadium",  "Atlanta, GA"),
    (9045, "2026-06-21T18:00:00+00:00", "H", "Espanha",       "Arábia Saudita","Hard Rock Stadium",      "Miami Gardens, FL"),
    (9046, "2026-06-21T22:00:00+00:00", "H", "Uruguai",       "Cabo Verde",    "Mercedes-Benz Stadium",  "Atlanta, GA"),
    (9047, "2026-06-26T17:00:00+00:00", "H", "Uruguai",       "Espanha",       "NRG Stadium",            "Houston, TX"),
    (9048, "2026-06-26T17:00:00+00:00", "H", "Cabo Verde",    "Arábia Saudita","Estadio Akron",           "Guadalajara"),

    # ── GRUPO I: França, Senegal, Iraque, Noruega ────────────────────────────
    (9049, "2026-06-16T18:00:00+00:00", "I", "França",  "Senegal", "MetLife Stadium",         "East Rutherford, NJ"),
    (9050, "2026-06-16T22:00:00+00:00", "I", "Iraque",  "Noruega", "Gillette Stadium",         "Foxborough, MA"),
    (9051, "2026-06-22T18:00:00+00:00", "I", "França",  "Iraque",  "MetLife Stadium",          "East Rutherford, NJ"),
    (9052, "2026-06-22T22:00:00+00:00", "I", "Noruega", "Senegal", "Lincoln Financial Field",  "Philadelphia, PA"),
    (9053, "2026-06-27T01:00:00+00:00", "I", "Noruega", "França",  "Gillette Stadium",          "Foxborough, MA"),
    (9054, "2026-06-27T01:00:00+00:00", "I", "Senegal", "Iraque",  "BMO Field",                "Toronto"),

    # ── GRUPO J: Argentina, Argélia, Áustria, Jordânia ──────────────────────
    (9055, "2026-06-16T18:00:00+00:00", "J", "Argentina","Argélia",  "Arrowhead Stadium", "Kansas City, MO"),
    (9056, "2026-06-16T22:00:00+00:00", "J", "Áustria",  "Jordânia", "Levi's Stadium",    "Santa Clara, CA"),
    (9057, "2026-06-22T18:00:00+00:00", "J", "Argentina","Áustria",  "AT&T Stadium",      "Arlington, TX"),
    (9058, "2026-06-22T22:00:00+00:00", "J", "Jordânia", "Argélia",  "Levi's Stadium",    "Santa Clara, CA"),
    (9059, "2026-06-27T21:00:00+00:00", "J", "Jordânia", "Argentina","Arrowhead Stadium", "Kansas City, MO"),
    (9060, "2026-06-27T21:00:00+00:00", "J", "Argélia",  "Áustria",  "AT&T Stadium",      "Arlington, TX"),

    # ── GRUPO K: Portugal, Congo DR, Uzbequistão, Colômbia ──────────────────
    (9061, "2026-06-17T18:00:00+00:00", "K", "Portugal",    "Congo DR",    "NRG Stadium",           "Houston, TX"),
    (9062, "2026-06-17T22:00:00+00:00", "K", "Uzbequistão", "Colômbia",   "Estadio Azteca",         "Mexico City"),
    (9063, "2026-06-23T18:00:00+00:00", "K", "Portugal",    "Uzbequistão", "NRG Stadium",            "Houston, TX"),
    (9064, "2026-06-23T22:00:00+00:00", "K", "Colômbia",    "Congo DR",    "Estadio Akron",          "Guadalajara"),
    (9065, "2026-06-27T17:00:00+00:00", "K", "Colômbia",    "Portugal",    "Hard Rock Stadium",      "Miami Gardens, FL"),
    (9066, "2026-06-27T17:00:00+00:00", "K", "Congo DR",    "Uzbequistão", "Mercedes-Benz Stadium",  "Atlanta, GA"),

    # ── GRUPO L: Inglaterra, Croácia, Gana, Panamá ──────────────────────────
    (9067, "2026-06-17T18:00:00+00:00", "L", "Inglaterra","Croácia", "BMO Field",                "Toronto"),
    (9068, "2026-06-17T22:00:00+00:00", "L", "Gana",      "Panamá",  "AT&T Stadium",             "Arlington, TX"),
    (9069, "2026-06-23T18:00:00+00:00", "L", "Inglaterra","Gana",    "Gillette Stadium",          "Foxborough, MA"),
    (9070, "2026-06-23T22:00:00+00:00", "L", "Panamá",    "Croácia", "BMO Field",                "Toronto"),
    (9071, "2026-06-28T01:00:00+00:00", "L", "Panamá",    "Inglaterra","MetLife Stadium",         "East Rutherford, NJ"),
    (9072, "2026-06-28T01:00:00+00:00", "L", "Croácia",   "Gana",    "Lincoln Financial Field",  "Philadelphia, PA"),
]

# ---------------------------------------------------------------------------
# MATA-MATA — 32 jogos (IDs 9073–9104, espelham M73–M104 da FIFA)
#
# Chaveamento oficial FIFA (sorteio dez/2025):
#   Rodada de 32  → Oitavas → Quartas → Semis → Final
#
# Notação dos mandantes/visitantes:
#   "1º A"              = 1º colocado do Grupo A
#   "2º B"              = 2º colocado do Grupo B
#   "3º (A/B/C/D/F)"    = melhor 3º entre esses grupos
#   "Ven. J73"          = vencedor do Jogo 73
#   "Perd. J101"        = perdedor do Jogo 101 (3º lugar)
#
# Formato: (id, data_utc, fase, mandante, visitante, estadio, cidade)
# ---------------------------------------------------------------------------

KNOCKOUT: list[tuple] = [

    # ── RODADA DE 32 ─────────────────────────────────────────────────────────
    (9073, "2026-06-28T21:00:00+00:00", "Round of 32",  "2º A",              "2º B",               "SoFi Stadium",            "Los Angeles, CA"),
    (9074, "2026-06-29T18:00:00+00:00", "Round of 32",  "1º E",              "3º (A/B/C/D/F)",     "Gillette Stadium",         "Foxborough, MA"),
    (9075, "2026-06-29T22:00:00+00:00", "Round of 32",  "1º F",              "2º C",               "Estadio Akron",            "Guadalajara"),
    (9076, "2026-06-29T02:00:00+00:00", "Round of 32",  "1º C",              "2º F",               "NRG Stadium",              "Houston, TX"),
    (9077, "2026-06-30T18:00:00+00:00", "Round of 32",  "1º I",              "3º (C/D/F/G/H)",     "MetLife Stadium",          "East Rutherford, NJ"),
    (9078, "2026-06-30T22:00:00+00:00", "Round of 32",  "2º E",              "2º I",               "AT&T Stadium",             "Arlington, TX"),
    (9079, "2026-06-30T02:00:00+00:00", "Round of 32",  "1º A",              "3º (C/E/F/H/I)",     "Estadio Azteca",           "Mexico City"),
    (9080, "2026-07-01T18:00:00+00:00", "Round of 32",  "1º L",              "3º (E/H/I/J/K)",     "Mercedes-Benz Stadium",    "Atlanta, GA"),
    (9081, "2026-07-01T22:00:00+00:00", "Round of 32",  "1º D",              "3º (B/E/F/I/J)",     "Levi's Stadium",           "Santa Clara, CA"),
    (9082, "2026-07-01T02:00:00+00:00", "Round of 32",  "1º G",              "3º (A/E/H/I/J)",     "Lumen Field",              "Seattle, WA"),
    (9083, "2026-07-02T18:00:00+00:00", "Round of 32",  "2º K",              "2º L",               "BMO Field",                "Toronto"),
    (9084, "2026-07-02T22:00:00+00:00", "Round of 32",  "1º H",              "2º J",               "SoFi Stadium",             "Los Angeles, CA"),
    (9085, "2026-07-02T02:00:00+00:00", "Round of 32",  "1º B",              "3º (E/F/G/I/J)",     "BC Place",                 "Vancouver"),
    (9086, "2026-07-03T18:00:00+00:00", "Round of 32",  "1º J",              "2º H",               "Hard Rock Stadium",        "Miami Gardens, FL"),
    (9087, "2026-07-03T22:00:00+00:00", "Round of 32",  "1º K",              "3º (D/E/I/J/L)",     "Arrowhead Stadium",        "Kansas City, MO"),
    (9088, "2026-07-03T02:00:00+00:00", "Round of 32",  "2º D",              "2º G",               "AT&T Stadium",             "Arlington, TX"),

    # ── OITAVAS DE FINAL ─────────────────────────────────────────────────────
    (9089, "2026-07-04T18:00:00+00:00", "Round of 16",  "Ven. J74",          "Ven. J77",           "Estadio Azteca",           "Mexico City"),
    (9090, "2026-07-04T22:00:00+00:00", "Round of 16",  "Ven. J73",          "Ven. J75",           "MetLife Stadium",          "East Rutherford, NJ"),
    (9091, "2026-07-05T18:00:00+00:00", "Round of 16",  "Ven. J76",          "Ven. J78",           "NRG Stadium",              "Houston, TX"),
    (9092, "2026-07-05T22:00:00+00:00", "Round of 16",  "Ven. J79",          "Ven. J80",           "Estadio Azteca",           "Mexico City"),
    (9093, "2026-07-06T18:00:00+00:00", "Round of 16",  "Ven. J83",          "Ven. J84",           "AT&T Stadium",             "Arlington, TX"),
    (9094, "2026-07-06T22:00:00+00:00", "Round of 16",  "Ven. J81",          "Ven. J82",           "Lumen Field",              "Seattle, WA"),
    (9095, "2026-07-07T18:00:00+00:00", "Round of 16",  "Ven. J86",          "Ven. J88",           "Lincoln Financial Field",  "Philadelphia, PA"),
    (9096, "2026-07-07T22:00:00+00:00", "Round of 16",  "Ven. J85",          "Ven. J87",           "Mercedes-Benz Stadium",    "Atlanta, GA"),

    # ── QUARTAS DE FINAL ─────────────────────────────────────────────────────
    (9097, "2026-07-09T21:00:00+00:00", "Quarter-finals","Ven. J89",         "Ven. J90",           "Gillette Stadium",         "Foxborough, MA"),
    (9098, "2026-07-10T21:00:00+00:00", "Quarter-finals","Ven. J93",         "Ven. J94",           "SoFi Stadium",             "Los Angeles, CA"),
    (9099, "2026-07-11T18:00:00+00:00", "Quarter-finals","Ven. J91",         "Ven. J92",           "Hard Rock Stadium",        "Miami Gardens, FL"),
    (9100, "2026-07-11T22:00:00+00:00", "Quarter-finals","Ven. J95",         "Ven. J96",           "Arrowhead Stadium",        "Kansas City, MO"),

    # ── SEMIFINAIS ───────────────────────────────────────────────────────────
    (9101, "2026-07-14T22:00:00+00:00", "Semi-finals",   "Ven. J97",         "Ven. J98",           "AT&T Stadium",             "Arlington, TX"),
    (9102, "2026-07-15T22:00:00+00:00", "Semi-finals",   "Ven. J99",         "Ven. J100",          "Mercedes-Benz Stadium",    "Atlanta, GA"),

    # ── DISPUTA DE 3º LUGAR ──────────────────────────────────────────────────
    (9103, "2026-07-18T19:00:00+00:00", "3rd Place Final","Perd. J101",       "Perd. J102",         "Hard Rock Stadium",        "Miami Gardens, FL"),

    # ── FINAL ────────────────────────────────────────────────────────────────
    (9104, "2026-07-19T19:00:00+00:00", "Final",          "Ven. J101",        "Ven. J102",          "MetLife Stadium",          "East Rutherford, NJ"),
]


# ---------------------------------------------------------------------------
# Conversão para o schema de fixtures
# ---------------------------------------------------------------------------

def _make_group_fixture(row: tuple) -> dict:
    fid, date, group, home, away, venue, city = row
    return {
        "id": fid,
        "date": date,
        "status": "NS",
        "round": f"Group Stage - {group}",
        "home": {"id": None, "name": home, "winner": None},
        "away": {"id": None, "name": away, "winner": None},
        "score": {"home": None, "away": None},
        "venue": {"name": venue, "city": city},
    }


def _make_knockout_fixture(row: tuple) -> dict:
    fid, date, phase, home, away, venue, city = row
    # Número do jogo = ID - 9000  (9073 → J73, 9104 → J104)
    match_num = fid - 9000
    return {
        "id": fid,
        "date": date,
        "status": "NS",
        "round": phase,
        "match_num": match_num,
        "home": {"id": None, "name": home, "winner": None},
        "away": {"id": None, "name": away, "winner": None},
        "score": {"home": None, "away": None},
        "venue": {"name": venue, "city": city},
    }


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def main() -> None:
    group_fixtures   = [_make_group_fixture(r)   for r in GROUP_STAGE]
    knockout_fixtures = [_make_knockout_fixture(r) for r in KNOCKOUT]
    all_fixtures = group_fixtures + knockout_fixtures

    payload = {
        "updated_at": utc_now().isoformat(),
        "source": "static",
        "total": len(all_fixtures),
        "fixtures": all_fixtures,
    }

    save_json(config.FIXTURES_FILE, payload)
    print(f"[static] {len(group_fixtures)} jogos de grupo + {len(knockout_fixtures)} mata-mata")
    print(f"[static] Total: {len(all_fixtures)} fixtures em {config.FIXTURES_FILE}")


if __name__ == "__main__":
    main()
