"""
IPython widgets for interactive agent control.
"""

from __future__ import annotations

from typing import Any

import ipywidgets as widgets
from IPython.display import display

from .kernel import OCClient, FleetAgent


class AgentConfigWidget(widgets.VBox):
    """Dropdown configuration for modules and interface type."""

    def __init__(self, client: OCClient | None = None, **kwargs):
        self._client = client or OCClient()
        self.module_dropdown = widgets.Dropdown(
            options=["vision", "text", "inference", "analysis"],
            value="vision",
            description="Module:",
        )
        self.interface_dropdown = widgets.Dropdown(
            options=["magic", "api", "widget", "cli"],
            value="magic",
            description="Interface:",
        )
        self.apply_btn = widgets.Button(description="Apply", button_style="primary")
        self.apply_btn.on_click(self._on_apply)
        self.output = widgets.Output()
        super().__init__(
            children=[self.module_dropdown, self.interface_dropdown, self.apply_btn, self.output],
            **kwargs,
        )

    def _on_apply(self, btn):
        with self.output:
            print(f"Configured: module={self.module_dropdown.value}, interface={self.interface_dropdown.value}")


class FleetStatusWidget(widgets.VBox):
    """Live fleet health dashboard."""

    def __init__(self, client: OCClient | None = None, **kwargs):
        self._client = client or OCClient()
        self.refresh_btn = widgets.Button(description="Refresh", button_style="info")
        self.refresh_btn.on_click(self._refresh)
        self.status_html = widgets.HTML(value="<i>No fleet data</i>")
        super().__init__(children=[self.refresh_btn, self.status_html], **kwargs)

    def _refresh(self, btn):
        fleet = self._client.discover_fleet()
        rows = "".join(
            f"<tr><td>{a['name']}</td><td>{a['status']}</td><td>{', '.join(a['modules'])}</td></tr>"
            for a in fleet
        )
        self.status_html.value = (
            "<table><tr><th>Agent</th><th>Status</th><th>Modules</th></tr>"
            f"{rows}</table>"
        )


class SenseShadowWidget(widgets.VBox):
    """Rendered sense output (HTML / ANSI)."""

    def __init__(self, **kwargs):
        self.shadow_output = widgets.HTML(value="<i>No shadow captured</i>")
        super().__init__(children=[self.shadow_output], **kwargs)

    def show(self, html: str):
        self.shadow_output.value = html


class RoomGraphWidget(widgets.VBox):
    """Plato room knowledge graph visualization."""

    def __init__(self, client: OCClient | None = None, **kwargs):
        self._client = client or OCClient()
        self.graph_output = widgets.HTML(value="<i>No room loaded</i>")
        super().__init__(children=[self.graph_output], **kwargs)

    def show_room(self, room: dict):
        tiles = room.get("tiles", [])
        nodes = "".join(
            f'<div style="border:1px solid #4a9;padding:4px 8px;margin:2px;border-radius:4px;'
            f'background:#1a2a1a;display:inline-block">{t["name"]} <small>(CR {t["cr_score"]})</small></div>'
            for t in tiles
        )
        self.graph_output.value = (
            f'<div style="font-family:monospace">'
            f'<b>Room: {room.get("name","?")}</b><br>{nodes}</div>'
        )


class TickBoardWidget(widgets.VBox):
    """Scrolling tick messages."""

    def __init__(self, **kwargs):
        self.tick_area = widgets.HTML(value="<i>No ticks</i>")
        self._messages: list[str] = []
        super().__init__(children=[self.tick_area], **kwargs)

    def add_tick(self, message: str):
        self._messages.append(message)
        bubbles = "".join(
            f'<div style="background:#2a3a5a;color:#ddd;padding:6px 10px;margin:3px 0;'
            f'border-radius:8px;max-width:70%">{m}</div>'
            for m in self._messages[-20:]
        )
        self.tick_area.value = bubbles


class PolicyWidget(widgets.VBox):
    """Policy configuration with toggles."""

    def __init__(self, **kwargs):
        self.auto_register = widgets.ToggleButton(value=True, description="Auto-register")
        self.auto_capture = widgets.ToggleButton(value=True, description="Auto-capture")
        self.verbose = widgets.ToggleButton(value=False, description="Verbose")
        self.output = widgets.Output()
        super().__init__(
            children=[self.auto_register, self.auto_capture, self.verbose, self.output],
            **kwargs,
        )

    @property
    def policy(self) -> dict:
        return {
            "auto_register": self.auto_register.value,
            "auto_capture": self.auto_capture.value,
            "verbose": self.verbose.value,
        }
