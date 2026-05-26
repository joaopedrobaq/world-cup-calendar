"""
Gera data/fixtures.json a partir de dados estáticos da Copa do Mundo 2026.
Usar quando a API não está disponível (plano gratuito).

Uso:
    python scripts/build_static_fixtures.py
"""

import os
import sys
from datetime import datetime, timezone
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from scripts.helpers import save_json, utc_now

# ---------------------------------------------------------------------------
# Grupos e times (sorteio de dezembro/2024)
# ---------------------------------------------------------------------------

GROUPS: dict[str, list[str]] = {
    "A": ["USA", "Panama", "Uruguay", "Bolivia"],
    "B": ["Mexico", "Jamaica", "Senegal", "New Zealand"],
    "C": ["Germany", "Japan", "Costa Rica", "Australia"],
    "D": ["Spain", "Croatia", "Morocco", "Venezuela"],
    "E": ["France", "Belgium", "Serbia", "Algeria"],
    "F": ["Brazil", "Colombia", "Ecuador", "Cameroon"],
    "G": ["Argentina", "Chile", "Peru", "Poland"],
    "H": ["Portugal", "Turkey", "Czech Republic", "Nigeria"],
    "I": ["England", "Netherlands", "Iran", "South Korea"],
    "J": ["Canada", "Honduras", "Tunisia", "Ukraine"],
    "K": ["Switzerland", "Denmark", "Saudi Arabia", "Ghana"],
    "L": ["Italy", "Egypt", "Paraguay", "Ivory Coast"],
}

# ---------------------------------------------------------------------------
# Estádios e cidades-sede (ID estático → (nome, cidade))
# ---------------------------------------------------------------------------

VENUES: list[tuple[str, str]] = [
    ("MetLife Stadium",             "East Rutherford, NJ"),
    ("AT&T Stadium",                "Dallas, TX"),
    ("SoFi Stadium",                "Los Angeles, CA"),
    ("Rose Bowl",                   "Los Angeles, CA"),
    ("Levi's Stadium",              "San Francisco, CA"),
    ("Arrowhead Stadium",           "Kansas City, MO"),
    ("Empower Field at Mile High",  "Denver, CO"),
    ("Lumen Field",                 "Seattle, WA"),
    ("Lincoln Financial Field",     "Philadelphia, PA"),
    ("Gillette Stadium",            "Boston, MA"),
    ("Hard Rock Stadium",           "Miami, FL"),
    ("Allegiant Stadium",           "Las Vegas, NV"),
    ("Estadio Azteca",              "Mexico City"),
    ("Estadio BBVA",                "Monterrey"),
    ("Estadio Akron",               "Guadalajara"),
    ("BC Place",                    "Vancouver"),
]

# Abertura em Azteca, depois rotação pelos demais estádios
VENUE_SEQUENCE = [
    12, 13, 14,  # México (dias 1-3)
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15,  # USA + Canada
] * 10  # ciclar quantas vezes precisar

# ---------------------------------------------------------------------------
# Datas da fase de grupos — 3-4 jogos/dia, 11 jun a 26 jun
# ---------------------------------------------------------------------------

GROUP_STAGE_START = datetime(2026, 6, 11, 18, 0, tzinfo=timezone.utc)

# Distribuição de horários por dia (UTC): 3 slots
DAILY_KICKOFFS_UTC = [15, 18, 21]   # 15h, 18h, 21h UTC

def _group_stage_dates() -> list[datetime]:
    """Gera 72 horários de kickoff distribuídos de 11/06 a 26/06."""
    from datetime import timedelta
    dates: list[datetime] = []
    day_offset = 0
    slot_idx = 0
    while len(dates) < 72:
        for hour in DAILY_KICKOFFS_UTC:
            dt = GROUP_STAGE_START.replace(
                year=2026, month=6, day=11,
                hour=hour, minute=0, second=0
            ) + timedelta(days=day_offset)
            dates.append(dt)
            if len(dates) == 72:
                break
        day_offset += 1
    return dates

# ---------------------------------------------------------------------------
# Fase de grupos — gerar todos os 72 jogos
# ---------------------------------------------------------------------------

def build_group_fixtures() -> list[dict]:
    dates = _group_stage_dates()
    fixtures: list[dict] = []
    fid = 9001
    date_idx = 0

    for group_letter, teams in GROUPS.items():
        matchups = list(combinations(teams, 2))   # 6 jogos por grupo
        for home, away in matchups:
            venue_name, city = VENUES[date_idx % len(VENUES)]
            fixtures.append({
                "id": fid,
                "date": dates[date_idx].isoformat(),
                "status": "NS",
                "round": f"Group Stage - {group_letter}",
                "home": {"id": None, "name": home, "winner": None},
                "away": {"id": None, "name": away, "winner": None},
                "score": {"home": None, "away": None},
                "venue": {"name": venue_name, "city": city},
            })
            fid += 1
            date_idx += 1

    return fixtures

# ---------------------------------------------------------------------------
# Mata-mata — placeholders
# ---------------------------------------------------------------------------

KNOCKOUT_ROUNDS: list[tuple[str, str, str, str]] = [
    # (round_label, date_str, venue_name, city)
    # Round of 32 — 16 jogos (29 jun a 2 jul)
    *[("Round of 32",    f"2026-06-{d:02d}T{h:02d}:00:00+00:00",
       "MetLife Stadium", "East Rutherford, NJ")
      for d, h in [
          (29,15),(29,19),(30,15),(30,19),(1,15),(1,19),(2,15),(2,19),
          (29,22),(30,22),(1,22),(2,22),(29,18),(30,18),(1,18),(2,18),
      ]],
    # Round of 16 — 8 jogos (4-7 jul)
    *[("Round of 16",    f"2026-07-{d:02d}T{h:02d}:00:00+00:00",
       "AT&T Stadium", "Dallas, TX")
      for d, h in [(4,18),(4,22),(5,18),(5,22),(6,18),(6,22),(7,18),(7,22)]],
    # Quartas — 4 jogos (9-12 jul)
    *[("Quarter-finals", f"2026-07-{d:02d}T{h:02d}:00:00+00:00",
       "SoFi Stadium", "Los Angeles, CA")
      for d, h in [(9,18),(10,18),(11,18),(12,18)]],
    # Semis — 2 jogos (14-15 jul)
    ("Semi-finals",      "2026-07-14T22:00:00+00:00", "MetLife Stadium",  "East Rutherford, NJ"),
    ("Semi-finals",      "2026-07-15T22:00:00+00:00", "AT&T Stadium",     "Dallas, TX"),
    # 3º lugar (18 jul)
    ("3rd Place Final",  "2026-07-18T19:00:00+00:00", "Hard Rock Stadium","Miami, FL"),
    # Final (19 jul)
    ("Final",            "2026-07-19T20:00:00+00:00", "MetLife Stadium",  "East Rutherford, NJ"),
]


def build_knockout_fixtures(start_id: int) -> list[dict]:
    fixtures: list[dict] = []
    fid = start_id

    # Conta jogos por rodada para nomear os placeholders
    round_counters: dict[str, int] = {}

    for round_label, date_str, venue_name, city in KNOCKOUT_ROUNDS:
        n = round_counters.get(round_label, 0) + 1
        round_counters[round_label] = n

        home_placeholder = f"TBD ({round_label} {n}A)"
        away_placeholder = f"TBD ({round_label} {n}B)"

        fixtures.append({
            "id": fid,
            "date": date_str,
            "status": "NS",
            "round": round_label,
            "home": {"id": None, "name": home_placeholder, "winner": None},
            "away": {"id": None, "name": away_placeholder, "winner": None},
            "score": {"home": None, "away": None},
            "venue": {"name": venue_name, "city": city},
        })
        fid += 1

    return fixtures

# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def main() -> None:
    group_fixtures = build_group_fixtures()
    knockout_fixtures = build_knockout_fixtures(start_id=group_fixtures[-1]["id"] + 1)
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
