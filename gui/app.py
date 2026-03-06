from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk


class OmniMindApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("OmniMind Automator")
        self.geometry("960x600")
        self._build_ui()

    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=16)
        root.pack(fill=tk.BOTH, expand=True)

        controls = ttk.Frame(root)
        controls.pack(fill=tk.X)

        record_btn = tk.Button(
            controls,
            text="Nahrát nového agenta",
            bg="#d7263d",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            command=lambda: messagebox.showinfo("Info", "Nahrávání bude dostupné v další iteraci."),
        )
        record_btn.pack(side=tk.LEFT, padx=(0, 12))

        ttk.Button(controls, text="Spustit", command=lambda: None).pack(side=tk.LEFT)
        ttk.Button(controls, text="Upravit", command=lambda: None).pack(side=tk.LEFT, padx=4)
        ttk.Button(controls, text="Smazat", command=lambda: None).pack(side=tk.LEFT)

        body = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        body.pack(fill=tk.BOTH, expand=True, pady=(16, 0))

        agents_frame = ttk.Labelframe(body, text="Uložení agenti", padding=8)
        self.agent_list = tk.Listbox(agents_frame, height=20)
        self.agent_list.pack(fill=tk.BOTH, expand=True)
        self.agent_list.insert(tk.END, "Faktury z emailu", "Test login flow", "Kontrola reportu")
        body.add(agents_frame, weight=2)

        steps_frame = ttk.Labelframe(body, text="Kroky agenta", padding=8)
        self.steps = tk.Text(steps_frame, height=18)
        self.steps.insert("1.0", "1) Klik na 'Přihlásit'\n2) Vyplnit email\n3) Čekat 2s\n")
        self.steps.pack(fill=tk.BOTH, expand=True)
        body.add(steps_frame, weight=3)

        ai_frame = ttk.Labelframe(body, text="AI asistent", padding=8)
        ttk.Label(ai_frame, text="Zadej instrukci:").pack(anchor=tk.W)
        self.prompt = ttk.Entry(ai_frame)
        self.prompt.pack(fill=tk.X, pady=4)
        ttk.Button(ai_frame, text="Analyzovat", command=lambda: None).pack(anchor=tk.E)
        body.add(ai_frame, weight=2)


def launch_app() -> None:
    app = OmniMindApp()
    app.mainloop()
