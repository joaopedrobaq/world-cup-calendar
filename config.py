"""
Configurações centrais do projeto Copa do Mundo 2026.
Todas as constantes e leituras de ambiente ficam aqui.
"""

import os

# ---------------------------------------------------------------------------
# API-Football (reservado para uso futuro com plano pago)
# ---------------------------------------------------------------------------

API_KEY: str = os.environ.get("API_FOOTBALL_KEY", "")
API_HOST: str = "v3.football.api-sports.io"
API_BASE_URL: str = f"https://{API_HOST}"

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
# Transmissão padrão
# ---------------------------------------------------------------------------

DEFAULT_BROADCASTS: list[str] = ["CazéTV"]

# ---------------------------------------------------------------------------
# Bandeiras por país — chaves em PORTUGUÊS (nomes usados nos fixtures)
# ---------------------------------------------------------------------------

COUNTRY_FLAGS: dict[str, str] = {
    # Grupo A
    "México":              "🇲🇽",
    "África do Sul":       "🇿🇦",
    "Coreia do Sul":       "🇰🇷",
    "República Tcheca":    "🇨🇿",
    # Grupo B
    "Canadá":              "🇨🇦",
    "Bósnia e Herzegovina":"🇧🇦",
    "Qatar":               "🇶🇦",
    "Suíça":               "🇨🇭",
    # Grupo C
    "Brasil":              "🇧🇷",
    "Marrocos":            "🇲🇦",
    "Haiti":               "🇭🇹",
    "Escócia":             "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    # Grupo D
    "EUA":                 "🇺🇸",
    "Paraguai":            "🇵🇾",
    "Austrália":           "🇦🇺",
    "Turquia":             "🇹🇷",
    # Grupo E
    "Alemanha":            "🇩🇪",
    "Curaçao":             "🇨🇼",
    "Costa do Marfim":     "🇨🇮",
    "Equador":             "🇪🇨",
    # Grupo F
    "Países Baixos":       "🇳🇱",
    "Japão":               "🇯🇵",
    "Suécia":              "🇸🇪",
    "Tunísia":             "🇹🇳",
    # Grupo G
    "Bélgica":             "🇧🇪",
    "Egito":               "🇪🇬",
    "Irã":                 "🇮🇷",
    "Nova Zelândia":       "🇳🇿",
    # Grupo H
    "Espanha":             "🇪🇸",
    "Cabo Verde":          "🇨🇻",
    "Arábia Saudita":      "🇸🇦",
    "Uruguai":             "🇺🇾",
    # Grupo I
    "França":              "🇫🇷",
    "Senegal":             "🇸🇳",
    "Iraque":              "🇮🇶",
    "Noruega":             "🇳🇴",
    # Grupo J
    "Argentina":           "🇦🇷",
    "Argélia":             "🇩🇿",
    "Áustria":             "🇦🇹",
    "Jordânia":            "🇯🇴",
    # Grupo K
    "Portugal":            "🇵🇹",
    "Congo DR":            "🇨🇩",
    "Uzbequistão":         "🇺🇿",
    "Colômbia":            "🇨🇴",
    # Grupo L
    "Inglaterra":          "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Croácia":             "🇭🇷",
    "Gana":                "🇬🇭",
    "Panamá":              "🇵🇦",
}
