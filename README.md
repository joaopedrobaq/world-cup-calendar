# 🏆 Copa do Mundo 2026 — Calendário ICS

Calendário automático da Copa do Mundo 2026 para Google Calendar, Apple Calendar e qualquer app compatível com `.ics`.

Atualizado automaticamente a cada 6 horas via GitHub Actions.

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
- Estádios e cidades-sede (EUA, México, Canadá)
- Horários em **UTC** (o app de calendário converte para seu fuso)
- Transmissões no Brasil (TV Globo, SporTV, CazéTV) por jogo

---

## Estrutura do projeto

```
world-cup-calendar/
│
├── data/
│   ├── fixtures.json       # Jogos baixados da API (não editar manualmente)
│   ├── broadcasts.json     # Mapeamento de transmissões por fixture_id
│   └── cache.json          # Timestamp da última geração
│
├── output/
│   └── worldcup.ics        # Arquivo publicado no GitHub Pages
│
├── scripts/
│   ├── fetch_matches.py    # Busca jogos na API-Football
│   ├── build_calendar.py   # Gera o .ics
│   ├── helpers.py          # Utilitários compartilhados
│   └── update_broadcasts.py # Gerencia broadcasts.json
│
├── .github/
│   └── workflows/
│       └── update.yml      # Automação GitHub Actions
│
├── config.py               # Configurações centrais
└── requirements.txt
```

---

## Setup local

### Pré-requisitos

- Python 3.12+
- Chave da [API-Football](https://www.api-football.com/) (plano gratuito é suficiente para testes)

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

### Configurar a API key localmente

```bash
# Windows PowerShell
$env:API_FOOTBALL_KEY = "sua_chave_aqui"

# macOS/Linux
export API_FOOTBALL_KEY="sua_chave_aqui"
```

### Executar

```bash
# 1. Baixar jogos da API
python scripts/fetch_matches.py

# 2. Gerar o .ics
python scripts/build_calendar.py

# O arquivo estará em output/worldcup.ics
```

---

## GitHub Pages

1. Acesse **Settings → Pages** no repositório.
2. Em **Source**, selecione **"GitHub Actions"**.
3. Faça o primeiro push — o workflow vai publicar automaticamente.

A URL pública será:

```
https://joaopedrobaq.github.io/world-cup-calendar/worldcup.ics
```

---

## GitHub Secrets

O workflow precisa de um secret para chamar a API:

1. Acesse **Settings → Secrets and variables → Actions**.
2. Clique em **"New repository secret"**.
3. Nome: `API_FOOTBALL_KEY`
4. Valor: sua chave da API-Football.

---

## Gerenciar transmissões

O mapeamento de canais por jogo é semi-manual. Use o script de utilidade:

```bash
# Ver todos os mapeamentos
python scripts/update_broadcasts.py list

# Definir canais para um jogo (ID do fixture da API)
python scripts/update_broadcasts.py set 123456 "TV Globo" "SporTV" "CazéTV"

# Remover mapeamento de um jogo
python scripts/update_broadcasts.py remove 123456
```

Jogos sem mapeamento explícito usam o padrão definido em `config.py → DEFAULT_BROADCASTS`.

---

## Automação

O workflow `update.yml` executa automaticamente:

| Gatilho         | Frequência       |
|-----------------|------------------|
| Cron schedule   | A cada 6 horas   |
| Manual dispatch | Sob demanda      |

Fluxo: **fetch → build → commit → deploy Pages**

---

## Contribuindo

Pull requests são bem-vindos. Áreas prioritárias:

- Completar mapeamento de transmissões (`data/broadcasts.json`)
- Adicionar bandeiras de países ainda não mapeados (`config.py → COUNTRY_FLAGS`)
- Melhorar resolução de placeholders no mata-mata
