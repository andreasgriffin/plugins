from __future__ import annotations

import importlib
import sys
from pathlib import Path

BYTECODE_ROOTS = {
    "cpython-310": Path("_bytecode/cpython-310"),
    "cpython-311": Path("_bytecode/cpython-311"),
    "cpython-312": Path("_bytecode/cpython-312"),
}
PACKAGE_NAME = "scheduled_payments"


def _load_payload() -> None:
    cache_tag = sys.implementation.cache_tag
    if cache_tag is None or cache_tag not in BYTECODE_ROOTS:
        supported = ", ".join(sorted(BYTECODE_ROOTS))
        raise ImportError(
            f"Unsupported Python cache tag {cache_tag!r} for {PACKAGE_NAME}. Supported: {supported}"
        )

    package_root = Path(__file__).resolve().parent
    bytecode_root = package_root / BYTECODE_ROOTS[cache_tag]
    if not bytecode_root.is_dir():
        raise ImportError(f"Missing bytecode root for {PACKAGE_NAME}: {bytecode_root}")

    bytecode_root_str = str(bytecode_root)
    if bytecode_root_str not in sys.path:
        sys.path.insert(0, bytecode_root_str)

    module = importlib.import_module(f"{PACKAGE_NAME}.client")
    globals()["PLUGIN_CLIENTS"] = module.PLUGIN_CLIENTS
    if "class_kwargs" in module.__dict__:
        globals()["class_kwargs"] = module.__dict__["class_kwargs"]
        globals()["__all__"] = ["PLUGIN_CLIENTS", "class_kwargs"]
    else:
        globals()["__all__"] = ["PLUGIN_CLIENTS"]


_load_payload()
