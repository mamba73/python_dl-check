# # .NET DLL Inspector v2.26

A powerful and lightweight Python tool for deep analysis of .NET assemblies. Designed specifically for modders (Space Engineers, Torch, etc.) to quickly map unknown APIs, discover hidden members, and understand class hierarchies without decompilation.

---

## ✨ New Features (v2.26)

- **C# Type Cleanup**: Converts raw .NET types into readable C# format (e.g., `Int64` -> `long`, `Single` -> `float`).
- **Generics Support**: Properly formats generic lists and dictionaries (e.g., `List<IMyPlayer>` instead of `List`1`).
- **Inheritance Tracking**: Displays the parent class (Base Class) next to each class, making navigation through the SE framework easier.
- **VS Code Integration**: Added `-o` switch to instantly open reports in a new tab of the active VS Code window.

---

## 📦 Installation and Prerequisites

- **Python 3.x**
- Package: `pip install pythonnet`
- VS Code (optional, for the `-o` switch)

---

## ⚙️ Configuration

Upon the first run, the tool generates `dll-check2.ini`.

| Setting | Description |
| :--- | :--- |
| `DefaultPath` | Path to the folder containing the DLLs you scan most frequently. |
| `FilterKeywords` | Keywords for filtering DLL files (e.g., `Sandbox, VRage`). |

---

## ▶️ Usage and Switches

### 🎯 "Sniper" Mode (Recommended)
When looking for specific data within a massive class:
```bash
# Searches for 'Players' inside 'MySession', prints deep details, and opens in VS Code
python dll-check2.py -y -d -s MySession -f Players -o
```

### 🔍 List of All Options
| Switch | Long Form | Description |
| :--- | :--- | :--- |
| `-s` | `--search` | Keyword for Class Name or Namespace. |
| `-f` | `--filter` | Keyword for Member (method, field, property). |
| `-d` | `--deep` | Deep mode: Includes Fields `[F]` and Events `[E]`. |
| `-e` | `--ext` | Extended mode: Includes Properties `[P]`. |
| `-y` | `--default`| Skips path prompt (uses the one from INI). |
| `-o` | `--open` | Automatically opens the result in VS Code. |
| `-h` | `--help` | Shows brief instructions. |

---

## 📖 How to Read the Report?

v2.26 brings readability that matches your C# code:

| Tag | Meaning | Note |
| :--- | :--- | :--- |
| `Class: X : Y` | Class X inherits Y | **New in v2.26** |
| `[ST]` | Static member | Accessed via `Class.Static...` |
| `[F]` | Field (Variable) | Requires `-d` |
| `[P]` | Property | Requires `-e` or `-d` |
| `-` | Method | Always displayed |

### Example of Cleaned Output:
```text
FILE: Sandbox.Game.dll
========================================
[NS: Sandbox.Game.World] -> Class: MySession : MySessionBase
  [P] [ST] MyFactionManager Factions
  [P] [ST] MyPlayerCollection Players
  - [ST] void SetLastDamage(MyDamageInformation info)
```

---

## 🗂 Project Structure

```text
project-root/
├── dll-check2.py
├── dll-check2.ini        # Automatic configuration
├── Dependencies/         # DLL files for analysis
└── doc/                  # Generated reports (.txt)
```

---

## 📜 License
MIT License.

[Buy Me a Coffee ☕](https://buymeacoffee.com/mamba73)
