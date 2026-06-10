# 🏆 Copa do Mundo 2026 — Calendário ICS

Calendário completo da Copa do Mundo 2026 para Google Calendar, Apple Calendar e qualquer app compatível com `.ics`.

---

## Adicionar ao seu calendário

[![Adicionar ao Google Calendar](https://img.shields.io/badge/Google%20Calendar-Adicionar%20Calendário-4285F4?style=for-the-badge&logo=googlecalendar&logoColor=white)](https://calendar.google.com/calendar/r/settings/addbyurl?url=https%3A%2F%2Fjoaopedrobaq.github.io%2Fworld-cup-calendar%2Fworldcup.ics)

[![Adicionar ao Apple Calendar (iOS / macOS)](https://img.shields.io/badge/Apple%20Calendar-Adicionar%20Calendário-000000?style=for-the-badge&logo=apple&logoColor=white)](webcal://joaopedrobaq.github.io/world-cup-calendar/worldcup.ics)

> **iOS/macOS:** o link acima abre diretamente no app Calendário e pergunta se deseja assinar.  
> **Google Calendar:** você será redirecionado para a página de adicionar por URL, já preenchida.  
> O Google Cache leva até 24h para atualizar — se precisar forçar, remova e adicione novamente.

### Adicionar manualmente (qualquer app)

Cole esta URL no seu app de calendário em **"Assinar por URL"** ou **"Adicionar calendário de internet"**:

```
https://joaopedrobaq.github.io/world-cup-calendar/worldcup.ics
```

---

## O que está incluído

- Todos os **104 jogos** da Copa do Mundo 2026
- Fase de grupos + Mata-mata (placeholders atualizados conforme classificação)
- Horários em **UTC** (o app de calendário converte para seu fuso)
- Transmissões no Brasil (TV Globo, SporTV, CazéTV) por jogo

### Formato dos eventos

**Título** — código de 3 letras em português para caber no grid do calendário:
```
BRA x ALE
```

**Descrição** — título completo com bandeiras, grupo (fase de grupos), cidade-sede, estádio e transmissões:
```
Brasil 🇧🇷 x 🇩🇪 Alemanha

Grupo C

Cidade-sede: Los Angeles, CA
Estádio: SoFi Stadium
Fase: Fase de grupos

Transmissão no Brasil:
• CazéTV
```

**Local** — cidade-sede metropolitana + UF/Província, não o município real do estádio:
```
SoFi Stadium, Los Angeles, CA   (não "Inglewood")
AT&T Stadium, Dallas, TX        (não "Arlington")
MetLife Stadium, New York, NY   (não "East Rutherford")
```

---

## Estrutura do projeto

```
world-cup-calendar/
│
├── data/
│   ├── fixtures.json         # Jogos (gerado por fetch_matches.py ou build_static_fixtures.py)
│   ├── broadcasts.json       # Mapeamento de transmissões por fixture_id
│   └── cache.json            # Timestamp da última geração
│
├── docs/
│   └── worldcup.ics          # Arquivo publicado no GitHub Pages
│
├── scripts/
│   ├── fetch_matches.py      # Busca jogos na API-Football
│   ├── build_static_fixtures.py  # Gera fixtures.json a partir de dados estáticos
│   ├── build_calendar.py     # Gera o .ics a partir de fixtures.json
│   ├── update_broadcasts.py  # Gerencia broadcasts.json
│   ├── editor.py             # Editor visual de jogos e transmissões
│   └── helpers.py            # Utilitários compartilhados
│
└── config.py                 # Configurações, bandeiras, códigos e mapeamento de estádios
```

---

## Setup local

### Pré-requisitos

- Python 3.11+

### Instalação

```bash
git clone https://github.com/joaopedrobaq/world-cup-calendar.git
cd world-cup-calendar

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### Gerar o calendário

```bash
# Gera o .ics a partir dos fixtures já existentes em data/fixtures.json
python scripts/build_calendar.py

# O arquivo será salvo em docs/worldcup.ics
```

### Atualizar jogos via API (requer chave paga)

```bash
# Configurar a API key
# Windows PowerShell:
$env:API_FOOTBALL_KEY = "sua_chave_aqui"
# macOS/Linux:
export API_FOOTBALL_KEY="sua_chave_aqui"

# Buscar jogos na API-Football
python scripts/fetch_matches.py
```

---

## GitHub Pages

1. Acesse **Settings → Pages** no repositório.
2. Em **Source**, selecione **Deploy from a branch → `main` → `/docs`**.

A URL pública será:

```
https://joaopedrobaq.github.io/world-cup-calendar/worldcup.ics
```

---

## Gerenciar transmissões

O mapeamento de canais por jogo é semi-manual. Use o script de utilidade:

```bash
# Ver todos os mapeamentos
python scripts/update_broadcasts.py list

# Definir canais para um jogo (ID do fixture)
python scripts/update_broadcasts.py set 9001 "TV Globo" "SporTV" "CazéTV"

# Remover mapeamento de um jogo
python scripts/update_broadcasts.py remove 9001
```

Jogos sem mapeamento explícito usam o padrão definido em `config.py → DEFAULT_BROADCASTS`.

---

## Contribuindo

Pull requests são bem-vindos. Áreas prioritárias:

- Completar mapeamento de transmissões (`data/broadcasts.json`)
- Atualizar fixtures conforme classificação oficial para o mata-mata
