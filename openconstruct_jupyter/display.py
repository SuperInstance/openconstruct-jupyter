"""
Rich display rendering for sense shadows, fleet topology, rooms, ticks, and config.
"""

from __future__ import annotations

import html as html_lib
from typing import Any


def render_fleet(fleet_data: list[dict]) -> str:
    """Render fleet topology as a styled HTML table."""
    if not fleet_data:
        return "<div style='color:#888'>No fleet agents discovered.</div>"
    rows = "".join(
        f"<tr><td>{a['agent_id']}</td><td><b>{a['name']}</b></td>"
        f"<td style='color:{'#4a9' if a['status']=='online' else '#a44'}'>{a['status']}</td>"
        f"<td>{', '.join(a.get('modules', []))}</td></tr>"
        for a in fleet_data
    )
    return (
        "<div style='font-family:monospace;background:#1e1e1e;color:#ddd;padding:12px;border-radius:6px'>"
        "<b>🏗 Fleet Topology</b><br><br>"
        "<table style='border-collapse:collapse'>"
        "<tr><th style='padding:4px 12px;border-bottom:1px solid #555'>ID</th>"
        "<th style='padding:4px 12px;border-bottom:1px solid #555'>Name</th>"
        "<th style='padding:4px 12px;border-bottom:1px solid #555'>Status</th>"
        "<th style='padding:4px 12px;border-bottom:1px solid #555'>Modules</th></tr>"
        f"{rows}</table></div>"
    )


def render_room(room_data: dict) -> str:
    """Render a Plato room as an SVG-style node graph."""
    name = html_lib.escape(room_data.get("name", "?"))
    tiles = room_data.get("tiles", [])
    nodes_html = "".join(
        f'<div style="border:1px solid #4a9;padding:4px 10px;margin:3px;border-radius:6px;'
        f'background:#1a2a1a;display:inline-block">'
        f'{html_lib.escape(t["name"])} <small style="color:#8ac">CR {t.get("cr_score", 0)}</small></div>'
        for t in tiles
    )
    return (
        f"<div style='font-family:monospace;background:#1a1a2a;color:#ddd;padding:12px;border-radius:6px'>"
        f"<b>🏠 Room: {name}</b> <small>({len(tiles)} tiles)</small><br><br>"
        f"{nodes_html}</div>"
    )


def render_tick(message: str) -> str:
    """Render a tick as a chat bubble."""
    safe = html_lib.escape(message)
    return (
        f"<div style='background:#2a3a5a;color:#ddd;padding:8px 14px;margin:4px 0;"
        f"border-radius:10px;max-width:75%;font-family:monospace;display:inline-block'>"
        f"✅ {safe}</div><br>"
    )


def render_shadow(shadow) -> str:
    """Render a sense shadow as styled HTML."""
    sense_type = getattr(shadow, "sense_type", "text")
    output = html_lib.escape(str(getattr(shadow, "output", "")))
    status = "✓" if getattr(shadow, "success", True) else "✗"
    color = "#4a9" if getattr(shadow, "success", True) else "#a44"
    return (
        f"<div style='font-family:monospace;background:#1a1a1a;color:#ddd;padding:10px;"
        f"border-left:3px solid {color};border-radius:4px;margin:4px 0'>"
        f"<b>🔍 Sense: {html_lib.escape(sense_type)}</b> {status}<br>"
        f"<pre style='margin:4px 0;color:#aaa'>{output[:500]}</pre></div>"
    )


def render_config_yaml(config: dict) -> str:
    """Render config as syntax-highlighted YAML-ish HTML."""
    lines = []
    for k, v in config.items():
        if isinstance(v, bool):
            color = "#4a9" if v else "#a44"
            lines.append(f'<span style="color:#88f">{k}</span>: <span style="color:{color}">{v}</span>')
        elif isinstance(v, str):
            lines.append(f'<span style="color:#88f">{k}</span>: <span style="color:#aa4">"{html_lib.escape(v)}"</span>')
        else:
            lines.append(f'<span style="color:#88f">{k}</span>: <span style="color:#ddd">{v}</span>')
    body = "<br>".join(lines)
    return f"<div style='font-family:monospace;background:#1e1e1e;color:#ddd;padding:10px;border-radius:4px'>{body}</div>"
