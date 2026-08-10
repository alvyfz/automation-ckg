from __future__ import annotations

import threading
import traceback
from pathlib import Path
from typing import Callable

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import main
import scanning
import ui


def _is_excel_file(path: str) -> bool:
    p = Path(path)
    return p.exists() and p.is_file() and p.suffix.lower() in {".xlsx", ".xlsm", ".xls"}


def _build_school_picker() -> tuple[list[str], dict[str, str], str]:
    school_items = sorted(
        [(key, value.get("school", key)) for key, value in ui.schools.items()],
        key=lambda x: x[1].lower(),
    )
    school_names = [name for _, name in school_items]
    school_key_by_name = {name: key for key, name in school_items}
    default_name = school_names[0] if school_names else ""
    return school_names, school_key_by_name, default_name


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Input Sehat")
        self.geometry("780x520")

        self._log_text = tk.Text(self, height=10, wrap="word", state="disabled")
        self._log_text.pack(side="bottom", fill="both", expand=False, padx=10, pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self._daftar_tab = ttk.Frame(notebook)
        self._periksa_tab = ttk.Frame(notebook)
        notebook.add(self._daftar_tab, text="Daftar")
        notebook.add(self._periksa_tab, text="Pemeriksaan")

        self._build_daftar(self._daftar_tab)
        self._build_pemeriksaan(self._periksa_tab)

    def log(self, message: str) -> None:
        self._log_text.configure(state="normal")
        self._log_text.insert("end", message + "\n")
        self._log_text.see("end")
        self._log_text.configure(state="disabled")

    def _run_async(self, title: str, fn: Callable[[], None]) -> None:
        def runner() -> None:
            try:
                self.log(f"[START] {title}")
                fn()
                self.log(f"[DONE] {title}")
            except Exception:
                self.log(f"[ERROR] {title}")
                self.log(traceback.format_exc())

        threading.Thread(target=runner, daemon=True).start()

    def _build_file_input(self, parent: ttk.Frame, *, label: str) -> tuple[ttk.Entry, tk.StringVar]:
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=8)

        ttk.Label(frame, text=label, width=14).pack(side="left")
        var = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=var)
        entry.pack(side="left", fill="x", expand=True, padx=6)

        def browse() -> None:
            path = filedialog.askopenfilename(
                title="Pilih file Excel",
                filetypes=[("Excel", "*.xlsx *.xlsm *.xls"), ("All files", "*.*")],
            )
            if path:
                var.set(path)

        ttk.Button(frame, text="Browse", command=browse, width=10).pack(side="left")
        return entry, var

    def _build_daftar(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Tampilan Daftar (main.py)", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", pady=6
        )

        _, excel_var = self._build_file_input(parent, label="File Excel")

        school_names, school_key_by_name, default_school = _build_school_picker()

        school_frame = ttk.Frame(parent)
        school_frame.pack(fill="x", pady=8)
        ttk.Label(school_frame, text="Sekolah", width=14).pack(side="left")
        school_var = tk.StringVar(value=default_school)
        school_combo = ttk.Combobox(
            school_frame, textvariable=school_var, values=school_names, state="readonly"
        )
        school_combo.pack(side="left", fill="x", expand=True, padx=6)

        def run_daftar() -> None:
            excel_path = excel_var.get().strip()
            if not _is_excel_file(excel_path):
                messagebox.showerror("Error", "Pilih file Excel yang valid untuk Daftar.")
                return
            selected_school_name = school_var.get().strip()
            school_key = school_key_by_name.get(selected_school_name, selected_school_name)

            def job() -> None:
                ui.set_school(school_key)
                main.run(excel_path, school_key=school_key)

            self._run_async("Daftar", job)

        ttk.Button(parent, text="Jalankan Daftar", command=run_daftar).pack(anchor="w", pady=8)

    def _build_pemeriksaan(self, parent: ttk.Frame) -> None:
        ttk.Label(
            parent, text="Tampilan Pemeriksaan (scanning.py)", font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=6)

        _, excel_var = self._build_file_input(parent, label="File Excel")

        school_names, school_key_by_name, default_school = _build_school_picker()

        school_frame = ttk.Frame(parent)
        school_frame.pack(fill="x", pady=8)
        ttk.Label(school_frame, text="Sekolah", width=14).pack(side="left")
        school_var = tk.StringVar(value=default_school)
        school_combo = ttk.Combobox(
            school_frame, textvariable=school_var, values=school_names, state="readonly"
        )
        school_combo.pack(side="left", fill="x", expand=True, padx=6)

        class_frame = ttk.Frame(parent)
        class_frame.pack(fill="x", pady=8)
        ttk.Label(class_frame, text="Kelas", width=14).pack(side="left")
        class_var = tk.StringVar(value="1")
        class_combo = ttk.Combobox(
            class_frame,
            textvariable=class_var,
            values=[str(i) for i in range(1, 13)],
            state="readonly",
            width=10,
        )
        class_combo.pack(side="left", padx=6)

        def run_pemeriksaan() -> None:
            excel_path = excel_var.get().strip()
            if not _is_excel_file(excel_path):
                messagebox.showerror("Error", "Pilih file Excel yang valid untuk Pemeriksaan.")
                return

            selected_school_name = school_var.get().strip()
            school_key = school_key_by_name.get(selected_school_name, selected_school_name)
            class_school = class_var.get().strip()

            def job() -> None:
                ui.set_school(school_key)
                ui.set_class_school(class_school)
                scanning.run(excel_path, school_key=school_key, class_school=class_school)

            self._run_async("Pemeriksaan", job)

        ttk.Button(parent, text="Jalankan Pemeriksaan", command=run_pemeriksaan).pack(
            anchor="w", pady=8
        )


if __name__ == "__main__":
    App().mainloop()

