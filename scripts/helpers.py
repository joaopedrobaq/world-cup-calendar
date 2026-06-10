"""
Funções utilitárias compartilhadas entre os scripts.
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Any

import config


# ---------------------------------------------------------------------------
# I/O de JSON
# ---------------------------------------------------------------------------

def load_json(path: str) -> Any:
    """Carrega um arquivo JSON, retornando {} ou [] se não existir."""
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: Any, indent: int = 2) -> None:
    """Salva data como JSON formatado no caminho indicado."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


# ---------------------------------------------------------------------------
# Bandeiras e nomes de países
# ---------------------------------------------------------------------------

def country_flag(country_name: str) -> str:
    """Retorna o emoji de bandeira para o país, ou string vazia se desconhecido."""
    return config.COUNTRY_FLAGS.get(country_name, "")


def country_code(country_name: str) -> str:
    """Retorna o código FIFA de 3 letras para o país, ou string vazia."""
    return config.COUNTRY_CODES.get(country_name, "")


def format_match_code(home: str, away: str) -> str:
    """Monta o título curto do evento: 'BRA x FRA'. Fallback para o nome se não houver código."""
    home_part = country_code(home) or home
    away_part = country_code(away) or away
    return f"{home_part} x {away_part}"


def format_team_name(country_name: str) -> str:
    """
    Formata nome do time com bandeira: 'Brasil 🇧🇷'
    Se a bandeira não for conhecida, retorna só o nome.
    """
    flag = country_flag(country_name)
    if flag:
        return f"{country_name} {flag}"
    return country_name


def format_match_title(home: str, away: str) -> str:
    """
    Monta o título do evento no padrão:
      'Brasil 🇧🇷 x 🇫🇷 França'

    Aceita nomes de times já formatados (com bandeira) ou crus.
    """
    home_flag = country_flag(home)
    away_flag = country_flag(away)

    home_part = f"{home} {home_flag}".strip() if home_flag else home
    away_part = f"{away_flag} {away}".strip() if away_flag else away

    return f"{home_part} x {away_part}"


# ---------------------------------------------------------------------------
# Fases do torneio
# ---------------------------------------------------------------------------

ROUND_LABELS: dict[str, str] = {
    "Group Stage": "Fase de grupos",
    "Round of 32": "Rodada de 32",       # Copa do Mundo 2026 tem 32 eliminatórias
    "Round of 16": "Oitavas de final",
    "Quarter-finals": "Quartas de final",
    "Semi-finals": "Semifinais",
    "3rd Place Final": "Disputa de 3º lugar",
    "Final": "Final",
}


def translate_round(api_round: str) -> str:
    """Traduz o nome da fase retornado pela API para português."""
    for key, label in ROUND_LABELS.items():
        if key.lower() in api_round.lower():
            return label
    return api_round


# ---------------------------------------------------------------------------
# UIDs estáveis para eventos ICS
# ---------------------------------------------------------------------------

def build_uid(fixture_id: int | str) -> str:
    """
    Cria um UID único e estável para o evento ICS.
    O mesmo fixture_id sempre gera o mesmo UID,
    evitando duplicatas no Google Calendar em re-importações.
    """
    return f"fixture-{fixture_id}@{config.UID_DOMAIN}"


# ---------------------------------------------------------------------------
# Validação de configuração
# ---------------------------------------------------------------------------

def require_api_key() -> str:
    """Aborta com mensagem amigável se a API key não estiver configurada."""
    key = config.API_KEY
    if not key:
        print(
            "Erro: variável de ambiente API_FOOTBALL_KEY não definida.\n"
            "Configure o secret no GitHub Actions ou exporte localmente:\n"
            "  export API_FOOTBALL_KEY=sua_chave_aqui",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


# ---------------------------------------------------------------------------
# Datas e horários
# ---------------------------------------------------------------------------

def utc_now() -> datetime:
    """Retorna o datetime atual em UTC."""
    return datetime.now(tz=timezone.utc)


def iso_to_datetime(iso_string: str) -> datetime:
    """
    Converte string ISO 8601 da API para datetime UTC.
    Exemplo: '2026-06-11T18:00:00+00:00' → datetime(2026, 6, 11, 18, 0, tzinfo=UTC)
    """
    dt = datetime.fromisoformat(iso_string)
    return dt.astimezone(timezone.utc)
