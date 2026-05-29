"""
Plato Room visualizer widget.
"""

from __future__ import annotations

import ipywidgets as widgets
from IPython.display import display

from .kernel import OCClient, PlatoRoom
from .display import render_room


class RoomViewer(widgets.VBox):
    """Interactive Plato Room visualizer."""

    def __init__(self, client: OCClient | None = None, **kwargs):
        self._client = client or OCClient()
        self.header = widgets.HTML(value="<h3>🏠 Plato Room Viewer</h3>")
        self.room_select = widgets.Dropdown(
            options=["(no rooms)"],
            description="Room:",
            layout=widgets.Layout(width="300px"),
        )
        self.load_btn = widgets.Button(description="Load", button_style="primary")
        self.load_btn.on_click(self._load)
        self.body = widgets.HTML(value="<i>Select a room to visualize.</i>")
        controls = widgets.HBox(children=[self.room_select, self.load_btn])
        super().__init__(children=[self.header, controls, self.body], **kwargs)

    def _refresh_rooms(self):
        names = list(self._client.rooms.keys())
        if not names:
            names = ["(no rooms)"]
        self.room_select.options = names

    def _load(self, btn):
        self._refresh_rooms()
        name = self.room_select.value
        if name in self._client.rooms:
            room = self._client.rooms[name]
            self.body.value = render_room(room.to_dict())
        else:
            self.body.value = "<i>No room selected.</i>"
