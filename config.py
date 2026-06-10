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

# ---------------------------------------------------------------------------
# Códigos FIFA de 3 letras — chaves em PORTUGUÊS (nomes usados nos fixtures)
# ---------------------------------------------------------------------------

COUNTRY_CODES: dict[str, str] = {
    # Grupo A
    "México":               "MEX",
    "África do Sul":        "RSA",
    "Coreia do Sul":        "KOR",
    "República Tcheca":     "CZE",
    # Grupo B
    "Canadá":               "CAN",
    "Bósnia e Herzegovina": "BIH",
    "Qatar":                "QAT",
    "Suíça":                "SUI",
    # Grupo C
    "Brasil":               "BRA",
    "Marrocos":             "MAR",
    "Haiti":                "HAI",
    "Escócia":              "SCO",
    # Grupo D
    "EUA":                  "USA",
    "Paraguai":             "PAR",
    "Austrália":            "AUS",
    "Turquia":              "TUR",
    # Grupo E
    "Alemanha":             "GER",
    "Curaçao":              "CUW",
    "Costa do Marfim":      "CIV",
    "Equador":              "ECU",
    # Grupo F
    "Países Baixos":        "NED",
    "Japão":                "JPN",
    "Suécia":               "SWE",
    "Tunísia":              "TUN",
    # Grupo G
    "Bélgica":              "BEL",
    "Egito":                "EGY",
    "Irã":                  "IRN",
    "Nova Zelândia":        "NZL",
    # Grupo H
    "Espanha":              "ESP",
    "Cabo Verde":           "CPV",
    "Arábia Saudita":       "KSA",
    "Uruguai":              "URU",
    # Grupo I
    "França":               "FRA",
    "Senegal":              "SEN",
    "Iraque":               "IRQ",
    "Noruega":              "NOR",
    # Grupo J
    "Argentina":            "ARG",
    "Argélia":              "ALG",
    "Áustria":              "AUT",
    "Jordânia":             "JOR",
    # Grupo K
    "Portugal":             "POR",
    "Congo DR":             "COD",
    "Uzbequistão":          "UZB",
    "Colômbia":             "COL",
    # Grupo L
    "Inglaterra":           "ENG",
    "Croácia":              "CRO",
    "Gana":                 "GHA",
    "Panamá":               "PAN",
}

# ---------------------------------------------------------------------------
# Mapeamento estádio → cidade-sede oficial (metrópole, não município real)
# ---------------------------------------------------------------------------

VENUE_CITY_MAP: dict[str, str] = {
    "AT&T Stadium":            "Dallas, TX",        # Arlington → Dallas metro
    "Arrowhead Stadium":       "Kansas City, MO",
    "BC Place":                "Vancouver, BC",
    "BMO Field":               "Toronto, ON",
    "Estadio Akron":           "Guadalajara",
    "Estadio Azteca":          "Cidade do México",
    "Estadio BBVA":            "Monterrey",
    "Gillette Stadium":        "Boston, MA",        # Foxborough → Boston metro
    "Hard Rock Stadium":       "Miami, FL",         # Miami Gardens → Miami
    "Levi's Stadium":          "San Francisco, CA", # Santa Clara → SF Bay Area
    "Lincoln Financial Field": "Philadelphia, PA",
    "Lumen Field":             "Seattle, WA",
    "Mercedes-Benz Stadium":   "Atlanta, GA",
    "MetLife Stadium":         "New York, NY",      # East Rutherford → NY metro
    "NRG Stadium":             "Houston, TX",
    "SoFi Stadium":            "Los Angeles, CA",
}
