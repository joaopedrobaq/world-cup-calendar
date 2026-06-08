"""
Editor de fixtures da Copa do Mundo 2026.

Uso:
    python scripts/editor.py
"""

import io
import os
import sys
from contextlib import redirect_stdout
from datetime import datetime, timezone

import tkinter as tk
from tkinter import ttk, messagebox

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from scripts.helpers import load_json, save_json, utc_now

# Lista de países participantes (mesmos nomes usados no ICS, com bandeira automática)
TEAM_OPTIONS: list[str] = sorted(config.COUNTRY_FLAGS.keys())

# Canais de transmissão disponíveis
CHANNELS = ["CazéTV", "Globo/SporTV", "SBT"]
DEFAULT_CHANNELS = ["CazéTV"]   # marcado por padrão quando não há entrada salva


# ── I/O ────────────────────────────────────────────────────────────────────────

def load_data() -> dict:
    data = load_json(config.FIXTURES_FILE)
    return data if isinstance(data, dict) else {"fixtures": data or [], "updated_at": ""}


def save_data(data: dict) -> None:
    save_json(config.FIXTURES_FILE, {
        **data,
        "updated_at": utc_now().isoformat(),
        "total": len(data["fixtures"]),
    })


def load_broadcasts() -> dict:
    raw = load_json(config.BROADCASTS_FILE)
    if not isinstance(raw, dict):
        return {}
    # Remove chaves de metadados (começam com "_")
    return {k: v for k, v in raw.items() if not k.startswith("_")}


def save_broadcasts(broadcasts: dict) -> None:
    save_json(config.BROADCASTS_FILE, broadcasts)


def rebuild_ics() -> None:
    from scripts.build_calendar import main as build_main
    buf = io.StringIO()
    with redirect_stdout(buf):
        build_main()


# ── Helpers de exibição ────────────────────────────────────────────────────────

def fmt_date(date_str: str) -> str:
    try:
        return datetime.fromisoformat(date_str).astimezone(timezone.utc).strftime("%d/%m %H:%M")
    except Exception:
        return "—"


def fmt_score(score: dict) -> str:
    h, a = score.get("home"), score.get("away")
    return f"{h}–{a}" if h is not None else "—"


def is_today(date_str: str) -> bool:
    try:
        today = datetime.now(tz=timezone.utc).date()
        return datetime.fromisoformat(date_str).astimezone(timezone.utc).date() == today
    except Exception:
        return False


def is_group(round_str: str) -> bool:
    return "group" in round_str.lower()


# ── Aplicação ──────────────────────────────────────────────────────────────────

class EditorApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Copa do Mundo 2026 — Editor")
        self.geometry("1020x640")
        self.minsize(800, 500)

        self._data = load_data()
        self._fixtures: list[dict] = self._data.get("fixtures", [])
        self._broadcasts: dict = load_broadcasts()
        self._selected_fid: int | None = None

        self._build_ui()
        self._populate_tree()

    # ── Construção da UI ───────────────────────────────────────────────────────

    def _build_ui(self):

        # ── Toolbar ──────────────────────────────────────────────────────────
        bar = ttk.Frame(self, padding=(8, 6, 8, 4))
        bar.pack(fill="x")

        ttk.Label(bar, text="Copa do Mundo 2026", font=("Segoe UI", 12, "bold")).pack(side="left", padx=(0, 14))

        self._filter = tk.StringVar(value="todos")
        for lbl, val in [("Todos", "todos"), ("Hoje", "hoje"),
                         ("Fase de Grupos", "grupo"), ("Mata-Mata", "mata")]:
            ttk.Radiobutton(bar, text=lbl, variable=self._filter, value=val,
                            command=self._populate_tree).pack(side="left", padx=3)

        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=10)

        ttk.Label(bar, text="Buscar:").pack(side="left")
        self._search = tk.StringVar()
        self._search.trace_add("write", lambda *_: self._populate_tree())
        ttk.Entry(bar, textvariable=self._search, width=16).pack(side="left", padx=4)

        ttk.Button(bar, text="🔄  Regenerar .ics", command=self._on_rebuild).pack(side="right")

        ttk.Separator(self, orient="horizontal").pack(fill="x")

        # ── PanedWindow: lista (esq.) + editor (dir.) ─────────────────────────
        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=8, pady=6)

        # ── Lista de jogos ────────────────────────────────────────────────────
        tree_frame = ttk.Frame(paned)
        paned.add(tree_frame, weight=3)

        cols = ("data", "casa", "placar", "fora")
        self._tree = ttk.Treeview(tree_frame, columns=cols,
                                   show="tree headings", selectmode="browse")

        self._tree.heading("#0",     text="Fase")
        self._tree.heading("data",   text="Data (UTC)")
        self._tree.heading("casa",   text="Casa")
        self._tree.heading("placar", text="Placar")
        self._tree.heading("fora",   text="Visitante")

        self._tree.column("#0",     width=175, minwidth=120, stretch=False)
        self._tree.column("data",   width=95,  minwidth=80,  anchor="center", stretch=False)
        self._tree.column("casa",   width=135, minwidth=80)
        self._tree.column("placar", width=65,  minwidth=50,  anchor="center", stretch=False)
        self._tree.column("fora",   width=135, minwidth=80)

        # Verde = encerrado
        self._tree.tag_configure("ft",  foreground="#1a7a1a")
        self._tree.tag_configure("rnd", font=("Segoe UI", 9, "bold"))

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        # ── Painel de edição ──────────────────────────────────────────────────
        edit = ttk.LabelFrame(paned, text=" Editar Jogo ", padding=14)
        paned.add(edit, weight=2)
        edit.columnconfigure(1, weight=1)

        row = 0

        # Identificador do jogo selecionado
        self._lbl_id = ttk.Label(edit, text="← Selecione um jogo",
                                  foreground="gray", font=("Segoe UI", 9, "italic"))
        self._lbl_id.grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 10))
        row += 1

        ttk.Separator(edit, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        row += 1

        # Nome: casa
        ttk.Label(edit, text="Casa").grid(row=row, column=0, sticky="w", pady=3)
        self._home_var = tk.StringVar()
        ttk.Combobox(edit, textvariable=self._home_var,
                     values=TEAM_OPTIONS, state="readonly").grid(
            row=row, column=1, sticky="ew", padx=(10, 0))
        row += 1

        # Nome: visitante
        ttk.Label(edit, text="Visitante").grid(row=row, column=0, sticky="w", pady=3)
        self._away_var = tk.StringVar()
        ttk.Combobox(edit, textvariable=self._away_var,
                     values=TEAM_OPTIONS, state="readonly").grid(
            row=row, column=1, sticky="ew", padx=(10, 0))
        row += 1

        ttk.Separator(edit, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=10)
        row += 1

        # Checkbox encerrado
        self._ft_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(edit, text="Encerrado", variable=self._ft_var,
                        command=self._on_ft_toggle).grid(
            row=row, column=0, columnspan=2, sticky="w")
        row += 1

        # Placar
        frm_score = ttk.Frame(edit)
        frm_score.grid(row=row, column=0, columnspan=2, sticky="w", pady=(6, 0))
        row += 1

        ttk.Label(frm_score, text="Placar  ").pack(side="left")

        self._score_h_var = tk.IntVar(value=0)
        self._score_a_var = tk.IntVar(value=0)

        self._spin_h = ttk.Spinbox(frm_score, from_=0, to=30,
                                    textvariable=self._score_h_var,
                                    width=4, state="disabled",
                                    command=self._on_score_change)
        self._spin_h.pack(side="left", padx=(0, 4))

        ttk.Label(frm_score, text="×").pack(side="left")

        self._spin_a = ttk.Spinbox(frm_score, from_=0, to=30,
                                    textvariable=self._score_a_var,
                                    width=4, state="disabled",
                                    command=self._on_score_change)
        self._spin_a.pack(side="left", padx=(4, 0))

        # Quem avançou? — aparece apenas em empates no mata-mata
        self._ko_frame = ttk.LabelFrame(edit, text=" Quem avançou? ", padding=8)
        self._ko_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        self._ko_frame.columnconfigure(0, weight=1)
        row += 1

        self._winner_var = tk.StringVar(value="none")
        self._rb_home = ttk.Radiobutton(self._ko_frame, text="Casa",
                                         variable=self._winner_var, value="home")
        self._rb_away = ttk.Radiobutton(self._ko_frame, text="Visitante",
                                         variable=self._winner_var, value="away")
        self._rb_home.grid(row=0, column=0, sticky="w", pady=1)
        self._rb_away.grid(row=1, column=0, sticky="w", pady=1)
        self._ko_frame.grid_remove()  # oculto por padrão

        ttk.Separator(edit, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=10)
        row += 1

        # Transmissões
        ttk.Label(edit, text="Transmissões").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(0, 4))
        row += 1

        self._br_caze_var  = tk.BooleanVar(value=True)
        self._br_globo_var = tk.BooleanVar(value=False)
        self._br_sbt_var   = tk.BooleanVar(value=False)

        ttk.Checkbutton(edit, text="CazéTV",      variable=self._br_caze_var).grid(
            row=row, column=0, columnspan=2, sticky="w")
        row += 1
        ttk.Checkbutton(edit, text="Globo/SporTV", variable=self._br_globo_var).grid(
            row=row, column=0, columnspan=2, sticky="w")
        row += 1
        ttk.Checkbutton(edit, text="SBT",          variable=self._br_sbt_var).grid(
            row=row, column=0, columnspan=2, sticky="w")
        row += 1

        ttk.Separator(edit, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=10)
        row += 1

        ttk.Button(edit, text="💾  Salvar", command=self._save_fixture).grid(
            row=row, column=0, columnspan=2, sticky="ew")

        # ── Status bar ────────────────────────────────────────────────────────
        sbar = ttk.Frame(self, relief="sunken")
        sbar.pack(fill="x", side="bottom")

        self._status_lbl = ttk.Label(sbar, text="Pronto.", padding=(8, 2))
        self._status_lbl.pack(side="left")

        updated = self._data.get("updated_at", "")
        self._saved_lbl = ttk.Label(sbar, text=f"Salvo: {updated[:19] or '—'}",
                                     padding=(8, 2))
        self._saved_lbl.pack(side="right")

    # ── Treeview ───────────────────────────────────────────────────────────────

    def _filtered_fixtures(self) -> list[dict]:
        filt   = self._filter.get()
        search = self._search.get().lower().strip()

        result = self._fixtures

        if filt == "hoje":
            result = [f for f in result if is_today(f.get("date", ""))]
        elif filt == "grupo":
            result = [f for f in result if is_group(f.get("round", ""))]
        elif filt == "mata":
            result = [f for f in result if not is_group(f.get("round", ""))]

        if search:
            result = [f for f in result if
                      search in f.get("home", {}).get("name", "").lower() or
                      search in f.get("away", {}).get("name", "").lower()]

        return result

    def _populate_tree(self):
        # Preserva rounds expandidos
        open_rnds = {iid for iid in self._tree.get_children()
                     if self._tree.item(iid, "open")}

        self._tree.delete(*self._tree.get_children())

        groups: dict[str, list] = {}
        for f in self._filtered_fixtures():
            groups.setdefault(f.get("round", "Sem fase"), []).append(f)

        for rnd, rnd_fixtures in groups.items():
            rnd_iid = f"rnd_{rnd}"
            self._tree.insert(
                "", "end", iid=rnd_iid, text=rnd,
                values=("", "", "", ""), tags=("rnd",),
                open=(rnd_iid in open_rnds or True),
            )
            for f in rnd_fixtures:
                fid  = f.get("id")
                tag  = "ft" if f.get("status") == "FT" else ""
                self._tree.insert(
                    rnd_iid, "end", iid=str(fid), text="",
                    values=(
                        fmt_date(f.get("date", "")),
                        f.get("home", {}).get("name", ""),
                        fmt_score(f.get("score", {})),
                        f.get("away", {}).get("name", ""),
                    ),
                    tags=(tag,),
                )

    # ── Seleção ────────────────────────────────────────────────────────────────

    def _on_select(self, _event=None):
        sel = self._tree.selection()
        if not sel:
            return

        iid = sel[0]
        if iid.startswith("rnd_"):
            return

        fid = int(iid)
        self._selected_fid = fid
        f = next((x for x in self._fixtures if x.get("id") == fid), None)
        if f is None:
            return

        match_num = fid - 9000
        self._lbl_id.config(
            text=f"Jogo {match_num}  ·  {fmt_date(f.get('date', ''))} UTC",
            foreground="black",
            font=("Segoe UI", 9, "bold"),
        )

        self._home_var.set(f.get("home", {}).get("name", ""))
        self._away_var.set(f.get("away", {}).get("name", ""))

        is_ft = f.get("status", "NS") == "FT"
        self._ft_var.set(is_ft)
        self._toggle_spinboxes(is_ft)

        score = f.get("score", {})
        self._score_h_var.set(score.get("home") or 0)
        self._score_a_var.set(score.get("away") or 0)

        self._refresh_ko_panel(f)

        # Transmissões
        channels = self._broadcasts.get(str(fid), DEFAULT_CHANNELS)
        self._br_caze_var.set("CazéTV"       in channels)
        self._br_globo_var.set("Globo/SporTV" in channels)
        self._br_sbt_var.set("SBT"            in channels)

    # ── Controles ──────────────────────────────────────────────────────────────

    def _on_ft_toggle(self):
        enabled = self._ft_var.get()
        self._toggle_spinboxes(enabled)
        if not enabled:
            self._score_h_var.set(0)
            self._score_a_var.set(0)
            self._ko_frame.grid_remove()
        else:
            self._on_score_change()

    def _on_score_change(self):
        if self._selected_fid is None or not self._ft_var.get():
            return
        f = next((x for x in self._fixtures if x.get("id") == self._selected_fid), None)
        if f:
            self._refresh_ko_panel(f)

    def _toggle_spinboxes(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self._spin_h.config(state=state)
        self._spin_a.config(state=state)

    def _refresh_ko_panel(self, f: dict):
        """Exibe 'Quem avançou?' apenas em empates de jogos eliminatórios."""
        if not self._ft_var.get():
            self._ko_frame.grid_remove()
            return

        ko = not is_group(f.get("round", ""))
        sh = self._score_h_var.get()
        sa = self._score_a_var.get()

        if ko and sh == sa:
            home_name = f.get("home", {}).get("name", "") or "Casa"
            away_name = f.get("away", {}).get("name", "") or "Visitante"
            self._rb_home.config(text=f"🏠  {home_name}")
            self._rb_away.config(text=f"✈️  {away_name}")

            hw = f.get("home", {}).get("winner")
            self._winner_var.set("home" if hw is True else "away" if hw is False else "none")

            self._ko_frame.grid()
        else:
            self._ko_frame.grid_remove()

    # ── Salvar ─────────────────────────────────────────────────────────────────

    def _save_fixture(self):
        fid = self._selected_fid
        if fid is None:
            messagebox.showwarning("Nenhum jogo selecionado",
                                   "Clique em um jogo na lista antes de salvar.")
            return

        f = next((x for x in self._fixtures if x.get("id") == fid), None)
        if f is None:
            return

        home_name = self._home_var.get().strip()
        away_name = self._away_var.get().strip()
        is_ft     = self._ft_var.get()

        f["home"]["name"] = home_name
        f["away"]["name"] = away_name

        if is_ft:
            sh = self._score_h_var.get()
            sa = self._score_a_var.get()

            f["status"]        = "FT"
            f["score"]["home"] = sh
            f["score"]["away"] = sa

            if sh > sa:
                f["home"]["winner"] = True
                f["away"]["winner"] = False
            elif sa > sh:
                f["home"]["winner"] = False
                f["away"]["winner"] = True
            else:
                # Empate → usa seleção manual (pênaltis / prorrogação no mata-mata)
                chosen = self._winner_var.get()
                f["home"]["winner"] = True  if chosen == "home" else (False if chosen == "away" else None)
                f["away"]["winner"] = False if chosen == "home" else (True  if chosen == "away" else None)
        else:
            f["status"]         = "NS"
            f["score"]["home"]  = None
            f["score"]["away"]  = None
            f["home"]["winner"] = None
            f["away"]["winner"] = None

        save_data(self._data)

        # Transmissões
        channels: list[str] = []
        if self._br_caze_var.get():  channels.append("CazéTV")
        if self._br_globo_var.get(): channels.append("Globo/SporTV")
        if self._br_sbt_var.get():   channels.append("SBT")
        self._broadcasts[str(fid)] = channels
        save_broadcasts(self._broadcasts)

        # Atualiza linha na árvore
        score_str = f"{self._score_h_var.get()}–{self._score_a_var.get()}" if is_ft else "—"
        tag = "ft" if is_ft else ""
        try:
            self._tree.item(str(fid), values=(
                fmt_date(f.get("date", "")),
                home_name,
                score_str,
                away_name,
            ), tags=(tag,))
        except tk.TclError:
            pass

        now = utc_now().strftime("%H:%M:%S")
        self._status_lbl.config(text=f"✅  {home_name} × {away_name} salvo!")
        self._saved_lbl.config(text=f"Salvo: {now}")
        self.after(3000, lambda: self._status_lbl.config(text="Pronto."))

    # ── Regenerar ICS ──────────────────────────────────────────────────────────

    def _on_rebuild(self):
        self._status_lbl.config(text="Gerando worldcup.ics…")
        self.update_idletasks()
        try:
            rebuild_ics()
            self._status_lbl.config(text="✅  worldcup.ics gerado!")
            messagebox.showinfo("Pronto", "worldcup.ics regenerado com sucesso.")
        except Exception as exc:
            self._status_lbl.config(text="❌  Erro ao gerar .ics")
            messagebox.showerror("Erro ao gerar .ics", str(exc))
        self.after(4000, lambda: self._status_lbl.config(text="Pronto."))


# ── Ponto de entrada ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = EditorApp()
    app.mainloop()
