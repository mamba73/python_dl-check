# .NET DLL Inspector v2.70

A powerful and lightweight Python tool for deep analysis of .NET assemblies.  
Designed for modders and plugin developers (Space Engineers, Torch, etc.) to quickly map unknown APIs, discover hidden members, and understand class hierarchies — without decompilation.

---

## ✨ What's New in v2.70

- **Timestamp log names**: Log files are now named with a timestamp prefix instead of `inspect_` (e.g., `2026-03-10_112229_ContractBlock.txt`).
- **`--clear`**: New command to delete all generated log files and clean up the log directory in one step.
- **Active parameter summary**: On every run, the tool prints which flags are active and what they do — no more guessing what was passed.
- **Extended help system**:
  - `--help` — compact option table, no examples
  - `--help:extend` — full help with detailed examples (ContractBlock, EconomyContract, StoreBlock, etc.)
  - `--help:rules:pb` — coding rules for SE Programmable Block scripting
  - `--help:rules:plugin` — coding rules for Torch Server Plugin development
  - `--help:rules:mod` — coding rules for SE World Modding

---

## 📦 Installation and Prerequisites

- **Python 3.x**
- Package: `pip install pythonnet`
- VS Code (optional, for the `-o` flag)

---

## ⚙️ Configuration

On first run, the tool generates `config_check.ini` automatically.

| Setting | Description |
| :--- | :--- |
| `DefaultPath` | Path to the folder containing the DLLs you scan most frequently. |
| `FilterKeywords` | Comma-separated keywords used to filter which DLL files to scan (e.g., `Sandbox,VRage,Torch`). |
| `LogDir` | Directory where log files are saved (default: `.inspect`). |
| `VSCodePath` | Full path to your VS Code `code.cmd` binary (used with `-o`). |

---

## ▶️ Usage

### 🎯 Sniper Mode (Recommended)

Looking for a specific method or field inside a massive class:

```bash
# Find all members named "GetContract" inside any ContractBlock type, deep scan, open in VS Code
python dll-check2.py -y -d -s ContractBlock -f GetContract -o
```

### 🔍 All Options

| Option | Description |
| :--- | :--- |
| `-s <term>` | Filter **TYPE** names (searches `Namespace.TypeName`) |
| `-f <term>` | Filter **MEMBER** names (methods, properties, fields) |
| `-x` | Exact word match (no substring) |
| `-e` | Include properties `[P]` in output |
| `-d` | Deep mode: include fields `[F]` + properties `[P]` |
| `-a` | Scan ALL DLL files (ignore `FilterKeywords` from config) |
| `--deps` | Show dependency graph between DLL files |
| `-y` | Use default path from config (skips path prompt) |
| `-o` | Open generated log in VS Code after scan |
| `--clear` | Delete all generated log files / log directory |
| `-h` / `--help` | Show compact help (options only, no examples) |
| `--help:extend` | Show full help with examples |
| `--help:rules:pb` | Show coding rules: SE Programmable Block |
| `--help:rules:plugin` | Show coding rules: Torch Server Plugin |
| `--help:rules:mod` | Show coding rules: SE World Modding |

---

## 📖 Reading the Report

| Tag | Meaning | Requires |
| :--- | :--- | :--- |
| `[NS: ...]` | Namespace of the type | always |
| `Class: X : Y` | Class X inherits from Y | always |
| `Struct: X` | Value type (struct) | always |
| `[ST]` | Static member | always |
| `[F]` | Field (variable) | `-d` |
| `[P]` | Property | `-e` or `-d` |
| `-` | Method | always |

### Example output:

```text
FILE: Sandbox.Game.dll (v1.208.15.0)
------------------------------------------------------------
[NS: Sandbox.Game.World] -> Class: MySession : MySessionBase
  [P] [ST] MyFactionManager Factions
  [P] [ST] MyPlayerCollection Players
  - [ST] void SetLastDamage(MyDamageInformation info)

[NS: Sandbox.Game.Entities.Blocks] -> Class: MyContractBlock : MyFunctionalBlock
  [F] long ContractId
  [P] bool IsEnabled
  - void AddContract(MyContractDescription contract)
  - MyContractDescription GetContract(long id)
```

---

## 💡 Example Commands

```bash
# Basic type search
python dll-check2.py -y -s ContractBlock

# Methods + properties (moderate detail)
python dll-check2.py -y -s ContractBlock -e

# Full deep scan (fields + properties + methods)
python dll-check2.py -y -d -s ContractBlock

# Deep scan, filter members by name
python dll-check2.py -y -d -s ContractBlock -f Id

# Economy contract types, full detail, open in VS Code
python dll-check2.py -y -d -s EconomyContract -o

# Store block, find insert methods
python dll-check2.py -y -d -s StoreBlock -f Insert -o

# Scan ALL DLLs (ignore keyword filter)
python dll-check2.py -y -a -s ContractBlock

# Dependency graph
python dll-check2.py -y --deps

# Delete all generated logs
python dll-check2.py --clear
```

---

## 🗂 Project Structure

```text
project-root/
├── dll-check2.py
├── config_check.ini      # Auto-generated configuration
├── Dependencies/         # DLL files for analysis
└── .inspect/             # Generated log files (timestamped .txt)
```

---

## 📜 License

MIT License.

---

*Developed by [mamba73](https://github.com/mamba73). Feel free to submit issues or pull requests!*

[Buy Me a Coffee ☕](https://buymeacoffee.com/mamba73)