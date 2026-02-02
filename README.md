# .NET DLL Inspector v2.26

Snažan i lagan Python alat za dubinsku analizu .NET sklopova (assemblies). Dizajniran posebno za modere (Space Engineers, Torch, itd.) kako bi brzo mapirali nepoznate API-je, otkrili skrivene članove i razumjeli hijerarhiju klasa bez dekompilacije.

---

## ✨ Nove značajke (v2.26)

- **C# Type Cleanup**: Pretvara sirove .NET tipove u čitljiv C# format (npr. `Int64` -> `long`, `Single` -> `float`).
- **Generics Support**: Pravilno formatira generičke liste i rječnike (npr. `List<IMyPlayer>` umjesto `List`1`).
- **Inheritance Tracking**: Uz svaku klasu ispisuje njezinu roditeljsku klasu (Base Class), što olakšava navigaciju kroz SE framework.
- **VS Code Integration**: Dodan `-o` switch za trenutno otvaranje izvještaja u novom tabu aktivnog VS Code prozora.

---

## 📦 Instalacija i preduvjeti

- **Python 3.x**
- Paket: `pip install pythonnet`
- VS Code (opcionalno, za `-o` switch)

---

## ⚙️ Konfiguracija

Kod prvog pokretanja, alat generira `dll-check2.ini`.

| Postavka | Opis |
| :--- | :--- |
| `DefaultPath` | Putanja do foldera s DLL-ovima koje najčešće skeniraš. |
| `FilterKeywords` | Ključne riječi za filtriranje DLL datoteka (npr. `Sandbox, VRage`). |

---

## ▶️ Korištenje i Switchevi

### 🎯 "Sniper" Mode (Preporučeno)
Kada tražiš točno određeni podatak unutar ogromne klase:
```bash
# Traži 'Players' unutar 'MySession', ispisuje duboke detalje i otvara u VS Code-u
python dll-check2.py -y -d -s MySession -f Players -o
```

### 🔍 Popis svih opcija
| Switch | Dugi oblik | Opis |
| :--- | :--- | :--- |
| `-s` | `--search` | Ključna riječ za Naziv Klase ili Namespace. |
| `-f` | `--filter` | Ključna riječ za Člana (metoda, field, property). |
| `-d` | `--deep` | Deep mode: Uključuje Fieldove `[F]` i Evente `[E]`. |
| `-e` | `--ext` | Extended mode: Uključuje Propertyje `[P]`. |
| `-y` | `--default`| Preskače upit za putanju (koristi onu iz INI-ja). |
| `-o` | `--open` | Automatski otvara rezultat u VS Code-u. |
| `-h` | `--help` | Prikazuje kratke upute. |

---

## 📖 Kako čitati izvještaj?

v2.26 donosi čitljivost koja odgovara tvom C# kôdu:

| Oznaka | Značenje | Napomena |
| :--- | :--- | :--- |
| `Class: X : Y` | Klasa X nasljeđuje Y | **Novo u v2.26** |
| `[ST]` | Statički član | Pristupaš mu sa `Klasa.Static...` |
| `[F]` | Field (Varijabla) | Zahtijeva `-d` |
| `[P]` | Property | Zahtijeva `-e` ili `-d` |
| `-` | Metoda | Uvijek se prikazuje |

### Primjer očišćenog ispisa:
```text
FILE: Sandbox.Game.dll
========================================
[NS: Sandbox.Game.World] -> Class: MySession : MySessionBase
  [P] [ST] MyFactionManager Factions
  [P] [ST] MyPlayerCollection Players
  - [ST] void SetLastDamage(MyDamageInformation info)
```

---

## 🗂 Struktura projekta

```text
project-root/
├── dll-check2.py
├── dll-check2.ini       # Automatska konfiguracija
├── Dependencies/        # DLL datoteke za analizu
└── doc/                 # Generirani izvještaji (.txt)
```

---

## 📜 Licenca
MIT License.