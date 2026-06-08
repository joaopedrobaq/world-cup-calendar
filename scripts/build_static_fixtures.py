"""
Gera data/fixtures.json com os 104 jogos da Copa do Mundo 2026.

Fonte dos dados:
  - Horários oficiais em ET (EDT = UTC-4) convertidos para UTC
  - Fonte: worldcupwiki.com / NBC Sports / FIFA

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
# Todos os horários em UTC (horário ET + 4h)
# ---------------------------------------------------------------------------

GROUP_STAGE: list[tuple] = [

    # ── GRUPO A: México, África do Sul, Coreia do Sul, República Tcheca ─────
    (9001, "2026-06-11T19:00:00+00:00", "A", "México",          "África do Sul",    "Estadio Azteca",          "Mexico City"),        # 3pm ET
    (9002, "2026-06-12T02:00:00+00:00", "A", "Coreia do Sul",   "República Tcheca", "Estadio Akron",           "Guadalajara"),        # 10pm ET 11/jun
    (9003, "2026-06-18T16:00:00+00:00", "A", "República Tcheca","África do Sul",    "Mercedes-Benz Stadium",   "Atlanta, GA"),        # 12pm ET
    (9004, "2026-06-19T01:00:00+00:00", "A", "México",          "Coreia do Sul",    "Estadio Akron",           "Guadalajara"),        # 9pm ET 18/jun
    (9005, "2026-06-25T01:00:00+00:00", "A", "República Tcheca","México",           "Estadio Azteca",          "Mexico City"),        # 9pm ET 24/jun
    (9006, "2026-06-25T01:00:00+00:00", "A", "África do Sul",   "Coreia do Sul",    "Estadio BBVA",            "Monterrey"),          # 9pm ET 24/jun

    # ── GRUPO B: Canadá, Bósnia e Herzegovina, Qatar, Suíça ─────────────────
    (9007, "2026-06-12T19:00:00+00:00", "B", "Canadá",              "Bósnia e Herzegovina","BMO Field",      "Toronto"),             # 3pm ET
    (9008, "2026-06-13T19:00:00+00:00", "B", "Qatar",               "Suíça",               "Levi's Stadium", "Santa Clara, CA"),    # 3pm ET 13/jun
    (9009, "2026-06-18T19:00:00+00:00", "B", "Suíça",               "Bósnia e Herzegovina","SoFi Stadium",   "Los Angeles, CA"),    # 3pm ET
    (9010, "2026-06-18T22:00:00+00:00", "B", "Canadá",              "Qatar",               "BC Place",        "Vancouver"),          # 6pm ET
    (9011, "2026-06-24T19:00:00+00:00", "B", "Suíça",               "Canadá",              "BC Place",        "Vancouver"),          # 3pm ET
    (9012, "2026-06-24T19:00:00+00:00", "B", "Bósnia e Herzegovina","Qatar",               "Lumen Field",     "Seattle, WA"),        # 3pm ET

    # ── GRUPO C: Brasil, Marrocos, Haiti, Escócia ────────────────────────────
    (9013, "2026-06-13T22:00:00+00:00", "C", "Brasil",  "Marrocos", "MetLife Stadium",          "East Rutherford, NJ"),              # 6pm ET
    (9014, "2026-06-14T01:00:00+00:00", "C", "Haiti",   "Escócia",  "Gillette Stadium",          "Foxborough, MA"),                  # 9pm ET 13/jun
    (9015, "2026-06-20T00:30:00+00:00", "C", "Brasil",  "Haiti",    "Lincoln Financial Field",  "Philadelphia, PA"),                 # 8:30pm ET 19/jun
    (9016, "2026-06-19T22:00:00+00:00", "C", "Escócia", "Marrocos", "Gillette Stadium",         "Foxborough, MA"),                   # 6pm ET
    (9017, "2026-06-24T22:00:00+00:00", "C", "Escócia", "Brasil",   "Hard Rock Stadium",        "Miami Gardens, FL"),               # 6pm ET
    (9018, "2026-06-24T22:00:00+00:00", "C", "Marrocos","Haiti",    "Mercedes-Benz Stadium",    "Atlanta, GA"),                     # 6pm ET

    # ── GRUPO D: EUA, Paraguai, Austrália, Turquia ───────────────────────────
    (9019, "2026-06-13T01:00:00+00:00", "D", "EUA",      "Paraguai",  "SoFi Stadium",   "Los Angeles, CA"),                        # 9pm ET 12/jun
    (9020, "2026-06-14T04:00:00+00:00", "D", "Austrália","Turquia",   "BC Place",        "Vancouver"),                              # 12am ET 14/jun
    (9021, "2026-06-20T03:00:00+00:00", "D", "Turquia",  "Paraguai",  "Levi's Stadium",  "Santa Clara, CA"),                       # 11pm ET 19/jun
    (9022, "2026-06-19T19:00:00+00:00", "D", "EUA",      "Austrália", "Lumen Field",     "Seattle, WA"),                           # 3pm ET
    (9023, "2026-06-26T02:00:00+00:00", "D", "Turquia",  "EUA",       "SoFi Stadium",    "Los Angeles, CA"),                       # 10pm ET 25/jun
    (9024, "2026-06-26T02:00:00+00:00", "D", "Paraguai", "Austrália", "Levi's Stadium",  "Santa Clara, CA"),                       # 10pm ET 25/jun

    # ── GRUPO E: Alemanha, Curaçao, Costa do Marfim, Equador ────────────────
    (9025, "2026-06-14T17:00:00+00:00", "E", "Alemanha",       "Curaçao",        "NRG Stadium",            "Houston, TX"),          # 1pm ET
    (9026, "2026-06-14T23:00:00+00:00", "E", "Costa do Marfim","Equador",         "Lincoln Financial Field","Philadelphia, PA"),     # 7pm ET
    (9027, "2026-06-20T20:00:00+00:00", "E", "Alemanha",       "Costa do Marfim", "BMO Field",              "Toronto"),             # 4pm ET
    (9028, "2026-06-21T00:00:00+00:00", "E", "Equador",        "Curaçao",         "Arrowhead Stadium",      "Kansas City, MO"),     # 8pm ET 20/jun
    (9029, "2026-06-25T20:00:00+00:00", "E", "Equador",        "Alemanha",        "MetLife Stadium",        "East Rutherford, NJ"), # 4pm ET
    (9030, "2026-06-25T20:00:00+00:00", "E", "Curaçao",        "Costa do Marfim", "Lincoln Financial Field","Philadelphia, PA"),    # 4pm ET

    # ── GRUPO F: Países Baixos, Japão, Suécia, Tunísia ──────────────────────
    (9031, "2026-06-14T20:00:00+00:00", "F", "Países Baixos","Japão",         "AT&T Stadium",    "Arlington, TX"),                  # 4pm ET
    (9032, "2026-06-15T02:00:00+00:00", "F", "Suécia",       "Tunísia",        "Estadio BBVA",    "Monterrey"),                    # 10pm ET 14/jun
    (9033, "2026-06-20T17:00:00+00:00", "F", "Países Baixos","Suécia",         "NRG Stadium",     "Houston, TX"),                  # 1pm ET
    (9034, "2026-06-21T04:00:00+00:00", "F", "Tunísia",      "Japão",          "Estadio BBVA",    "Monterrey"),                    # 12am ET 21/jun
    (9035, "2026-06-25T23:00:00+00:00", "F", "Tunísia",      "Países Baixos",  "Arrowhead Stadium","Kansas City, MO"),             # 7pm ET
    (9036, "2026-06-25T23:00:00+00:00", "F", "Japão",        "Suécia",         "AT&T Stadium",    "Arlington, TX"),                # 7pm ET

    # ── GRUPO G: Bélgica, Egito, Irã, Nova Zelândia ─────────────────────────
    (9037, "2026-06-15T19:00:00+00:00", "G", "Bélgica",      "Egito",        "Lumen Field",  "Seattle, WA"),                      # 3pm ET
    (9038, "2026-06-16T01:00:00+00:00", "G", "Irã",          "Nova Zelândia", "SoFi Stadium", "Los Angeles, CA"),                 # 9pm ET 15/jun
    (9039, "2026-06-21T19:00:00+00:00", "G", "Bélgica",      "Irã",           "SoFi Stadium", "Los Angeles, CA"),                 # 3pm ET
    (9040, "2026-06-22T01:00:00+00:00", "G", "Nova Zelândia","Egito",          "BC Place",     "Vancouver"),                      # 9pm ET 21/jun
    (9041, "2026-06-27T03:00:00+00:00", "G", "Nova Zelândia","Bélgica",        "BC Place",     "Vancouver"),                      # 11pm ET 26/jun
    (9042, "2026-06-27T03:00:00+00:00", "G", "Egito",        "Irã",            "Lumen Field",  "Seattle, WA"),                    # 11pm ET 26/jun

    # ── GRUPO H: Espanha, Cabo Verde, Arábia Saudita, Uruguai ───────────────
    (9043, "2026-06-15T16:00:00+00:00", "H", "Espanha",       "Cabo Verde",    "Mercedes-Benz Stadium",  "Atlanta, GA"),           # 12pm ET
    (9044, "2026-06-15T22:00:00+00:00", "H", "Arábia Saudita","Uruguai",       "Hard Rock Stadium",      "Miami Gardens, FL"),     # 6pm ET
    (9045, "2026-06-21T16:00:00+00:00", "H", "Espanha",       "Arábia Saudita","Mercedes-Benz Stadium",  "Atlanta, GA"),           # 12pm ET
    (9046, "2026-06-21T22:00:00+00:00", "H", "Uruguai",       "Cabo Verde",    "Hard Rock Stadium",      "Miami Gardens, FL"),     # 6pm ET
    (9047, "2026-06-27T00:00:00+00:00", "H", "Uruguai",       "Espanha",       "Estadio Akron",           "Guadalajara"),          # 8pm ET 26/jun
    (9048, "2026-06-27T00:00:00+00:00", "H", "Cabo Verde",    "Arábia Saudita","NRG Stadium",            "Houston, TX"),           # 8pm ET 26/jun

    # ── GRUPO I: França, Senegal, Iraque, Noruega ────────────────────────────
    (9049, "2026-06-16T19:00:00+00:00", "I", "França",  "Senegal", "MetLife Stadium",         "East Rutherford, NJ"),              # 3pm ET
    (9050, "2026-06-16T22:00:00+00:00", "I", "Iraque",  "Noruega", "Gillette Stadium",         "Foxborough, MA"),                  # 6pm ET
    (9051, "2026-06-22T21:00:00+00:00", "I", "França",  "Iraque",  "Lincoln Financial Field",  "Philadelphia, PA"),                # 5pm ET
    (9052, "2026-06-23T00:00:00+00:00", "I", "Noruega", "Senegal", "MetLife Stadium",          "East Rutherford, NJ"),             # 8pm ET 22/jun
    (9053, "2026-06-26T19:00:00+00:00", "I", "Noruega", "França",  "Gillette Stadium",          "Foxborough, MA"),                 # 3pm ET
    (9054, "2026-06-26T19:00:00+00:00", "I", "Senegal", "Iraque",  "BMO Field",                "Toronto"),                        # 3pm ET

    # ── GRUPO J: Argentina, Argélia, Áustria, Jordânia ──────────────────────
    (9055, "2026-06-17T01:00:00+00:00", "J", "Argentina","Argélia",  "Arrowhead Stadium", "Kansas City, MO"),                     # 9pm ET 16/jun
    (9056, "2026-06-17T04:00:00+00:00", "J", "Áustria",  "Jordânia", "Levi's Stadium",    "Santa Clara, CA"),                     # 12am ET 17/jun
    (9057, "2026-06-22T17:00:00+00:00", "J", "Argentina","Áustria",  "AT&T Stadium",      "Arlington, TX"),                       # 1pm ET
    (9058, "2026-06-23T03:00:00+00:00", "J", "Jordânia", "Argélia",  "Levi's Stadium",    "Santa Clara, CA"),                     # 11pm ET 22/jun
    (9059, "2026-06-28T02:00:00+00:00", "J", "Jordânia", "Argentina","AT&T Stadium",      "Arlington, TX"),                       # 10pm ET 27/jun
    (9060, "2026-06-28T02:00:00+00:00", "J", "Argélia",  "Áustria",  "Arrowhead Stadium", "Kansas City, MO"),                     # 10pm ET 27/jun

    # ── GRUPO K: Portugal, Congo DR, Uzbequistão, Colômbia ──────────────────
    (9061, "2026-06-17T17:00:00+00:00", "K", "Portugal",    "Congo DR",    "NRG Stadium",           "Houston, TX"),               # 1pm ET
    (9062, "2026-06-18T02:00:00+00:00", "K", "Uzbequistão", "Colômbia",   "Estadio Azteca",         "Mexico City"),               # 10pm ET 17/jun
    (9063, "2026-06-23T17:00:00+00:00", "K", "Portugal",    "Uzbequistão", "NRG Stadium",            "Houston, TX"),              # 1pm ET
    (9064, "2026-06-24T02:00:00+00:00", "K", "Colômbia",    "Congo DR",    "Estadio Akron",          "Guadalajara"),              # 10pm ET 23/jun
    (9065, "2026-06-27T23:30:00+00:00", "K", "Colômbia",    "Portugal",    "Hard Rock Stadium",      "Miami Gardens, FL"),        # 7:30pm ET
    (9066, "2026-06-27T23:30:00+00:00", "K", "Congo DR",    "Uzbequistão", "Mercedes-Benz Stadium",  "Atlanta, GA"),              # 7:30pm ET

    # ── GRUPO L: Inglaterra, Croácia, Gana, Panamá ──────────────────────────
    (9067, "2026-06-17T20:00:00+00:00", "L", "Inglaterra","Croácia", "AT&T Stadium",             "Arlington, TX"),                # 4pm ET
    (9068, "2026-06-17T23:00:00+00:00", "L", "Gana",      "Panamá",  "BMO Field",                "Toronto"),                     # 7pm ET
    (9069, "2026-06-23T20:00:00+00:00", "L", "Inglaterra","Gana",    "Gillette Stadium",          "Foxborough, MA"),              # 4pm ET
    (9070, "2026-06-23T23:00:00+00:00", "L", "Panamá",    "Croácia", "BMO Field",                "Toronto"),                     # 7pm ET
    (9071, "2026-06-27T21:00:00+00:00", "L", "Panamá",    "Inglaterra","MetLife Stadium",         "East Rutherford, NJ"),        # 5pm ET
    (9072, "2026-06-27T21:00:00+00:00", "L", "Croácia",   "Gana",    "Lincoln Financial Field",  "Philadelphia, PA"),            # 5pm ET
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
    (9073, "2026-06-28T19:00:00+00:00", "Round of 32",  "2º A",              "2º B",               "SoFi Stadium",            "Los Angeles, CA"),   # 3pm ET
    (9074, "2026-06-29T20:30:00+00:00", "Round of 32",  "1º E",              "3º (A/B/C/D/F)",     "Gillette Stadium",         "Foxborough, MA"),    # 4:30pm ET
    (9075, "2026-06-30T01:00:00+00:00", "Round of 32",  "1º F",              "2º C",               "Estadio BBVA",             "Monterrey"),         # 9pm ET 29/jun
    (9076, "2026-06-29T17:00:00+00:00", "Round of 32",  "1º C",              "2º F",               "NRG Stadium",              "Houston, TX"),       # 1pm ET
    (9077, "2026-06-30T21:00:00+00:00", "Round of 32",  "1º I",              "3º (C/D/F/G/H)",     "MetLife Stadium",          "East Rutherford, NJ"), # 5pm ET
    (9078, "2026-06-30T17:00:00+00:00", "Round of 32",  "2º E",              "2º I",               "AT&T Stadium",             "Arlington, TX"),     # 1pm ET
    (9079, "2026-07-01T01:00:00+00:00", "Round of 32",  "1º A",              "3º (C/E/F/H/I)",     "Estadio Azteca",           "Mexico City"),       # 9pm ET 30/jun
    (9080, "2026-07-01T16:00:00+00:00", "Round of 32",  "1º L",              "3º (E/H/I/J/K)",     "Mercedes-Benz Stadium",    "Atlanta, GA"),       # 12pm ET
    (9081, "2026-07-02T00:00:00+00:00", "Round of 32",  "1º D",              "3º (B/E/F/I/J)",     "Levi's Stadium",           "Santa Clara, CA"),   # 8pm ET 1/jul
    (9082, "2026-07-01T20:00:00+00:00", "Round of 32",  "1º G",              "3º (A/E/H/I/J)",     "Lumen Field",              "Seattle, WA"),       # 4pm ET
    (9083, "2026-07-02T23:00:00+00:00", "Round of 32",  "2º K",              "2º L",               "BMO Field",                "Toronto"),           # 7pm ET
    (9084, "2026-07-02T19:00:00+00:00", "Round of 32",  "1º H",              "2º J",               "SoFi Stadium",             "Los Angeles, CA"),   # 3pm ET
    (9085, "2026-07-03T03:00:00+00:00", "Round of 32",  "1º B",              "3º (E/F/G/I/J)",     "BC Place",                 "Vancouver"),         # 11pm ET 2/jul
    (9086, "2026-07-03T22:00:00+00:00", "Round of 32",  "1º J",              "2º H",               "Hard Rock Stadium",        "Miami Gardens, FL"), # 6pm ET
    (9087, "2026-07-04T01:30:00+00:00", "Round of 32",  "1º K",              "3º (D/E/I/J/L)",     "Arrowhead Stadium",        "Kansas City, MO"),   # 9:30pm ET 3/jul
    (9088, "2026-07-03T18:00:00+00:00", "Round of 32",  "2º D",              "2º G",               "AT&T Stadium",             "Arlington, TX"),     # 2pm ET

    # ── OITAVAS DE FINAL ─────────────────────────────────────────────────────
    (9089, "2026-07-04T21:00:00+00:00", "Round of 16",  "Ven. J74",          "Ven. J77",           "Lincoln Financial Field",  "Philadelphia, PA"),  # 5pm ET
    (9090, "2026-07-04T17:00:00+00:00", "Round of 16",  "Ven. J73",          "Ven. J75",           "NRG Stadium",              "Houston, TX"),       # 1pm ET
    (9091, "2026-07-05T20:00:00+00:00", "Round of 16",  "Ven. J76",          "Ven. J78",           "MetLife Stadium",          "East Rutherford, NJ"), # 4pm ET
    (9092, "2026-07-06T00:00:00+00:00", "Round of 16",  "Ven. J79",          "Ven. J80",           "Estadio Azteca",           "Mexico City"),       # 8pm ET 5/jul
    (9093, "2026-07-06T19:00:00+00:00", "Round of 16",  "Ven. J83",          "Ven. J84",           "AT&T Stadium",             "Arlington, TX"),     # 3pm ET
    (9094, "2026-07-07T00:00:00+00:00", "Round of 16",  "Ven. J81",          "Ven. J82",           "Lumen Field",              "Seattle, WA"),       # 8pm ET 6/jul
    (9095, "2026-07-07T16:00:00+00:00", "Round of 16",  "Ven. J86",          "Ven. J88",           "Mercedes-Benz Stadium",    "Atlanta, GA"),       # 12pm ET
    (9096, "2026-07-07T20:00:00+00:00", "Round of 16",  "Ven. J85",          "Ven. J87",           "BC Place",                 "Vancouver"),         # 4pm ET

    # ── QUARTAS DE FINAL ─────────────────────────────────────────────────────
    (9097, "2026-07-09T20:00:00+00:00", "Quarter-finals","Ven. J89",         "Ven. J90",           "Gillette Stadium",         "Foxborough, MA"),    # 4pm ET
    (9098, "2026-07-10T19:00:00+00:00", "Quarter-finals","Ven. J93",         "Ven. J94",           "SoFi Stadium",             "Los Angeles, CA"),   # 3pm ET
    (9099, "2026-07-11T21:00:00+00:00", "Quarter-finals","Ven. J91",         "Ven. J92",           "Hard Rock Stadium",        "Miami Gardens, FL"), # 5pm ET
    (9100, "2026-07-12T01:00:00+00:00", "Quarter-finals","Ven. J95",         "Ven. J96",           "Arrowhead Stadium",        "Kansas City, MO"),   # 9pm ET 11/jul

    # ── SEMIFINAIS ───────────────────────────────────────────────────────────
    (9101, "2026-07-14T19:00:00+00:00", "Semi-finals",   "Ven. J97",         "Ven. J98",           "AT&T Stadium",             "Arlington, TX"),     # 3pm ET
    (9102, "2026-07-15T19:00:00+00:00", "Semi-finals",   "Ven. J99",         "Ven. J100",          "Mercedes-Benz Stadium",    "Atlanta, GA"),       # 3pm ET

    # ── DISPUTA DE 3º LUGAR ──────────────────────────────────────────────────
    (9103, "2026-07-18T21:00:00+00:00", "3rd Place Final","Perd. J101",       "Perd. J102",         "Hard Rock Stadium",        "Miami Gardens, FL"), # 5pm ET

    # ── FINAL ────────────────────────────────────────────────────────────────
    (9104, "2026-07-19T19:00:00+00:00", "Final",          "Ven. J101",        "Ven. J102",          "MetLife Stadium",          "East Rutherford, NJ"), # 3pm ET
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
