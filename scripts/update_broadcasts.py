"""
Utilitário para gerenciar o mapeamento de transmissões (broadcasts.json).

Operações disponíveis:
    python scripts/update_broadcasts.py list
    python scripts/update_broadcasts.py set <fixture_id> <canal1> [canal2 ...]
    python scripts/update_broadcasts.py remove <fixture_id>
    python scripts/update_broadcasts.py reset         # restaura template vazio

O mapeamento é manual/semi-manual intencionalmente — transmissões
variam por jogo e precisam de curadoria humana.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from scripts.helpers import load_json, save_json


# ---------------------------------------------------------------------------
# Operações CRUD sobre broadcasts.json
# ---------------------------------------------------------------------------

def cmd_list(broadcasts: dict) -> None:
    if not broadcasts:
        print("Nenhuma transmissão mapeada ainda.")
        return
    print(f"{'Fixture ID':<14} {'Canais'}")
    print("-" * 50)
    for fid, channels in sorted(broadcasts.items(), key=lambda x: int(x[0])):
        print(f"{fid:<14} {', '.join(channels)}")


def cmd_set(broadcasts: dict, fixture_id: str, channels: list[str]) -> dict:
    broadcasts[fixture_id] = channels
    print(f"[update] fixture {fixture_id} → {channels}")
    return broadcasts


def cmd_remove(broadcasts: dict, fixture_id: str) -> dict:
    if fixture_id in broadcasts:
        del broadcasts[fixture_id]
        print(f"[update] fixture {fixture_id} removido.")
    else:
        print(f"[update] fixture {fixture_id} não encontrado.")
    return broadcasts


def cmd_reset() -> dict:
    """Retorna um template vazio comentado como exemplo."""
    template: dict = {
        "_exemplo_fixture_id": ["TV Globo", "SporTV", "CazéTV"],
    }
    print("[update] Template de exemplo criado. Remova a chave '_exemplo_fixture_id' ao usar.")
    return template


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gerencia mapeamento de transmissões dos jogos."
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="Lista todos os mapeamentos.")

    set_parser = subparsers.add_parser("set", help="Define canais para um fixture.")
    set_parser.add_argument("fixture_id", help="ID do fixture (número).")
    set_parser.add_argument("channels", nargs="+", help="Nomes dos canais.")

    remove_parser = subparsers.add_parser("remove", help="Remove mapeamento de um fixture.")
    remove_parser.add_argument("fixture_id", help="ID do fixture.")

    subparsers.add_parser("reset", help="Recria broadcasts.json com template vazio.")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    broadcasts: dict = load_json(config.BROADCASTS_FILE)
    if not isinstance(broadcasts, dict):
        broadcasts = {}

    if args.command == "list":
        cmd_list(broadcasts)
        return

    if args.command == "set":
        broadcasts = cmd_set(broadcasts, args.fixture_id, args.channels)

    elif args.command == "remove":
        broadcasts = cmd_remove(broadcasts, args.fixture_id)

    elif args.command == "reset":
        broadcasts = cmd_reset()

    save_json(config.BROADCASTS_FILE, broadcasts)
    print(f"[update] {config.BROADCASTS_FILE} atualizado.")


if __name__ == "__main__":
    main()
