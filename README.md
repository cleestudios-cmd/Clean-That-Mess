# 🗂️ Clean-That-Mess
A beginner-built Python tool that scans a folder, detects file types, and copies them into organized subfolders automatically — no more messy Downloads folders.

---

## 👋 About This Project

Hi! I'm a beginner Python developer building this project to learn real-world automation while solving an actual everyday problem.

The idea is simple: point the script at a messy folder, and it automatically sorts everything into clean, organized subfolders based on file type — photos go into `PHOTOS/`, PDFs go into `PDF/`, videos into `VIDEOS/`, and so on.

**This is an open learning project.** I built this to grow as a coder, and I'd love to grow alongside other beginners and aspiring developers. If you're just starting out and want a real project to contribute to, learn from, or just experiment with — you're in the right place.

---

## ✨ What It Does

- 🖥️ Offers a **Modern flat-design GUI** and a classic **CLI mode**
- 📂 Select source and destination folders with dialog browsers (GUI) or path prompts (CLI)
- 🔍 Scans all files in the source folder
- 📋 **Copies** or **Moves** files into organized subfolders (Copy mode keeps originals, Move mode transfers them)
- 🔁 Optionally **scans subfolders recursively** instead of just the top level
- 🖼️ Photos (jpg, png, heic, webp, etc.) → `PHOTOS/JPG/`, `PHOTOS/PNG/`, etc.
- 📄 Documents, videos, audio, archives → `PDF/`, `DOCS/`, `VIDEOS/`, `AUDIO/`, etc.
- ❓ Unknown file types → `OTHERS/`
- ⏭️ Skips files that already exist at the destination (no duplicates)
- 📝 Displays a live, real-time log of the operation

---

## 📁 Output Structure Example

```
Organized/
├── PHOTOS/
│   ├── JPG/
│   ├── PNG/
│   └── HEIC/
├── PDF/
├── DOCS/
├── VIDEOS/
├── AUDIO/
├── ARCHIVES/
├── CODE/
└── OTHERS/
```

---

## 🗃️ File Structure

- **`file-org.py`**: Main entrypoint containing core organizing logic, CLI mode, and dynamic GUI launcher.
- **`gui.py`**: Custom-styled flat dark-theme Tkinter GUI layout.

---

## 🚀 How to Run

### 1. Requirements

- Python 3.x installed — [Download here](https://www.python.org/downloads/)
- No extra libraries needed — only built-in Python modules (`os`, `shutil`, `tkinter`)

### 2. Clone the Repository

```bash
git clone https://github.com/cleestudios-cmd/Clean-That-Mess.git
```

Then navigate into the folder:

```bash
cd Clean-That-Mess
```

### 3. Run the GUI (Default)

Running the script directly opens the interactive GUI:

```bash
python file-org.py
```

Inside the GUI:
- Use the **Browse** buttons to select your source and destination folders.
- Select **Copy** (keeps originals) or **Move** (transfers/removes originals) mode.
- Tick **Include subfolders** to scan nested folders recursively.
- Click **Run** to organize. Progress logs will show in the log area.

### 4. Run the CLI Mode

If you prefer using the command line:

```bash
python file-org.py --cli
```

Follow the prompts to enter folders, choose the operation mode, and decide whether to scan subfolders recursively.

---

## 🗺️ Roadmap

This is just the beginning. Here's what I'm planning to build next:

- [x] Add **file move mode** (not just copy) as an option
- [x] Scan **subfolders recursively** (not just top-level files)
- [x] Add a **simple GUI** so non-coders can use it too
- [ ] Let users **customize their own file type categories**
- [ ] Add a **undo/restore** feature
- [ ] Generate an **organized summary report** after each run
- [ ] Support for **scheduled/automatic runs**

---

## 🤝 Contributing — Beginners Welcome!

This project is **open to everyone**, especially beginners and aspiring coders who want to work on a real project.

I tagged beginner-friendly tasks with **`good first issue`** — these are small, well-defined tasks that are perfect if you've never contributed to a project before.

### How to contribute

1. **Fork** this repository (click Fork at the top right)
2. **Clone** your fork:
   ```bash
   git clone https://github.com/cleestudios-cmd/Clean-That-Mess.git
   ```
3. **Create a branch** for your change:
   ```bash
   git checkout -b your-feature-name
   ```
4. **Make your changes**, then commit:
   ```bash
   git commit -m "Add: your change description"
   ```
5. **Push** to your fork:
   ```bash
   git push origin your-feature-name
   ```
6. Open a **Pull Request** and describe what you did

Not sure where to start? Check the [Issues](../../issues) tab and look for the `good first issue` label.

---

## 💬 Suggestions & Collaboration

Have an idea? Found a bug? Want to build something together?

- Open an [Issue](../../issues) — for bugs, ideas, or feature requests
- Start a [Discussion](../../discussions) — for questions, feedback, or just saying hi
- DM me — always open to connecting with fellow coders learning the same path

This project isn't just about the code. It's about building something real while meeting people with the same goal — learning, improving, and having something to show for it.

---

## 📄 License

MIT License — free to use, fork, and build on.

---

> Built by a beginner, for beginners. Every expert was once where you are. Let's build together. 🚀
