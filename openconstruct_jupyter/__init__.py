"""
openconstruct-jupyter — Jupyter notebook integration for OpenConstruct.
"""

__version__ = "0.1.0"

from .magic import load_ipython_extension, unload_ipython_extension
from .widgets import (
    AgentConfigWidget,
    FleetStatusWidget,
    SenseShadowWidget,
    RoomGraphWidget,
    TickBoardWidget,
    PolicyWidget,
)
from .kernel import OCClient

# Module-level convenience functions backed by a default OCClient
_default_client: OCClient | None = None


def _get_client() -> OCClient:
    global _default_client
    if _default_client is None:
        _default_client = OCClient()
    return _default_client


def connect(**kwargs) -> OCClient:
    """Connect this notebook to OpenConstruct. Returns the active client."""
    global _default_client
    _default_client = OCClient(**kwargs)
    _default_client.connect()
    return _default_client


def from_dataframe(df, *, name: str = "data"):
    """Convert a DataFrame into a Plato room."""
    return _get_client().from_dataframe(df, name=name)


def from_function(func, *, name: str = "tool"):
    """Wrap a Python function as an agent tool."""
    return _get_client().from_function(func, name=name)


def from_model(model, *, name: str = "model"):
    """Wrap an ML model as a sense module."""
    return _get_client().from_model(model, name=name)


def from_api(url: str, *, name: str = "api"):
    """Register a REST API as an agent resource."""
    return _get_client().from_api(url, name=name)


def publish_room():
    """Publish the notebook's room with the fleet."""
    return _get_client().publish_room()
