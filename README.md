# .NET DLL Inspector v2.21

A lightweight Python utility designed for analyzing .NET assemblies. This tool offers a structured overview of class hierarchies, members, properties, methods, fields, and events—without requiring full decompilation. Ideal for reverse-engineering or inspecting complex frameworks such as Torch and Space Engineers modding environments.

---

## ✨ Features

- **Smart Search**: Filter by namespaces, types, methods, or properties across multiple DLLs.
- **Progress Tracking**: Real-time console feedback during heavy assembly analysis.
- **Modes of Inspection**:
  - **Standard**: Methods `[M]` only (Default).
  - **Extended (`--ext`)**: Adds Properties `[P]`.
  - **Deep (`--deep`)**: Adds Fields `[F]` and Events `[E]`.
- **CLI Automation**: Skip prompts using the default path switch.
- **Clean Logging**: Automatically sanitizes search terms for log filenames and handles increments to prevent overwriting.

---

## 📦 Installation

### Prerequisites

- **Python 3.x**
- Required packages listed in `requirements.txt` (Mainly `pythonnet`)

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

On first run, the script generates `dll-check2.ini`.

| Setting          | Description                                               |
|------------------|-----------------------------------------------------------|
| `DefaultPath`    | Folder to scan (default: `./Dependencies`)                |
| `FilterKeywords` | Only scan DLLs containing these words (comma-separated)   |
| `LogDir`         | Output directory for reports (default: `doc`)             |

---

## ▶️ Usage

### 🚀 Quick/Automated Scan (New in v2.21)
Use the `--default` (or `-y`) switch to skip the path prompt and use the INI settings immediately:
```bash
python dll-check2.py --default --search "ChatManager"
```

### Search Modes
| Command | Description |
| :--- | :--- |
| `python dll-check2.py --search "MySession"` | Basic method search |
| `python dll-check2.py -e -s "Block"` | Search methods + properties |
| `python dll-check2.py -d -s "Grid"` | Deep search (includes Fields/Events) |

### Interactive Mode
Simply run the script to be prompted for a target directory:
```bash
python dll-check2.py
```

---

## 🔍 Member Legend

| Tag | Meaning | Required Switch |
| :--- | :--- | :--- |
| `[M]` | Method | (Always shown) |
| `[ST]`| Static member | (Context dependent) |
| `[P]` | Property | `--ext` or `--deep` |
| `[F]` | Field (Public variable) | `--deep` |
| `[E]` | Event | `--deep` |



**Example output snippet:**
```text
[NS: Sandbox.Game.Entities.Blocks] -> Class: MyCubeBlock
  [P] [ST] Int32 BlockTypeID
  - Void UpdateBeforeSimulation()
  [F] [ST] Boolean IsFunctional
```

---

## 🗂 Project Structure

```text
project-root/
├── dll-check2.py
├── dll-check2.ini       # Auto-generated config
├── Dependencies/        # Place DLLs here
└── doc/                 # inspect_search_TEXT.txt
```

---

## 📜 License
MIT License.

---

## 💡 Tips
- **Filenames**: Searching for `Sandbox.Game` will generate `inspect_search_SandboxGame.txt`.
- **Performance**: For massive libraries (like VRage), use the interactive mode to see the `[X/Y] Analyzing...` progress tracker.
- **Automation**: Integrate with `-y` switch in your build tasks to verify API changes after game updates.