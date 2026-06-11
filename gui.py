import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

class ModernEntry(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#27272a", bd=0, highlightthickness=1, highlightbackground="#3f3f46", highlightcolor="#3b82f6")
        self.entry = tk.Entry(self, bg="#27272a", fg="#f4f4f5", insertbackground="#f4f4f5", relief="flat", bd=0, font=("Segoe UI", 10), **kwargs)
        self.entry.pack(fill="both", expand=True, padx=10, pady=8)
        
        # Bind focus events to change highlight border
        self.entry.bind("<FocusIn>", lambda e: self.config(highlightbackground="#3b82f6", highlightcolor="#3b82f6"))
        self.entry.bind("<FocusOut>", lambda e: self.config(highlightbackground="#3f3f46", highlightcolor="#3b82f6"))

    def get(self):
        return self.entry.get()

    def delete(self, first, last):
        self.entry.delete(first, last)

    def insert(self, index, string):
        self.entry.insert(index, string)

    def set_disabled(self, disabled=True):
        if disabled:
            self.entry.config(state="disabled", bg="#18181b", fg="#71717a")
            self.config(bg="#18181b", highlightbackground="#27272a")
        else:
            self.entry.config(state="normal", bg="#27272a", fg="#f4f4f5")
            self.config(bg="#27272a", highlightbackground="#3f3f46")


class ModernButton(tk.Button):
    def __init__(self, parent, text, command=None, bg="#3b82f6", fg="#ffffff", hover_bg="#60a5fa", font=("Segoe UI", 9, "bold"), **kwargs):
        super().__init__(
            parent, text=text, command=command, bg=bg, fg=fg, 
            activebackground=hover_bg, activeforeground=fg,
            relief="flat", bd=0, font=font, 
            cursor="hand2", padx=15, pady=8, **kwargs
        )
        self.bg = bg
        self.hover_bg = hover_bg
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, e):
        if self.cget("state") != "disabled":
            self.config(bg=self.hover_bg)
        
    def on_leave(self, e):
        if self.cget("state") != "disabled":
            self.config(bg=self.bg)

    def set_disabled(self, disabled=True):
        if disabled:
            self.config(state="disabled", bg="#27272a", fg="#52525b")
        else:
            self.config(state="normal", bg=self.bg, fg="#ffffff")


class SegmentedControl(tk.Frame):
    def __init__(self, parent, options, default_value, command=None):
        super().__init__(parent, bg="#18181b")
        self.options = options
        self.command = command
        self.value = default_value
        self.buttons = {}
        
        for opt in options:
            btn = tk.Button(
                self, text=opt, relief="flat", bd=0, font=("Segoe UI", 9, "bold"),
                cursor="hand2", padx=16, pady=6
            )
            btn.pack(side="left", padx=2)
            btn.config(command=lambda o=opt: self.select(o))
            self.buttons[opt] = btn
            
        self.update_styles()
        
    def select(self, opt):
        if self.buttons[opt].cget("state") != "disabled":
            self.value = opt
            self.update_styles()
            if self.command:
                self.command(opt)
            
    def update_styles(self):
        for opt, btn in self.buttons.items():
            if opt == self.value:
                btn.config(bg="#3b82f6", fg="#ffffff", activebackground="#3b82f6", activeforeground="#ffffff")
            else:
                btn.config(bg="#27272a", fg="#a1a1aa", activebackground="#27272a", activeforeground="#a1a1aa")
                
    def get(self):
        return self.value

    def set_disabled(self, disabled=True):
        for opt, btn in self.buttons.items():
            if disabled:
                btn.config(state="disabled", bg="#1f1f23", fg="#52525b")
            else:
                btn.config(state="normal")
        if not disabled:
            self.update_styles()


class CleanMessGUI:
    def __init__(self, root, organize_callback):
        self.root = root
        self.organize_callback = organize_callback
        self.root.title("🗂️ Clean-That-Mess")
        self.root.geometry("700x580")
        self.root.minsize(620, 520)
        self.root.configure(bg="#18181b")

        # Main container with padding
        main_container = tk.Frame(root, bg="#18181b", padx=20, pady=20)
        main_container.pack(fill="both", expand=True)

        # Header Section
        header_frame = tk.Frame(main_container, bg="#18181b")
        header_frame.pack(fill="x", pady=(0, 15))

        title_label = tk.Label(header_frame, text="🗂️ Clean-That-Mess", font=("Segoe UI", 18, "bold"), fg="#f4f4f5", bg="#18181b")
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(header_frame, text="Sort your messy files into organized categories automatically.", font=("Segoe UI", 10), fg="#a1a1aa", bg="#18181b")
        subtitle_label.pack(anchor="w", pady=(2, 0))

        # Divider line
        divider = tk.Frame(main_container, height=1, bg="#27272a")
        divider.pack(fill="x", pady=(0, 20))

        # Form container
        form_frame = tk.Frame(main_container, bg="#18181b")
        form_frame.pack(fill="x", pady=(0, 15))

        # --- Source Selection ---
        src_lbl = tk.Label(form_frame, text="Source Folder", font=("Segoe UI", 10, "bold"), fg="#f4f4f5", bg="#18181b")
        src_lbl.pack(anchor="w", pady=(0, 5))

        src_row = tk.Frame(form_frame, bg="#18181b")
        src_row.pack(fill="x", pady=(0, 15))
        
        self.src_entry = ModernEntry(src_row)
        self.src_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.src_btn = ModernButton(src_row, text="Browse", command=self.browse_source, bg="#27272a", hover_bg="#3f3f46")
        self.src_btn.pack(side="right")

        # --- Destination Selection ---
        dest_lbl = tk.Label(form_frame, text="Destination Folder", font=("Segoe UI", 10, "bold"), fg="#f4f4f5", bg="#18181b")
        dest_lbl.pack(anchor="w", pady=(0, 5))

        dest_row = tk.Frame(form_frame, bg="#18181b")
        dest_row.pack(fill="x", pady=(0, 15))

        self.dest_entry = ModernEntry(dest_row)
        self.dest_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.dest_btn = ModernButton(dest_row, text="Browse", command=self.browse_destination, bg="#27272a", hover_bg="#3f3f46")
        self.dest_btn.pack(side="right")

        # --- Action & Mode Section ---
        action_row = tk.Frame(form_frame, bg="#18181b")
        action_row.pack(fill="x", pady=(10, 0))

        mode_lbl_frame = tk.Frame(action_row, bg="#18181b")
        mode_lbl_frame.pack(side="left", fill="y")
        
        mode_lbl = tk.Label(mode_lbl_frame, text="Mode:", font=("Segoe UI", 10, "bold"), fg="#f4f4f5", bg="#18181b")
        mode_lbl.pack(side="left", padx=(0, 10))

        self.mode_control = SegmentedControl(action_row, ["Copy (Keep originals)", "Move (Transfer files)"], "Copy (Keep originals)")
        self.mode_control.pack(side="left")

        self.run_btn = ModernButton(action_row, text="Run Organization", command=self.start_organize, bg="#10b981", hover_bg="#34d399")
        self.run_btn.pack(side="right")

        # --- Options Section ---
        options_row = tk.Frame(form_frame, bg="#18181b")
        options_row.pack(fill="x", pady=(12, 0))

        self.recursive_var = tk.BooleanVar(value=False)
        self.recursive_check = tk.Checkbutton(
            options_row,
            text="Include subfolders (scan recursively)",
            variable=self.recursive_var,
            font=("Segoe UI", 9), fg="#a1a1aa", bg="#18181b",
            activebackground="#18181b", activeforeground="#f4f4f5",
            selectcolor="#27272a", bd=0, highlightthickness=0,
            cursor="hand2", anchor="w",
        )
        self.recursive_check.pack(anchor="w")

        # --- Logs Section ---
        log_lbl = tk.Label(main_container, text="Results Log", font=("Segoe UI", 10, "bold"), fg="#f4f4f5", bg="#18181b")
        log_lbl.pack(anchor="w", pady=(15, 5))

        log_frame = tk.Frame(main_container, bg="#27272a", bd=1, highlightthickness=1, highlightbackground="#3f3f46")
        log_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(log_frame, wrap="word", state="disabled", font=("Consolas", 10), bg="#18181b", fg="#e2e8f0", insertbackground="#e2e8f0", relief="flat", bd=0, padx=10, pady=10)
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview, bg="#18181b", bd=0)
        scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def browse_source(self):
        dir_path = filedialog.askdirectory(title="Select Source Directory")
        if dir_path:
            self.src_entry.delete(0, tk.END)
            self.src_entry.insert(0, os.path.abspath(dir_path))

    def browse_destination(self):
        dir_path = filedialog.askdirectory(title="Select Destination Directory")
        if dir_path:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, os.path.abspath(dir_path))

    def append_log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.configure(state="disabled")
        self.log_text.see(tk.END)

    def start_organize(self):
        source = self.src_entry.get().strip()
        destination = self.dest_entry.get().strip()
        mode = "copy" if self.mode_control.get().startswith("Copy") else "move"
        recursive = self.recursive_var.get()

        if not source:
            messagebox.showerror("Error", "Please select a source folder.")
            return
        if not os.path.isdir(source):
            messagebox.showerror("Error", f"Source folder does not exist:\n{source}")
            return

        if not destination:
            messagebox.showerror("Error", "Please select a destination folder.")
            return

        # If destination doesn't exist, prompt to create it
        if not os.path.isdir(destination):
            confirm = messagebox.askyesno("Create Folder", f"Destination folder does not exist:\n{destination}\n\nDo you want to create it?")
            if not confirm:
                return

        # Clear logs
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")

        # Disable UI elements during run
        self.run_btn.set_disabled(True)
        self.src_btn.set_disabled(True)
        self.dest_btn.set_disabled(True)
        self.src_entry.set_disabled(True)
        self.dest_entry.set_disabled(True)
        self.mode_control.set_disabled(True)
        self.recursive_check.config(state="disabled")

        t = threading.Thread(target=self.run_thread, args=(source, destination, mode, recursive))
        t.daemon = True
        t.start()

    def run_thread(self, source, destination, mode, recursive):
        try:
            self.organize_callback(source, destination, mode=mode, recursive=recursive, log_callback=self.append_log)
        except Exception as e:
            self.append_log(f"❌ Unexpected error: {e}")
        finally:
            self.root.after(0, self.enable_ui)

    def enable_ui(self):
        self.run_btn.set_disabled(False)
        self.src_btn.set_disabled(False)
        self.dest_btn.set_disabled(False)
        self.src_entry.set_disabled(False)
        self.dest_entry.set_disabled(False)
        self.mode_control.set_disabled(False)
        self.recursive_check.config(state="normal")


def run_gui(organize_callback):
    # Attempt to enable high DPI awareness for a crisp GUI on Windows
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

    root = tk.Tk()
    gui = CleanMessGUI(root, organize_callback)
    root.mainloop()
