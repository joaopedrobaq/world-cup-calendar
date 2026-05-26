"""
Gera o arquivo worldcup.ics a partir dos fixtures em data/fixtures.json
e das transmissões em data/broadcasts.json.

Uso:
    python scripts/build_calendar.py
"""

import os
import sys
from datetime import timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ics import Calendar, Event

import config
from scripts.helpers import (
    format_match_title,
    load_json,
    save_json,
    translate_round,
    build_uid,
    iso_to_datetime,
    utc_now,
)

# Duração padrão de um jogo (90 min + intervalo + acréscimos)
DEFAULT_DURATION = timedelta(minutes=110)


# ---------------------------------------------------------------------------
# Construção da descrição do evento
# ---------------------------------------------------------------------------

def build_description(fixture: dict, broadcast_names: list[str]) -> str:
    """
    Monta o texto de descrição do evento ICS.
    Todos os campos são opcionais — campos vazios são omitidos.
    """
    lines: list[str] = []

    city = fixture.get("venue", {}).get("city", "")
    stadium = fixture.get("venue", {}).get("name", "")
    round_label = translate_round(fixture.get("round", ""))

    if city:
        lines.append(f"Cidade-sede: {city}")
    if stadium:
        lines.append(f"Estádio: {stadium}")
    if round_label:
        lines.append(f"Fase: {round_label}")

    if broadcast_names:
        lines.append("")
        lines.append("Transmissão no Brasil:")
        for channel in broadcast_names:
            lines.append(f"• {channel}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Títulos dinâmicos (fase de grupos vs. mata-mata)
# ---------------------------------------------------------------------------

def resolve_team_name(team: dict) -> str:
    """
    Retorna o nome definitivo do time para exibição no título.
    Se o nome for vazio ou placeholder (TBD), retorna string vazia
    para que o caller use o placeholder de fase.
    """
    name = (team.get("name") or "").strip()
    if name.lower() in ("", "tbd", "to be defined"):
        return ""
    return name


def build_event_title(fixture: dict) -> str:
    """
    Determina o título mais informativo possível para o jogo:

    - Ambos conhecidos  → 'Brasil 🇧🇷 x 🇫🇷 França'
    - Um desconhecido   → 'Brasil 🇧🇷 x 2º Grupo B'   (placeholder do outro)
    - Nenhum conhecido  → placeholder completo da rodada
    """
    home = resolve_team_name(fixture.get("home", {}))
    away = resolve_team_name(fixture.get("away", {}))

    # Placeholder extraído do campo 'round' quando times ainda não definidos
    round_raw = fixture.get("round", "")
    placeholder = _round_placeholder(round_raw)

    if home and away:
        return format_match_title(home, away)
    if home and not away:
        return f"{format_match_title(home, '')} x {placeholder}".strip(" x ")
    if not home and away:
        return f"{placeholder} x {format_match_title('', away)}".strip("x ").strip()

    # Nenhum time definido — usa placeholder genérico da fase
    return placeholder or f"Jogo {fixture.get('id', '')}"


def _round_placeholder(round_str: str) -> str:
    """
    Converte a string de rodada da API em placeholder legível.
    Ex.: 'Quarter-finals - 1' → 'Quartas de Final 1'
         'Group Stage - 1'    → 'Fase de Grupos'
    """
    label = translate_round(round_str)
    # Extrai número da rodada quando presente (ex.: 'Rodada de 32 - 3')
    parts = round_str.split(" - ")
    if len(parts) > 1 and parts[-1].strip().isdigit():
        return f"{label} {parts[-1].strip()}"
    return label


# ---------------------------------------------------------------------------
# Construção de um Event ICS a partir de um fixture
# ---------------------------------------------------------------------------

def fixture_to_event(fixture: dict, broadcasts: dict[str, list[str]]) -> Event | None:
    """
    Converte um fixture normalizado em um objeto Event da lib ics.
    Retorna None se o fixture não tiver data válida.
    """
    date_str = fixture.get("date")
    if not date_str:
        return None

    try:
        begin = iso_to_datetime(date_str)
    except ValueError as exc:
        print(f"[build] Data inválida no fixture {fixture.get('id')}: {exc}")
        return None

    fid = fixture.get("id")
    broadcast_names: list[str] = broadcasts.get(str(fid), config.DEFAULT_BROADCASTS)

    event = Event()
    event.uid = build_uid(fid)
    event.name = build_event_title(fixture)
    event.begin = begin
    event.duration = DEFAULT_DURATION
    event.description = build_description(fixture, broadcast_names)
    event.location = fixture.get("venue", {}).get("name", "")

    return event


# ---------------------------------------------------------------------------
# Geração do calendário completo
# ---------------------------------------------------------------------------

def build_calendar(fixtures: list[dict], broadcasts: dict[str, list[str]]) -> Calendar:
    """Cria o objeto Calendar com todos os eventos."""
    cal = Calendar()
    # Metadados do calendário
    cal.creator = f"-//joaopedrobaq//{config.CALENDAR_NAME}//EN"

    skipped = 0
    for fixture in fixtures:
        event = fixture_to_event(fixture, broadcasts)
        if event is None:
            skipped += 1
            continue
        cal.events.add(event)

    total = len(fixtures)
    added = total - skipped
    print(f"[build] {added}/{total} eventos adicionados ao calendário ({skipped} sem data).")
    return cal


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def main() -> None:
    # Carrega fixtures
    fixtures_data = load_json(config.FIXTURES_FILE)
    if not fixtures_data:
        print(
            f"[build] Arquivo {config.FIXTURES_FILE} não encontrado ou vazio.\n"
            "Execute primeiro: python scripts/fetch_matches.py",
            file=sys.stderr,
        )
        sys.exit(1)

    fixtures: list[dict] = (
        fixtures_data.get("fixtures", [])
        if isinstance(fixtures_data, dict)
        else fixtures_data
    )

    # Carrega mapeamento de transmissões
    broadcasts_raw = load_json(config.BROADCASTS_FILE)
    broadcasts: dict[str, list[str]] = broadcasts_raw if isinstance(broadcasts_raw, dict) else {}

    # Gera calendário
    cal = build_calendar(fixtures, broadcasts)

    # Salva .ics
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    with open(config.OUTPUT_ICS, "w", encoding="utf-8") as f:
        f.writelines(cal)

    print(f"[build] Calendário salvo em {config.OUTPUT_ICS}")

    # Atualiza cache com timestamp da última geração
    save_json(
        config.CACHE_FILE,
        {
            "last_build": utc_now().isoformat(),
            "events_count": len(cal.events),
        },
    )


if __name__ == "__main__":
    main()
