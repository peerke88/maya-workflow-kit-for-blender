# SPDX-License-Identifier: GPL-3.0-or-later
"""Explicit test-only reference selection; default retains the upstream 2022 audit."""
import importlib.util
import json
import os


def adapter():
    path = os.environ.get('ALLSET_MAYA_REFERENCE_ADAPTER')
    if not path:
        return None
    spec = importlib.util.spec_from_file_location('selected_maya_reference', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def hotkeys(root):
    selected = adapter()
    if selected:
        return selected.hotkeys()
    data = json.loads((root / 'research/maya/hotkeys_default.json').read_text(encoding='utf-8'))['hotkeys']
    assert len(data) == 468, len(data)
    return data


def entry_for(mapping, hotkey):
    selected = adapter()
    return selected.entry_for(mapping, hotkey) if selected else mapping.entry_for(hotkey)


def validate_reviews(mapping, rows):
    selected = adapter()
    if selected:
        selected.validate_reviews(mapping, rows)


def audit_menu_table(root, actual):
    selected = adapter()
    if selected:
        selected.audit_menu_table(root, actual)
    else:
        spec = importlib.util.spec_from_file_location('gen_menu_hotkeys', root / 'tools/gen_menu_hotkeys.py')
        gen = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gen)
        assert gen.table() == actual, 'run python tools/gen_menu_hotkeys.py'
