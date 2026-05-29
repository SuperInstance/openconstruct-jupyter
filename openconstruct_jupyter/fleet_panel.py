"""
Fleet status dashboard widget — a higher-level convenience wrapper.
"""

from __future__ import annotations

import ipywidgets as widgets
from IPython.display import display

from .kernel import OCClient
from .display import render_fleet


class FleetPanel(widgets.VBox):
    """Full fleet status dashboard with auto-refresh capability."""

    def __init__(self, client: OCClient | None = None, **kwargs):
        self._client = client or OCClient()
        self.header = widgets.HTML(value="<h3>🏗 OpenConstruct Fleet</h3>")
        self.body = widgets.HTML(value="<i>Click Refresh to discover fleet agents.</i>")
        self.refresh_btn = widgets.Button(
            description="🔄 Refresh", button_style="info", layout=widgets.Layout(width="120px")
        )
        self.refresh_btn.on_click(self._refresh)
        self.connect_btn = widgets.Button(
            description="⚡ Connect", button_style="success", layout=widgets.Layout(width="120px")
        )
        self.connect_btn.on_click(self._connect)
        button_row = widgets.HBox(children=[self.connect_btn, self.refresh_btn])
        super().__init__(children=[self.header, button_row, self.body], **kwargs)

    def _connect(self, btn):
        self._client.connect()
        self._refresh(btn)

    def _refresh(self, btn):
        fleet = self._client.discover_fleet()
        self.body.value = render_fleet(fleet)
