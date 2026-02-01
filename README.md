# .NET DLL Inspector v2.25

A lightweight Python utility designed for analyzing .NET assemblies. This tool offers a structured overview of class hierarchies, members, properties, methods, fields, and events—without requiring full decompilation.

---

## ✨ Features

- **Smart Search & Filter**: Find specific classes (`-s`) and then drill down into specific members (`-f`) to avoid massive log files.
- **Structural Analysis**: Supports Classes, Interfaces, and **Structs** (ValueTypes).
- **Progress Tracking**: Real-time console feedback with a cleaner UI.
- **CLI Automation**: Skip prompts using the default path switch (`-y`).
- **Sanitized Logging**: Filenames are automatically generated based on your search and filter terms.

---

## 📦 Installation

### Prerequisites

- **Python 3.x**
- Required packages: `pythonnet`

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

### 🚀 The "Sniper" Search (New in v2.24+)
If a class like `MySession` has thousands of lines, use the filter to find exactly what you need:
```bash
# Finds MySession class, but shows ONLY members containing "Players"
python dll-check2.py -y -d -s MySession -f Players
```

### 🔍 Quick Switches
| Switch | Long Form | Description |
| :--- | :--- | :--- |
| `-s` | `--search` | Keyword for Namespace or Class name |
| `-f` | `--filter` | Keyword for Member (Method/Field/Property) name |
| `-d` | `--deep` | Deep mode: Includes Fields `[F]` and Events `[E]` |
| `-e` | `--ext` | Extended mode: Includes Properties `[P]` |
| `-y` | `--default`| Skip path prompt and use INI default |
| `-h` | `--help` | Show help menu |

### 💡 Examples
**Basic search for a struct:**
```bash
python dll-check2.py -y -d -s MyDamageInformation
```

**Deep search in default folder without prompts:**
```bash
python dll-check2.py -y -d -s MyCubeBlock
```

---

## 🔍 Member Legend

| Tag | Meaning | Required Switch |
| :--- | :--- | :--- |
| `[M]` | Method | (Always shown) |
| `[ST]`| Static member | (Automatic detection) |
| `[P]` | Property | `-e` or `-d` |
| `[F]` | Field (Public variable) | `-d` |
| `[E]` | Event | `-d` |



**Example output snippet:**
```text
[NS: Sandbox.Game.World] -> Class: MySession
  [P] [ST] MyFactionManager Factions
  [P] [ST] MyPlayerCollection Players
```

---

## 🗂 Project Structure

```text
project-root/
├── dll-check2.py
├── dll-check2.ini       # Auto-generated config
├── Dependencies/        # Place DLLs here
└── doc/                 # inspect_search_Term_filter_Term.txt
```

---

## 📜 License
MIT License.