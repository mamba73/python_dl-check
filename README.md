# .NET DLL Inspector v2.27

Lightweight utility for analyzing .NET assemblies, tailored for Space Engineers/Torch modding.

---

## ✨ Features (v2.27)

- **Portable VSCode Support**: Configurable path to your `code.cmd` for instant reporting.
- **Smart Type Cleanup**: Converts `Int64` to `long`, `Single` to `float`, etc.
- **Generics & Inheritance**: Clear visualization of `List<T>` and Base Classes.
- **Auto-naming Logs**: Reports are named based on your search/filter parameters.

---

## ⚙️ Configuration (dll-check2.ini)

The script will auto-generate this on first run.

| Key | Description |
| :--- | :--- |
| `DefaultPath` | Path to your DLL folder. |
| `VSCodePath` | Full path to your portable VSCode `bin\code.cmd`. |
| `FilterKeywords` | Only scan DLLs containing these words. |

---

## ▶️ Usage

```bash
# Search for Vector3D, deep scan, use default path, and open in VSCode
python dll-check2.py -y -d -o -s Vector3D
```

### 🔍 Switches
| Switch | Description |
| :--- | :--- |
| `-s` | Search for Class or Namespace. |
| `-f` | Filter members (Methods, Fields, etc.) inside found classes. |
| `-d` | Deep scan (Includes Fields `[F]` and Events). |
| `-e` | Extended scan (Includes Properties `[P]`). |
| `-o` | **Open in VSCode** (Uses path from .ini). |
| `-y` | Use default path from .ini (No prompt). |

---

## 📜 Member Legend
- `Class: X : Y` -> Class X inherits from Y.
- `[ST]` -> Static member.
- `[F]` -> Field.
- `[P]` -> Property.
- `-` -> Method.