# dll-check2.py
import os
import sys
import clr
import configparser
import re
import subprocess
import shutil
from datetime import datetime

# --- CONFIG ---

script_full_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_full_path)
script_base_name = os.path.splitext(os.path.basename(__file__))[0]
config_file = os.path.join(script_dir, "config_check.ini")

config = configparser.ConfigParser()

VERSION = "2.70"

# ============================================================
# HELP STRINGS
# ============================================================

HELP_RULES_PB = """
.NET DLL Inspector v{ver} -- Rules: Space Engineers Programmable Block (PB)
======================================================================
Context:  Space Engineers (SE) In-Game Scripting (Programmable Block)
======================================================================

RULE        DESCRIPTION
----------------------------------------------------------------------
Platform    .NET Framework 4.6 / C# 6.0 syntax ONLY
API         VRage.Game, VRageMath, Sandbox.ModAPI.Ingame namespaces
Constraint  NO LINQ, NO Reflection, NO file access, NO multithreading
Style       Use string.Format() instead of string interpolation ($"...")
Language    Respond in Croatian (ijekavica) or English. No Serbian/Ekavica.
Comments    All code comments must be in ENGLISH
File Header MANDATORY - put relative file path as first line comment
            Example: // Scripts/Miner/RefinerControl.cs
======================================================================
""".format(ver=VERSION)

HELP_RULES_PLUGIN = """
.NET DLL Inspector v{ver} -- Rules: Torch Server Plugin
======================================================================
Target:  Torch v1.3.1.328-master | SE 1.208.15
======================================================================

RULE        DESCRIPTION
----------------------------------------------------------------------
Platform    .NET Framework 4.8 or .NET 6+ (depending on Torch version)
API         Torch.API, VRage.Game, Sandbox.ModAPI (Full API, not Ingame)
Constraint  LINQ, Reflection, Multithreading, File I/O ARE allowed
Thread      Use MySandboxGame.Static.Invoke for game-world interactions
Language    Respond in Croatian (ijekavica) or English. No Serbian/Ekavica.
Comments    All code comments must be in ENGLISH
File Header MANDATORY - put relative file path as first line comment
======================================================================
""".format(ver=VERSION)

HELP_RULES_MOD = """
.NET DLL Inspector v{ver} -- Rules: Space Engineers World Mod
======================================================================
Context:  Space Engineers (SE) World Modding (Script Mod)
======================================================================

RULE        DESCRIPTION
----------------------------------------------------------------------
Platform    .NET Framework 4.8 / C# 7.3 or 8.0
API         Sandbox.ModAPI, VRage.Game.ModAPI, Sandbox.Common.ObjectBuilders
Key Class   Inherit from MySessionComponentBase or use [MyEntityComponentDescriptor]
Constraint  LINQ and Reflection ARE allowed in Mods (unlike PB scripts)
            Avoid direct File I/O or prohibited System calls (Workshop compat)
Gateway     Use MyAPIGateway for Entities, Terminal, Session access
Language    Respond in Croatian (ijekavica) or English. No Serbian/Ekavica.
Comments    All code comments must be in ENGLISH
File Header MANDATORY - put relative file path as first line comment
======================================================================
""".format(ver=VERSION)

HELP_SHORT = """
.NET DLL Inspector v{ver}
======================================================================
OPTION              DESCRIPTION
----------------------------------------------------------------------
-s <term>           Filter TYPE names (Namespace.TypeName)
-f <term>           Filter MEMBER names (methods, properties, fields)
-x                  Exact word match (no substring)
-e                  Include properties
-d                  Deep mode (fields + properties)
-a                  Scan ALL DLL files (ignore config keywords)
--deps              Show dependency graph
-y                  Use default path from config
-o                  Open generated log in VSCode
--clear             Delete all generated inspect log files/directory
-h / --help         Show this help (no examples)
--help:extend       Show full help with examples
--help:rules:pb     Show coding rules for SE Programmable Block scripting
--help:rules:plugin Show coding rules for Torch Server Plugin development
--help:rules:mod    Show coding rules for SE World Modding
======================================================================
""".format(ver=VERSION)

HELP_EXTENDED = """
.NET DLL Inspector v{ver}
======================================================================
OPTION              DESCRIPTION
----------------------------------------------------------------------
-s <term>           Filter TYPE names (Namespace.TypeName)
-f <term>           Filter MEMBER names (methods, properties, fields)
-x                  Exact word match (no substring)
-e                  Include properties
-d                  Deep mode (fields + properties)
-a                  Scan ALL DLL files (ignore config keywords)
--deps              Show dependency graph
-y                  Use default path from config
-o                  Open generated log in VSCode
--clear             Delete all generated inspect log files/directory
-h / --help         Show this help (no examples)
--help:extend       Show full help with examples
--help:rules:pb     Show coding rules for SE Programmable Block scripting
--help:rules:plugin Show coding rules for Torch Server Plugin development
--help:rules:mod    Show coding rules for SE World Modding
======================================================================
EXAMPLES
----------------------------------------------------------------------
BASIC SEARCH (TYPE MATCHING)

-s Math
  Matches any type whose full name contains "Math": MathHelper, MyMathConstants, etc.
  Output: methods only. Log: 2026-03-10_112229_Math.txt

-s Math -x
  Exact word match only. Matches "Math" but NOT "MathHelper" or "MathConstants".
  Output: methods only. Log: 2026-03-10_112229_Math.txt

-s Math -f Add
  Types containing "Math" AND members whose name contains "Add".
  Output: only matching methods. Useful to narrow down API surface quickly.

PROPERTY / FIELD DETAIL LEVELS

-s ContractBlock -e
  Types containing "ContractBlock" + their public PROPERTIES (marked [P]).
  Output: methods + properties. Moderate detail.

-s ContractBlock -d
  Deep mode: methods + properties + PUBLIC FIELDS (marked [F]).
  Output: maximum detail. Use this to discover data structure of block types.

-s ContractBlock -d -f Id
  Deep mode, additionally filter members by "Id".
  Output: only fields/properties/methods whose name contains "Id". Very narrow.

ECONOMY / CONTRACT EXAMPLES

-s EconomyContract -y -o
  Search for EconomyContract types using default DLL path from config, open result in VSCode.
  Useful for exploring contract definitions in Sandbox / VRage economy system.

-s EconomyContract -d -y -o
  Same as above but deep mode: shows ALL fields and properties of contract types.
  Use this to find money amounts, reward fields, NPC assignee IDs, deadlines, etc.

-s ContractBlock -f GetContract -y -o
  Find method GetContract on any type matching ContractBlock.
  Output: exact method signatures, parameter types and names.

STORE / ECONOMY BLOCK EXAMPLES

-s StoreBlock -y -o
  Basic scan of StoreBlock types: public methods only.
  Output: method list. Gives quick overview of what the block exposes.

-s StoreBlock -e -y -o
  StoreBlock types + properties. Reveals configurable fields like IsOpen, StoreName.

-s StoreBlock -d -y -o
  StoreBlock deep scan: all fields + properties + methods.
  Output: most complete picture. Use when building plugin interactions with stores.

-s StoreBlock -f Insert -d -y -o
  Deep scan, only members matching "Insert". Finds insertion methods for store items.

ALL DLL SCAN

-s ContractBlock -a -y
  Ignore keyword filter, scan ALL DLLs in the directory.
  Use when you're not sure which assembly defines a type.

DEPENDENCY GRAPH

--deps -y
  Print which DLLs reference which other DLLs (filtered by config keywords).
  Useful for understanding plugin dependency chains.

======================================================================
NOTE ON LOG FILES
----------------------------------------------------------------------
All logs are saved with a timestamp prefix in the configured log directory.
Example filename: 2026-03-10_112229_ContractBlock_f_GetContract.txt
Use --clear to delete all generated logs at once.
======================================================================
""".format(ver=VERSION)


# ============================================================
# CONFIG
# ============================================================

def load_config():
    defaults = {
        'DefaultPath': os.path.join(script_dir, "Dependencies"),
        'FilterKeywords': "Torch,Sandbox,VRage,SpaceEngineers,Discord",
        'LogDir': ".inspect",
        'VSCodePath': r"c:\dev\VSCode\bin\code.cmd"
    }

    updated = False

    if not os.path.exists(config_file):
        config['SETTINGS'] = defaults
        updated = True
    else:
        config.read(config_file)
        if 'SETTINGS' not in config:
            config['SETTINGS'] = {}
            updated = True
        for key, value in defaults.items():
            if not config.has_option('SETTINGS', key):
                config.set('SETTINGS', key, value)
                updated = True

    if updated:
        with open(config_file, 'w') as f:
            config.write(f)

    return {
        'path': config.get('SETTINGS', 'DefaultPath'),
        'keywords': config.get('SETTINGS', 'FilterKeywords').split(','),
        'log_dir': config.get('SETTINGS', 'LogDir'),
        'vscode_path': config.get('SETTINGS', 'VSCodePath')
    }


cfg = load_config()


# ============================================================
# UTILITIES
# ============================================================

def detect_keywords_from_directory(dll_list):
    roots = set()
    for dll in dll_list:
        name = os.path.splitext(dll)[0]
        root = name.split('.')[0]
        if len(root) > 2:
            roots.add(root)
    return sorted(roots)


def get_timestamp_log_path(directory, search_term, member_filter):
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    clean_s = re.sub(r'[^\w]', '', search_term) if search_term else "All"
    clean_f = "_f_" + re.sub(r'[^\w]', '', member_filter) if member_filter else ""
    base_name = "{ts}_{s}{f}.txt".format(ts=ts, s=clean_s, f=clean_f)
    return os.path.join(directory, base_name)


def exact_or_contains(value, term, exact):
    if not term:
        return True
    if exact:
        pattern = r'\b' + re.escape(term) + r'\b'
        return re.search(pattern, value, re.IGNORECASE)
    return term.lower() in value.lower()


def format_type_name(t):
    if t is None:
        return "void"

    name = t.Name
    mappings = {
        "Int64": "long",
        "UInt64": "ulong",
        "Int32": "int",
        "UInt32": "uint",
        "Single": "float",
        "Double": "double",
        "Boolean": "bool",
        "String": "string"
    }

    if name in mappings:
        return mappings[name]

    if '`' in name:
        base_name = name.split('`')[0]
        try:
            gen_args = t.GetGenericArguments()
            args_names = [format_type_name(a) for a in gen_args]
            return "{base}<{args}>".format(base=base_name, args=', '.join(args_names))
        except:
            return name

    return name


# ============================================================
# PARAMETER SUMMARY (printed at run start)
# ============================================================

PARAM_DESCRIPTIONS = {
    '-y': "Use default DLL path from config ({path})",
    '-o': "Open generated log in VSCode after scan",
    '-d': "Deep mode: include fields + properties in output",
    '-e': "Include properties in output (lighter than -d)",
    '-x': "Exact word match (no substring matching)",
    '-a': "Scan ALL DLL files (ignore config keyword filter)",
    '--deps': "Show dependency graph between DLL files",
}


def print_active_params(args, cfg, search_term, member_filter):
    active = []
    for flag, desc in PARAM_DESCRIPTIONS.items():
        if flag in args:
            d = desc
            if '{path}' in d:
                d = d.format(path=cfg['path'])
            active.append("  {f:<8} {d}".format(f=flag, d=d))
    if search_term:
        active.append("  {f:<8} Searching TYPE names containing: \"{v}\"".format(f='-s', v=search_term))
    if member_filter:
        active.append("  {f:<8} Filtering MEMBER names containing: \"{v}\"".format(f='-f', v=member_filter))

    if active:
        print("\nActive parameters:")
        for line in active:
            print(line)

    # Suggest refinements
    print("\nTips for more detail:")
    if '-d' not in args and '-e' not in args:
        print("  Add -e to include properties, or -d for full deep scan (fields + properties).")
    if search_term and '-f' not in args:
        print("  Add -f <name> to filter members, e.g.: -s {s} -f Get".format(s=search_term))
    if search_term and '-x' not in args:
        print("  Add -x for exact type name match only.")
    print()


# ============================================================
# DEPENDENCIES
# ============================================================

def build_dependency_map(directory, dll_files):
    import System.Reflection as Reflection
    dep_map = {}

    for dll in dll_files:
        try:
            asm = Reflection.Assembly.LoadFrom(os.path.join(directory, dll))
            refs = [r.Name + ".dll" for r in asm.GetReferencedAssemblies()]
            dep_map[dll] = refs
        except:
            dep_map[dll] = []

    return dep_map


# ============================================================
# INSPECT
# ============================================================

def inspect_dll(dll_path, search_term=None, member_filter=None,
                ext_mode=False, deep_mode=False, exact_mode=False):

    results = []
    version = "Unknown"

    try:
        import System.Reflection as Reflection
        from System.Reflection import ReflectionTypeLoadException

        assembly = Reflection.Assembly.LoadFrom(os.path.abspath(dll_path))
        version = assembly.GetName().Version

        try:
            types = assembly.GetTypes()
        except ReflectionTypeLoadException as e:
            types = [t for t in e.Types if t is not None]

        for t in types:
            if not t.IsPublic:
                continue

            type_full = "{ns}.{name}".format(ns=t.Namespace, name=t.Name)

            if not exact_or_contains(type_full, search_term, exact_mode):
                continue

            flags = (Reflection.BindingFlags.Public |
                     Reflection.BindingFlags.Instance |
                     Reflection.BindingFlags.Static |
                     Reflection.BindingFlags.FlattenHierarchy)

            temp_items = []

            if deep_mode:
                for f in t.GetFields(flags):
                    if exact_or_contains(f.Name, member_filter, exact_mode):
                        prefix = "[ST] " if f.IsStatic else ""
                        temp_items.append("  [F] {p}{ft} {n}".format(
                            p=prefix, ft=format_type_name(f.FieldType), n=f.Name))

            for m in t.GetMethods(flags):
                if m.IsSpecialName:
                    continue
                if exact_or_contains(m.Name, member_filter, exact_mode):
                    params = ", ".join(
                        "{t} {n}".format(t=format_type_name(p.ParameterType), n=p.Name)
                        for p in m.GetParameters()
                    )
                    prefix = "[ST] " if m.IsStatic else ""
                    temp_items.append("  - {p}{rt} {n}({params})".format(
                        p=prefix, rt=format_type_name(m.ReturnType), n=m.Name, params=params))

            if ext_mode or deep_mode:
                for p in t.GetProperties(flags):
                    if exact_or_contains(p.Name, member_filter, exact_mode):
                        prefix = "[ST] " if any(a.IsStatic for a in p.GetAccessors()) else ""
                        temp_items.append("  [P] {p}{pt} {n}".format(
                            p=prefix, pt=format_type_name(p.PropertyType), n=p.Name))

            if temp_items:
                t_type = "Struct" if t.IsValueType else "Class"
                base_info = " : {n}".format(n=t.BaseType.Name) if t.BaseType and t.BaseType.Name != "Object" else ""
                results.append("\n[NS: {ns}] -> {tt}: {tn}{bi}".format(
                    ns=t.Namespace, tt=t_type, tn=t.Name, bi=base_info))
                results.extend(temp_items)

    except:
        pass

    return version, results


# ============================================================
# CLEAR
# ============================================================

def do_clear():
    log_dir_full = os.path.join(script_dir, cfg['log_dir'])
    if not os.path.exists(log_dir_full):
        print("[--clear] Log directory does not exist: {d}".format(d=log_dir_full))
        return
    count = 0
    for fname in os.listdir(log_dir_full):
        fpath = os.path.join(log_dir_full, fname)
        if os.path.isfile(fpath):
            os.remove(fpath)
            count += 1
    # Optionally remove the directory itself if empty
    try:
        os.rmdir(log_dir_full)
        print("[--clear] Removed {c} file(s) and deleted directory: {d}".format(c=count, d=log_dir_full))
    except OSError:
        print("[--clear] Removed {c} file(s) from: {d}".format(c=count, d=log_dir_full))


# ============================================================
# MAIN
# ============================================================

def main():

    args = sys.argv[1:]
    joined = " ".join(args)

    # --- HELP VARIANTS ---
    if "--help:rules:pb" in args:
        print(HELP_RULES_PB)
        return

    if "--help:rules:plugin" in args:
        print(HELP_RULES_PLUGIN)
        return

    if "--help:rules:mod" in args:
        print(HELP_RULES_MOD)
        return

    if "--help:extend" in args:
        print(HELP_EXTENDED)
        return

    if "-h" in args or "--help" in args:
        print(HELP_SHORT)
        return

    # --- CLEAR ---
    if "--clear" in args:
        do_clear()
        return

    # --- PARSE STANDARD FLAGS ---
    ext_mode   = "-e" in args
    deep_mode  = "-d" in args
    exact_mode = "-x" in args
    scan_all   = "-a" in args
    deps_mode  = "--deps" in args
    use_default = "-y" in args
    open_vscode = "-o" in args

    search_term  = args[args.index("-s") + 1] if "-s" in args and args.index("-s") + 1 < len(args) else None
    member_filter = args[args.index("-f") + 1] if "-f" in args and args.index("-f") + 1 < len(args) else None

    print("--- .NET DLL Inspector v{v} ---".format(v=VERSION))

    # Print active param summary
    print_active_params(args, cfg, search_term, member_filter)

    target_dir = os.path.abspath(cfg['path']) if use_default else input("Path: ").strip()

    if not os.path.isdir(target_dir):
        print("Invalid directory.")
        return

    all_dlls = [f for f in os.listdir(target_dir) if f.lower().endswith(".dll")]
    detected = detect_keywords_from_directory(all_dlls)
    print('Found Keywords: "{kw}"'.format(kw=",".join(detected)))

    dll_files = all_dlls if scan_all else [
        f for f in all_dlls
        if any(k.lower() in f.lower() for k in cfg['keywords'])
    ]

    if deps_mode:
        dep_map = build_dependency_map(target_dir, dll_files)
        print("\nDEPENDENCIES:\n")
        for dll, refs in dep_map.items():
            print(dll)
            for r in refs:
                if r in dll_files:
                    print("  -> {r}".format(r=r))
        return

    log_dir_full = os.path.join(script_dir, cfg['log_dir'])
    if not os.path.exists(log_dir_full):
        os.makedirs(log_dir_full)

    log_path = get_timestamp_log_path(log_dir_full, search_term, member_filter)

    total_matches = 0

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("REPORT: {d}\nSEARCH: {s} | FILTER: {mf}\n".format(
            d=target_dir, s=search_term, mf=member_filter))
        f.write("=" * 60 + "\n")

        for index, dll in enumerate(dll_files, start=1):
            print("\r[{i}/{t}] Analyzing {dll}".format(
                i=index, t=len(dll_files), dll=dll[:30].ljust(30)), end="", flush=True)

            version, matches = inspect_dll(
                os.path.join(target_dir, dll),
                search_term,
                member_filter,
                ext_mode,
                deep_mode,
                exact_mode
            )

            if matches:
                total_matches += 1
                f.write("\nFILE: {dll} (v{v})\n".format(dll=dll, v=version))
                f.write("-" * 60 + "\n")
                f.write("\n".join(matches) + "\n")

        if total_matches == 0:
            f.write("\nNo results found.\n")

    if total_matches == 0:
        print("\n\n[!] No results found. (Log: {f})".format(f=os.path.basename(log_path)))
    else:
        print("\n\nDONE! {n} file(s) matched.".format(n=total_matches))
        print("Results saved: {f}".format(f=os.path.basename(log_path)))

    if open_vscode:
        vscode_cmd = cfg['vscode_path']
        if os.path.exists(vscode_cmd):
            subprocess.run([vscode_cmd, log_path], shell=True)
        else:
            os.startfile(log_path)


if __name__ == "__main__":
    main()