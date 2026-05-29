"""
Agent-aware kernel hooks and OCClient — the brain behind the magic.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class SenseShadow:
    """A captured sense shadow."""
    shadow_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    sense_type: str = "text"
    output: str = ""
    success: bool = True
    timestamp: float = field(default_factory=time.time)


@dataclass
class PlatoTile:
    """A tile in a Plato room."""
    tile_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    name: str = ""
    value: Any = None
    cr_score: float = 0.0
    source: str = "notebook"


@dataclass
class PlatoRoom:
    """A Plato room — a shared knowledge space."""
    room_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    name: str = "default"
    tiles: list[PlatoTile] = field(default_factory=list)
    created: float = field(default_factory=time.time)

    def add_tile(self, tile: PlatoTile):
        self.tiles.append(tile)

    def to_dict(self) -> dict:
        return {
            "room_id": self.room_id,
            "name": self.name,
            "tiles": [
                {"tile_id": t.tile_id, "name": t.name, "cr_score": t.cr_score, "source": t.source}
                for t in self.tiles
            ],
        }


@dataclass
class FleetAgent:
    """An agent in the fleet."""
    agent_id: str = ""
    name: str = ""
    status: str = "online"
    modules: list[str] = field(default_factory=list)


@dataclass
class Tick:
    """A tick message."""
    tick_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    message: str = ""
    timestamp: float = field(default_factory=time.time)


class OCClient:
    """
    The core OpenConstruct client for Jupyter notebooks.

    Maintains local state (rooms, shadows, fleet) and provides
    the Python API surface (from_dataframe, from_function, etc.).
    """

    def __init__(self, notebook: bool = False, **kwargs):
        self.connected = False
        self.notebook = notebook
        self.shadows: list[SenseShadow] = []
        self.rooms: dict[str, PlatoRoom] = {}
        self.fleet: list[FleetAgent] = []
        self.ticks: list[Tick] = []
        self.tools: dict[str, Callable] = {}
        self.api_resources: dict[str, dict] = {}
        self._default_room = PlatoRoom(name="notebook")

    # --- Connection ---

    def connect(self) -> dict:
        """Connect to the OpenConstruct network."""
        self.connected = True
        self.fleet = [
            FleetAgent(agent_id="self", name="notebook-agent", status="online", modules=["vision", "text"]),
        ]
        return {"status": "connected", "agent_id": "self"}

    # --- Fleet ---

    def discover_fleet(self) -> list[dict]:
        """Return fleet topology."""
        return [
            {"agent_id": a.agent_id, "name": a.name, "status": a.status, "modules": a.modules}
            for a in self.fleet
        ]

    # --- Shadows ---

    def register_shadow(self, sense_type: str, output: str, success: bool = True) -> SenseShadow:
        shadow = SenseShadow(sense_type=sense_type, output=output, success=success)
        self.shadows.append(shadow)
        return shadow

    # --- Rooms ---

    def load_room(self, name: str, context: str = "") -> PlatoRoom:
        if name not in self.rooms:
            self.rooms[name] = PlatoRoom(name=name)
        if context:
            tile = PlatoTile(name="cell_context", value=context, cr_score=0.5)
            self.rooms[name].add_tile(tile)
        return self.rooms[name]

    def publish_room(self) -> dict:
        """Publish the default room to the fleet."""
        self._default_room.name = "published-notebook"
        return self._default_room.to_dict()

    # --- Ticks ---

    def post_tick(self, message: str) -> Tick:
        tick = Tick(message=message)
        self.ticks.append(tick)
        return tick

    # --- Integration helpers ---

    def from_dataframe(self, df, *, name: str = "data") -> PlatoTile:
        """Convert a DataFrame into a Plato room tile with CR score."""
        try:
            rows = len(df)
            cols = len(df.columns)
            cr = min(1.0, (rows * cols) / 1000)
        except Exception:
            cr = 0.1
        tile = PlatoTile(name=name, value=df, cr_score=round(cr, 2), source="dataframe")
        self._default_room.add_tile(tile)
        return tile

    def from_function(self, func: Callable, *, name: str = "tool") -> dict:
        """Register a Python function as an agent tool."""
        self.tools[name] = func
        return {"name": name, "type": "function", "registered": True}

    def from_model(self, model, *, name: str = "model") -> dict:
        """Register an ML model as a sense module."""
        self.fleet.append(
            FleetAgent(agent_id=name, name=name, status="online", modules=["inference"])
        )
        return {"name": name, "type": "model", "registered": True}

    def from_api(self, url: str, *, name: str = "api") -> dict:
        """Register a REST API as an agent resource."""
        entry = {"url": url, "name": name, "type": "api"}
        self.api_resources[name] = entry
        return entry
