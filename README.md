# .NET DLL Inspector v2.14

A lightweight Python utility designed for analyzing .NET assemblies. This tool offers a structured overview of class hierarchies, members, properties, methods, fields, and events—without requiring full decompilation. Ideal for reverse-engineering or inspecting complex frameworks such as Torch and Space Engineers modding environments.

---

## ✨ Features

- Analyze public classes, interfaces, and their members.
- Search through namespaces, types, methods, and properties by keyword.
- Optional Extended (`--ext`) and Deep inspection (`--deep`) modes to include Properties `[P]`, Fields `[F]`, and Events `[E]`.
- Automatic configuration file generation with sensible defaults.
- Output saved to timestamped logs in the `doc/` directory.
- Clean separation of dependencies using a local `Dependencies/` folder.

---

## 📦 Installation

### Prerequisites

- **Python 3.x**
- Required packages listed in `requirements.txt`

Install required libraries:

```
pip install -r requirements.txt
```

> Note: The primary dependency is [`pythonnet`](https://github.com/pythonnet/pythonnet), which enables interaction with .NET assemblies from Python.

---

## ⚙️ Configuration

On first run, the script automatically generates a configuration file named after itself (e.g., `dll-check2.ini`). You can customize the following settings:

| Setting          | Description |
|------------------|-------------|
| `DefaultPath`    | Path where DLLs are scanned (defaults to `./Dependencies`) |
| `FilterKeywords` | Comma-separated list of keywords to filter relevant DLLs |
| `LogDir`         | Directory where output logs are stored (default: `doc`) |
| `LogBaseName`    | Base name for generated report files |

Example auto-generated INI content:
```
[SETTINGS]
DefaultPath = ./Dependencies
FilterKeywords = Torch,Sandbox,VRage,SpaceEngineers
LogDir = doc
LogBaseName = inspect_results
```

You may modify these values directly in the `.ini` file to match your environment.

---

## ▶️ Usage

### Basic Scan

Run the script and press Enter to scan all filtered DLLs under the default path:

```
python dll-check2.py
```

### Search Mode

To find specific terms across all loaded assemblies:

```
python dll-check2.py --search "ChatManager"
```

This searches within namespaces, class names, method signatures, property names, etc.

### Extended Mode

To include Properties `[P]` in your results (Methods are shown by default):

```
python dll-check2.py --ext
```

### Deep Inspection

Include fields and events in the scan:

```
python dll-check2.py --search "MySession" --deep
```

Useful when exploring internal structure or event-driven components.

### Help Command

Display built-in help menu:

```
python dll-check2.py --help
```

---

## 🔍 Member Legend

Each entry in the output uses short tags to indicate member type:

| Tag   | Meaning                      | Switch              |
|-------|------------------------------|---------------------|
| `[M]` | Method                       | (Always shown)      |
| `[ST]`| Static member (Next to tag)  | (Context dependent) |
| `[P]` | Property                     | --ext or --deep     |
| `[F]` | Field (Public variable)      | --deep              |
| `[E]` | Event                        | --deep              |

Example output snippet:
```
[NS: Sandbox.Game.Entities.Blocks] -> Class: MyCubeBlock
  [P] [ST] Int32 BlockTypeID
  - Void UpdateBeforeSimulation()
  [F] [ST] Boolean IsFunctional
```

---

## 🗂 Project Structure

Ensure that you organize your project like so:

```
project-root/
├── dll-check2.py
├── dll-check2.ini       # Auto-generated config
├── Dependencies/        # Place DLLs here
│   ├── Torch.dll
│   └── VRage.dll
└── doc/                 # Generated reports go here
```

---

## 📜 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 💡 Tips

- Use `git` to track changes in generated documentation inside `/doc`, but ignore large binary outputs.
- Always ensure correct runtime context for loading .NET assemblies (especially architecture-specific ones).
- For advanced analysis, consider integrating this tool into CI pipelines or automated mod validation workflows.

---