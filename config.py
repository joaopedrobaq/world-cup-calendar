"""
Configurações centrais do projeto Copa do Mundo 2026.
Todas as constantes e leituras de ambiente ficam aqui.
"""

import os

# ---------------------------------------------------------------------------
# API-Football
# ---------------------------------------------------------------------------

API_KEY: str = os.environ.get("API_FOOTBALL_KEY", "")
API_HOST: str = "v3.football.api-sports.io"
API_BASE_URL: str = f"https://{API_HOST}"

# ID da liga Copa do Mundo 2026 na API-Football
# 1: FIFA World Cup  (verificar antes do torneio se o ID mudou)
WORLD_CUP_LEAGUE_ID: int = 1
WORLD_CUP_SEASON: int = 2026

# ---------------------------------------------------------------------------
# Calendário ICS
# ---------------------------------------------------------------------------

CALENDAR_NAME: str = "🏆 Copa do Mundo 2026"
CALENDAR_DESCRIPTION: str = (
    "Calendário completo da Copa do Mundo 2026 com horários, "
    "estádios e transmissões no Brasil."
)
CALENDAR_TIMEZONE: str = "UTC"

# UID base para eventos — garante que re-importações não dupliquem no Google Calendar
UID_DOMAIN: str = "worldcup2026.joaopedrobaq.github.io"

# ---------------------------------------------------------------------------
# Caminhos de arquivo
# ---------------------------------------------------------------------------

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
DATA_DIR: str = os.path.join(BASE_DIR, "data")
OUTPUT_DIR: str = os.path.join(BASE_DIR, "docs")

FIXTURES_FILE: str = os.path.join(DATA_DIR, "fixtures.json")
BROADCASTS_FILE: str = os.path.join(DATA_DIR, "broadcasts.json")
CACHE_FILE: str = os.path.join(DATA_DIR, "cache.json")
OUTPUT_ICS: str = os.path.join(OUTPUT_DIR, "worldcup.ics")

# ---------------------------------------------------------------------------
# Transmissão padrão (fallback quando fixture não está mapeado)
# ---------------------------------------------------------------------------

DEFAULT_BROADCASTS: list[str] = ["SporTV", "CazéTV"]

# ---------------------------------------------------------------------------
# Bandeiras por país (ISO 3166-1 alpha-2 → emoji)
# Expandir conforme os 48 classificados forem conhecidos.
# ---------------------------------------------------------------------------

COUNTRY_FLAGS: dict[str, str] = {
    # Grupo A
    "Mexico": "🇲🇽",
    "South Africa": "🇿🇦",
    "South Korea": "🇰🇷",
    "Czech Republic": "🇨🇿",
    # Grupo B
    "Canada": "🇨🇦",
    "Bosnia & Herzegovina": "🇧🇦",
    "Qatar": "🇶🇦",
    "Switzerland": "🇨🇭",
    # Grupo C
    "Brazil": "🇧🇷",
    "Morocco": "🇲🇦",
    "Haiti": "🇭🇹",
    "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    # Grupo D
    "USA": "🇺🇸",
    "Paraguay": "🇵🇾",
    "Australia": "🇦🇺",
    "Turkey": "🇹🇷",
    # Grupo E
    "Germany": "🇩🇪",
    "Curacao": "🇨🇼",
    "Ivory Coast": "🇨🇮",
    "Ecuador": "🇪🇨",
    # Grupo F
    "Netherlands": "🇳🇱",
    "Japan": "🇯🇵",
    "Sweden": "🇸🇪",
    "Tunisia": "🇹🇳",
    # Grupo G
    "Belgium": "🇧🇪",
    "Egypt": "🇪🇬",
    "Iran": "🇮🇷",
    "New Zealand": "🇳🇿",
    # Grupo H
    "Spain": "🇪🇸",
    "Cape Verde": "🇨🇻",
    "Saudi Arabia": "🇸🇦",
    "Uruguay": "🇺🇾",
    # Grupo I
    "France": "🇫🇷",
    "Senegal": "🇸🇳",
    "Iraq": "🇮🇶",
    "Norway": "🇳🇴",
    # Grupo J
    "Argentina": "🇦🇷",
    "Algeria": "🇩🇿",
    "Austria": "🇦🇹",
    "Jordan": "🇯🇴",
    # Grupo K
    "Portugal": "🇵🇹",
    "DR Congo": "🇨🇩",
    "Uzbekistan": "🇺🇿",
    "Colombia": "🇨🇴",
    # Grupo L
    "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Croatia": "🇭🇷",
    "Ghana": "🇬🇭",
    "Panama": "🇵🇦",
}
