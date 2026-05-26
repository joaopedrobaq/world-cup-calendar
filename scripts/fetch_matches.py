"""
Busca os fixtures da Copa do Mundo 2026 na API-Football
e salva em data/fixtures.json.

Uso:
    python scripts/fetch_matches.py
    python scripts/fetch_matches.py --dry-run   # usa cache existente sem chamar a API
"""

import argparse
import sys
import os

# Permite importar config e scripts de qualquer diretório
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

import config
from scripts.helpers import (
    load_json,
    require_api_key,
    save_json,
    utc_now,
)


# ---------------------------------------------------------------------------
# Cliente da API-Football
# ---------------------------------------------------------------------------

def build_headers(api_key: str) -> dict[str, str]:
    return {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": config.API_HOST,
    }


def fetch_fixtures(api_key: str) -> list[dict]:
    """
    Consulta o endpoint /fixtures com os parâmetros da Copa do Mundo 2026.
    Retorna a lista de fixtures brutos da API.
    """
    url = f"{config.API_BASE_URL}/fixtures"
    params = {
        "league": config.WORLD_CUP_LEAGUE_ID,
        "season": config.WORLD_CUP_SEASON,
    }
    headers = build_headers(api_key)

    print(f"[fetch] GET {url} | league={params['league']} season={params['season']}")

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
    except requests.exceptions.RequestException as exc:
        print(f"[fetch] Falha na requisição HTTP: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"[fetch] HTTP {response.status_code}")

    if not response.ok:
        print(f"[fetch] Erro HTTP {response.status_code}:", file=sys.stderr)
        print(response.text[:500], file=sys.stderr)
        response.raise_for_status()

    body = response.json()

    # API-Football retorna erros como {"errors": {"token": "..."}}
    if body.get("errors"):
        errors = body["errors"]
        print(f"[fetch] Erro retornado pela API: {errors}", file=sys.stderr)
        if "token" in str(errors).lower() or "key" in str(errors).lower():
            print(
                "[fetch] Verifique se o secret API_FOOTBALL_KEY está correto no GitHub.",
                file=sys.stderr,
            )
        sys.exit(1)

    # Informações de quota (útil para debug)
    remaining = response.headers.get("x-ratelimit-requests-remaining", "?")
    print(f"[fetch] Requisições restantes na cota: {remaining}")

    fixtures: list[dict] = body.get("response", [])
    print(f"[fetch] {len(fixtures)} fixtures recebidos.")

    if len(fixtures) == 0:
        print(
            f"[fetch] AVISO: Nenhum fixture encontrado para league={config.WORLD_CUP_LEAGUE_ID} "
            f"season={config.WORLD_CUP_SEASON}. Verifique o ID da liga na API.",
            file=sys.stderr,
        )

    return fixtures


# ---------------------------------------------------------------------------
# Normalização dos dados brutos
# ---------------------------------------------------------------------------

def normalize_fixture(raw: dict) -> dict:
    """
    Extrai apenas os campos necessários de cada fixture,
    garantindo um schema estável independente de mudanças na API.
    """
    fixture = raw.get("fixture", {})
    league = raw.get("league", {})
    teams = raw.get("teams", {})
    goals = raw.get("goals", {})
    venue = fixture.get("venue", {})

    return {
        "id": fixture.get("id"),
        "date": fixture.get("date"),                    # ISO 8601 UTC
        "status": fixture.get("status", {}).get("short"),  # NS, 1H, HT, 2H, FT …
        "round": league.get("round", ""),
        "home": {
            "id": teams.get("home", {}).get("id"),
            "name": teams.get("home", {}).get("name", ""),
            "winner": teams.get("home", {}).get("winner"),
        },
        "away": {
            "id": teams.get("away", {}).get("id"),
            "name": teams.get("away", {}).get("name", ""),
            "winner": teams.get("away", {}).get("winner"),
        },
        "score": {
            "home": goals.get("home"),
            "away": goals.get("away"),
        },
        "venue": {
            "name": venue.get("name", ""),
            "city": venue.get("city", ""),
        },
    }


# ---------------------------------------------------------------------------
# Persistência — preserva IDs fixos e mescla com dados anteriores
# ---------------------------------------------------------------------------

def merge_fixtures(existing: list[dict], fresh: list[dict]) -> list[dict]:
    """
    Mescla fixtures novos com os existentes.
    Para cada fixture, dados novos prevalecem; fixtures que
    desapareceram da API são mantidos para não perder o histórico.
    """
    existing_by_id: dict[int, dict] = {f["id"]: f for f in existing if f.get("id")}
    for fixture in fresh:
        fid = fixture.get("id")
        if fid is not None:
            existing_by_id[fid] = fixture
    return sorted(existing_by_id.values(), key=lambda f: (f.get("date") or "", f["id"]))


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Busca fixtures da Copa 2026.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Usa o cache local sem chamar a API.",
    )
    args = parser.parse_args()

    existing_data = load_json(config.FIXTURES_FILE)
    existing_fixtures: list[dict] = existing_data.get("fixtures", []) if isinstance(existing_data, dict) else []

    if args.dry_run:
        print("[fetch] Modo dry-run: usando cache existente sem chamar a API.")
        fresh_fixtures: list[dict] = []
    else:
        api_key = require_api_key()
        raw_fixtures = fetch_fixtures(api_key)
        fresh_fixtures = [normalize_fixture(r) for r in raw_fixtures]

    merged = merge_fixtures(existing_fixtures, fresh_fixtures)

    payload = {
        "updated_at": utc_now().isoformat(),
        "total": len(merged),
        "fixtures": merged,
    }
    save_json(config.FIXTURES_FILE, payload)
    print(f"[fetch] {len(merged)} fixtures salvos em {config.FIXTURES_FILE}")


if __name__ == "__main__":
    main()
