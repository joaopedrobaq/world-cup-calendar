"""
Gera data/fixtures.json com todos os 104 jogos da Copa do Mundo 2026.

Fase de grupos: 72 jogos com datas, times e estádios oficiais.
Mata-mata: 32 jogos com datas e estádios confirmados, times TBD.

Fonte: FIFA / sorteio de 5 dez 2025 em Washington D.C.

Uso:
    python scripts/build_static_fixtures.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from scripts.helpers import save_json, utc_now

# ---------------------------------------------------------------------------
# Fase de grupos — 72 jogos
# Formato: (id, "ISO_DATE_UTC", "Group Stage - X", "Casa", "Visitante", "Estádio", "Cidade")
# Horários UTC: 18:00 = ~2PM ET | 22:00 = ~6PM ET | 00:00 (dia seguinte) = ~8PM ET anterior
# ---------------------------------------------------------------------------

GROUP_FIXTURES: list[tuple] = [
    # ── GRUPO A: Mexico · South Africa · South Korea · Czech Republic ─────────
    (9001, "2026-06-11T18:00:00+00:00", "Group Stage - A", "Mexico",        "South Africa",   "Estadio Azteca",          "Mexico City"),
    (9002, "2026-06-11T22:00:00+00:00", "Group Stage - A", "South Korea",   "Czech Republic", "Estadio Akron",           "Guadalajara"),
    (9003, "2026-06-18T18:00:00+00:00", "Group Stage - A", "Czech Republic","South Africa",   "Mercedes-Benz Stadium",   "Atlanta, GA"),
    (9004, "2026-06-18T22:00:00+00:00", "Group Stage - A", "Mexico",        "South Korea",    "Estadio Akron",           "Guadalajara"),
    (9005, "2026-06-24T21:00:00+00:00", "Group Stage - A", "Czech Republic","Mexico",         "Estadio Azteca",          "Mexico City"),
    (9006, "2026-06-24T21:00:00+00:00", "Group Stage - A", "South Africa",  "South Korea",    "Estadio BBVA",            "Monterrey"),

    # ── GRUPO B: Canada · Bosnia & Herzegovina · Qatar · Switzerland ──────────
    (9007, "2026-06-12T18:00:00+00:00", "Group Stage - B", "Canada",               "Bosnia & Herzegovina", "BMO Field",     "Toronto"),
    (9008, "2026-06-12T22:00:00+00:00", "Group Stage - B", "Qatar",                "Switzerland",          "Levi's Stadium","San Jose, CA"),
    (9009, "2026-06-18T18:00:00+00:00", "Group Stage - B", "Switzerland",          "Bosnia & Herzegovina", "SoFi Stadium",  "Los Angeles, CA"),
    (9010, "2026-06-18T22:00:00+00:00", "Group Stage - B", "Canada",               "Qatar",                "BC Place",      "Vancouver"),
    (9011, "2026-06-24T17:00:00+00:00", "Group Stage - B", "Switzerland",          "Canada",               "BC Place",      "Vancouver"),
    (9012, "2026-06-24T17:00:00+00:00", "Group Stage - B", "Bosnia & Herzegovina", "Qatar",                "Lumen Field",   "Seattle, WA"),

    # ── GRUPO C: Brazil · Morocco · Haiti · Scotland ──────────────────────────
    (9013, "2026-06-13T18:00:00+00:00", "Group Stage - C", "Brazil",   "Morocco",  "Gillette Stadium",        "Boston, MA"),
    (9014, "2026-06-13T22:00:00+00:00", "Group Stage - C", "Haiti",    "Scotland", "MetLife Stadium",          "East Rutherford, NJ"),
    (9015, "2026-06-19T18:00:00+00:00", "Group Stage - C", "Brazil",   "Haiti",    "Lincoln Financial Field", "Philadelphia, PA"),
    (9016, "2026-06-19T22:00:00+00:00", "Group Stage - C", "Scotland", "Morocco",  "Gillette Stadium",        "Boston, MA"),
    (9017, "2026-06-25T00:00:00+00:00", "Group Stage - C", "Scotland", "Brazil",   "Hard Rock Stadium",       "Miami, FL"),
    (9018, "2026-06-25T00:00:00+00:00", "Group Stage - C", "Morocco",  "Haiti",    "Mercedes-Benz Stadium",   "Atlanta, GA"),

    # ── GRUPO D: USA · Paraguay · Australia · Turkey ──────────────────────────
    (9019, "2026-06-12T18:00:00+00:00", "Group Stage - D", "USA",       "Paraguay",  "SoFi Stadium",   "Los Angeles, CA"),
    (9020, "2026-06-12T22:00:00+00:00", "Group Stage - D", "Australia", "Turkey",    "BC Place",       "Vancouver"),
    (9021, "2026-06-19T18:00:00+00:00", "Group Stage - D", "Turkey",    "Paraguay",  "Levi's Stadium", "San Jose, CA"),
    (9022, "2026-06-19T22:00:00+00:00", "Group Stage - D", "USA",       "Australia", "Lumen Field",    "Seattle, WA"),
    (9023, "2026-06-25T21:00:00+00:00", "Group Stage - D", "Turkey",    "USA",       "SoFi Stadium",   "Los Angeles, CA"),
    (9024, "2026-06-25T21:00:00+00:00", "Group Stage - D", "Paraguay",  "Australia", "Levi's Stadium", "San Jose, CA"),

    # ── GRUPO E: Germany · Curacao · Ivory Coast · Ecuador ───────────────────
    (9025, "2026-06-14T18:00:00+00:00", "Group Stage - E", "Germany",     "Curacao",     "Lincoln Financial Field", "Philadelphia, PA"),
    (9026, "2026-06-14T22:00:00+00:00", "Group Stage - E", "Ivory Coast", "Ecuador",     "NRG Stadium",             "Houston, TX"),
    (9027, "2026-06-20T18:00:00+00:00", "Group Stage - E", "Germany",     "Ivory Coast", "BMO Field",               "Toronto"),
    (9028, "2026-06-20T22:00:00+00:00", "Group Stage - E", "Ecuador",     "Curacao",     "Arrowhead Stadium",       "Kansas City, MO"),
    (9029, "2026-06-25T17:00:00+00:00", "Group Stage - E", "Ecuador",     "Germany",     "Lincoln Financial Field", "Philadelphia, PA"),
    (9030, "2026-06-25T17:00:00+00:00", "Group Stage - E", "Curacao",     "Ivory Coast", "MetLife Stadium",         "East Rutherford, NJ"),

    # ── GRUPO F: Netherlands · Japan · Sweden · Tunisia ──────────────────────
    (9031, "2026-06-14T18:00:00+00:00", "Group Stage - F", "Netherlands", "Japan",       "AT&T Stadium",    "Dallas, TX"),
    (9032, "2026-06-14T22:00:00+00:00", "Group Stage - F", "Sweden",      "Tunisia",     "Estadio BBVA",    "Monterrey"),
    (9033, "2026-06-20T18:00:00+00:00", "Group Stage - F", "Netherlands", "Sweden",      "NRG Stadium",     "Houston, TX"),
    (9034, "2026-06-20T22:00:00+00:00", "Group Stage - F", "Tunisia",     "Japan",       "Estadio BBVA",    "Monterrey"),
    (9035, "2026-06-26T01:00:00+00:00", "Group Stage - F", "Tunisia",     "Netherlands", "AT&T Stadium",    "Dallas, TX"),
    (9036, "2026-06-26T01:00:00+00:00", "Group Stage - F", "Japan",       "Sweden",      "Arrowhead Stadium","Kansas City, MO"),

    # ── GRUPO G: Belgium · Egypt · Iran · New Zealand ────────────────────────
    (9037, "2026-06-15T18:00:00+00:00", "Group Stage - G", "Belgium",     "Egypt",       "SoFi Stadium",  "Los Angeles, CA"),
    (9038, "2026-06-15T22:00:00+00:00", "Group Stage - G", "Iran",        "New Zealand", "Lumen Field",   "Seattle, WA"),
    (9039, "2026-06-21T18:00:00+00:00", "Group Stage - G", "Belgium",     "Iran",        "SoFi Stadium",  "Los Angeles, CA"),
    (9040, "2026-06-21T22:00:00+00:00", "Group Stage - G", "New Zealand", "Egypt",       "BC Place",      "Vancouver"),
    (9041, "2026-06-26T21:00:00+00:00", "Group Stage - G", "New Zealand", "Belgium",     "Lumen Field",   "Seattle, WA"),
    (9042, "2026-06-26T21:00:00+00:00", "Group Stage - G", "Egypt",       "Iran",        "BC Place",      "Vancouver"),

    # ── GRUPO H: Spain · Cape Verde · Saudi Arabia · Uruguay ─────────────────
    (9043, "2026-06-15T18:00:00+00:00", "Group Stage - H", "Spain",        "Cape Verde",   "Hard Rock Stadium",     "Miami, FL"),
    (9044, "2026-06-15T22:00:00+00:00", "Group Stage - H", "Saudi Arabia", "Uruguay",      "Mercedes-Benz Stadium", "Atlanta, GA"),
    (9045, "2026-06-21T18:00:00+00:00", "Group Stage - H", "Spain",        "Saudi Arabia", "Hard Rock Stadium",     "Miami, FL"),
    (9046, "2026-06-21T22:00:00+00:00", "Group Stage - H", "Uruguay",      "Cape Verde",   "Mercedes-Benz Stadium", "Atlanta, GA"),
    (9047, "2026-06-26T17:00:00+00:00", "Group Stage - H", "Uruguay",      "Spain",        "NRG Stadium",           "Houston, TX"),
    (9048, "2026-06-26T17:00:00+00:00", "Group Stage - H", "Cape Verde",   "Saudi Arabia", "Estadio Akron",         "Guadalajara"),

    # ── GRUPO I: France · Senegal · Iraq · Norway ────────────────────────────
    (9049, "2026-06-16T18:00:00+00:00", "Group Stage - I", "France",  "Senegal", "MetLife Stadium",         "East Rutherford, NJ"),
    (9050, "2026-06-16T22:00:00+00:00", "Group Stage - I", "Iraq",    "Norway",  "Gillette Stadium",        "Boston, MA"),
    (9051, "2026-06-22T18:00:00+00:00", "Group Stage - I", "France",  "Iraq",    "MetLife Stadium",         "East Rutherford, NJ"),
    (9052, "2026-06-22T22:00:00+00:00", "Group Stage - I", "Norway",  "Senegal", "Lincoln Financial Field", "Philadelphia, PA"),
    (9053, "2026-06-27T01:00:00+00:00", "Group Stage - I", "Norway",  "France",  "Gillette Stadium",        "Boston, MA"),
    (9054, "2026-06-27T01:00:00+00:00", "Group Stage - I", "Senegal", "Iraq",    "BMO Field",               "Toronto"),

    # ── GRUPO J: Argentina · Algeria · Austria · Jordan ──────────────────────
    (9055, "2026-06-16T18:00:00+00:00", "Group Stage - J", "Argentina", "Algeria", "Arrowhead Stadium", "Kansas City, MO"),
    (9056, "2026-06-16T22:00:00+00:00", "Group Stage - J", "Austria",   "Jordan",  "Levi's Stadium",    "San Jose, CA"),
    (9057, "2026-06-22T18:00:00+00:00", "Group Stage - J", "Argentina", "Austria", "AT&T Stadium",      "Dallas, TX"),
    (9058, "2026-06-22T22:00:00+00:00", "Group Stage - J", "Jordan",    "Algeria", "Levi's Stadium",    "San Jose, CA"),
    (9059, "2026-06-27T21:00:00+00:00", "Group Stage - J", "Jordan",    "Argentina","Arrowhead Stadium","Kansas City, MO"),
    (9060, "2026-06-27T21:00:00+00:00", "Group Stage - J", "Algeria",   "Austria", "AT&T Stadium",      "Dallas, TX"),

    # ── GRUPO K: Portugal · DR Congo · Uzbekistan · Colombia ─────────────────
    (9061, "2026-06-17T18:00:00+00:00", "Group Stage - K", "Portugal",  "DR Congo",   "NRG Stadium",           "Houston, TX"),
    (9062, "2026-06-17T22:00:00+00:00", "Group Stage - K", "Uzbekistan","Colombia",   "Estadio Azteca",        "Mexico City"),
    (9063, "2026-06-23T18:00:00+00:00", "Group Stage - K", "Portugal",  "Uzbekistan", "NRG Stadium",           "Houston, TX"),
    (9064, "2026-06-23T22:00:00+00:00", "Group Stage - K", "Colombia",  "DR Congo",   "Estadio Akron",         "Guadalajara"),
    (9065, "2026-06-27T17:00:00+00:00", "Group Stage - K", "Colombia",  "Portugal",   "Hard Rock Stadium",     "Miami, FL"),
    (9066, "2026-06-27T17:00:00+00:00", "Group Stage - K", "DR Congo",  "Uzbekistan", "Mercedes-Benz Stadium", "Atlanta, GA"),

    # ── GRUPO L: England · Croatia · Ghana · Panama ───────────────────────────
    (9067, "2026-06-17T18:00:00+00:00", "Group Stage - L", "England", "Croatia", "BMO Field",               "Toronto"),
    (9068, "2026-06-17T22:00:00+00:00", "Group Stage - L", "Ghana",   "Panama",  "AT&T Stadium",            "Dallas, TX"),
    (9069, "2026-06-23T18:00:00+00:00", "Group Stage - L", "England", "Ghana",   "Gillette Stadium",        "Boston, MA"),
    (9070, "2026-06-23T22:00:00+00:00", "Group Stage - L", "Panama",  "Croatia", "BMO Field",               "Toronto"),
    (9071, "2026-06-28T01:00:00+00:00", "Group Stage - L", "Panama",  "England", "MetLife Stadium",         "East Rutherford, NJ"),
    (9072, "2026-06-28T01:00:00+00:00", "Group Stage - L", "Croatia", "Ghana",   "Lincoln Financial Field", "Philadelphia, PA"),
]

# ---------------------------------------------------------------------------
# Mata-mata — 32 jogos com estádios e datas oficiais, times TBD
# Fonte: FIFA + kickoffadventures.com
# ---------------------------------------------------------------------------

KNOCKOUT_FIXTURES: list[tuple] = [
    # ── RODADA DE 32 (16 jogos, 28 jun – 3 jul) ──────────────────────────────
    (9073, "2026-06-28T18:00:00+00:00", "Round of 32",   "SoFi Stadium",            "Los Angeles, CA"),
    (9074, "2026-06-28T22:00:00+00:00", "Round of 32",   "Gillette Stadium",        "Boston, MA"),
    (9075, "2026-06-29T18:00:00+00:00", "Round of 32",   "NRG Stadium",             "Houston, TX"),
    (9076, "2026-06-29T22:00:00+00:00", "Round of 32",   "Estadio BBVA",            "Monterrey"),
    (9077, "2026-06-30T18:00:00+00:00", "Round of 32",   "MetLife Stadium",         "East Rutherford, NJ"),
    (9078, "2026-06-30T22:00:00+00:00", "Round of 32",   "AT&T Stadium",            "Dallas, TX"),
    (9079, "2026-07-01T18:00:00+00:00", "Round of 32",   "Mercedes-Benz Stadium",   "Atlanta, GA"),
    (9080, "2026-07-01T22:00:00+00:00", "Round of 32",   "Levi's Stadium",          "San Jose, CA"),
    (9081, "2026-07-02T18:00:00+00:00", "Round of 32",   "BMO Field",               "Toronto"),
    (9082, "2026-07-02T22:00:00+00:00", "Round of 32",   "BC Place",                "Vancouver"),
    (9083, "2026-07-03T18:00:00+00:00", "Round of 32",   "Lumen Field",             "Seattle, WA"),
    (9084, "2026-07-03T22:00:00+00:00", "Round of 32",   "Hard Rock Stadium",       "Miami, FL"),
    (9085, "2026-07-04T00:00:00+00:00", "Round of 32",   "Estadio Azteca",          "Mexico City"),
    (9086, "2026-07-04T18:00:00+00:00", "Round of 32",   "Arrowhead Stadium",       "Kansas City, MO"),
    (9087, "2026-07-04T22:00:00+00:00", "Round of 32",   "Lincoln Financial Field", "Philadelphia, PA"),
    (9088, "2026-07-05T02:00:00+00:00", "Round of 32",   "Estadio Akron",           "Guadalajara"),

    # ── OITAVAS DE FINAL (8 jogos, 4–7 jul) ──────────────────────────────────
    (9089, "2026-07-05T18:00:00+00:00", "Round of 16",   "NRG Stadium",             "Houston, TX"),
    (9090, "2026-07-05T22:00:00+00:00", "Round of 16",   "MetLife Stadium",         "East Rutherford, NJ"),
    (9091, "2026-07-06T18:00:00+00:00", "Round of 16",   "Levi's Stadium",          "San Jose, CA"),
    (9092, "2026-07-06T22:00:00+00:00", "Round of 16",   "Estadio Azteca",          "Mexico City"),
    (9093, "2026-07-07T18:00:00+00:00", "Round of 16",   "AT&T Stadium",            "Dallas, TX"),
    (9094, "2026-07-07T22:00:00+00:00", "Round of 16",   "Lumen Field",             "Seattle, WA"),
    (9095, "2026-07-08T18:00:00+00:00", "Round of 16",   "Mercedes-Benz Stadium",   "Atlanta, GA"),
    (9096, "2026-07-08T22:00:00+00:00", "Round of 16",   "Lincoln Financial Field", "Philadelphia, PA"),

    # ── QUARTAS DE FINAL (4 jogos, 9–11 jul) ─────────────────────────────────
    (9097, "2026-07-09T22:00:00+00:00", "Quarter-finals","Gillette Stadium",        "Boston, MA"),
    (9098, "2026-07-10T22:00:00+00:00", "Quarter-finals","SoFi Stadium",            "Los Angeles, CA"),
    (9099, "2026-07-11T18:00:00+00:00", "Quarter-finals","Hard Rock Stadium",       "Miami, FL"),
    (9100, "2026-07-11T22:00:00+00:00", "Quarter-finals","Arrowhead Stadium",       "Kansas City, MO"),

    # ── SEMIFINAIS (2 jogos, 14–15 jul) ──────────────────────────────────────
    (9101, "2026-07-14T22:00:00+00:00", "Semi-finals",   "AT&T Stadium",            "Dallas, TX"),
    (9102, "2026-07-15T22:00:00+00:00", "Semi-finals",   "Mercedes-Benz Stadium",   "Atlanta, GA"),

    # ── 3º LUGAR (18 jul) ────────────────────────────────────────────────────
    (9103, "2026-07-18T19:00:00+00:00", "3rd Place Final","Hard Rock Stadium",      "Miami, FL"),

    # ── FINAL (19 jul — MetLife Stadium, New Jersey) ──────────────────────────
    (9104, "2026-07-19T19:00:00+00:00", "Final",         "MetLife Stadium",         "East Rutherford, NJ"),
]


# ---------------------------------------------------------------------------
# Conversão para o schema de fixture
# ---------------------------------------------------------------------------

def to_fixture(row: tuple) -> dict:
    fid, date, rnd, home, away, venue, city = row
    return {
        "id": fid,
        "date": date,
        "status": "NS",
        "round": rnd,
        "home": {"id": None, "name": home, "winner": None},
        "away": {"id": None, "name": away, "winner": None},
        "score": {"home": None, "away": None},
        "venue": {"name": venue, "city": city},
    }


def to_knockout_fixture(row: tuple) -> dict:
    fid, date, rnd, venue, city = row
    return {
        "id": fid,
        "date": date,
        "status": "NS",
        "round": rnd,
        "home": {"id": None, "name": "TBD", "winner": None},
        "away": {"id": None, "name": "TBD", "winner": None},
        "score": {"home": None, "away": None},
        "venue": {"name": venue, "city": city},
    }


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def main() -> None:
    group   = [to_fixture(r) for r in GROUP_FIXTURES]
    knockout = [to_knockout_fixture(r) for r in KNOCKOUT_FIXTURES]
    all_fixtures = group + knockout

    payload = {
        "updated_at": utc_now().isoformat(),
        "source": "static",
        "total": len(all_fixtures),
        "fixtures": all_fixtures,
    }

    save_json(config.FIXTURES_FILE, payload)
    print(f"[static] {len(group)} jogos de grupo + {len(knockout)} mata-mata = {len(all_fixtures)} total")
    print(f"[static] Salvo em {config.FIXTURES_FILE}")


if __name__ == "__main__":
    main()
