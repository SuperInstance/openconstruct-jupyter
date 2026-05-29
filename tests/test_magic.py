"""
Tests for openconstruct-jupyter.
"""

import pytest
from unittest.mock import MagicMock, patch


# ── Kernel / OCClient ──────────────────────────────────────────────

class TestOCClient:
    def setup_method(self):
        from openconstruct_jupyter.kernel import OCClient
        self.client = OCClient()

    def test_connect(self):
        result = self.client.connect()
        assert result["status"] == "connected"
        assert self.client.connected is True

    def test_discover_fleet_empty(self):
        fleet = self.client.discover_fleet()
        assert fleet == []

    def test_discover_fleet_after_connect(self):
        self.client.connect()
        fleet = self.client.discover_fleet()
        assert len(fleet) == 1
        assert fleet[0]["name"] == "notebook-agent"

    def test_register_shadow(self):
        shadow = self.client.register_shadow("vision", "hello world")
        assert shadow.sense_type == "vision"
        assert shadow.output == "hello world"
        assert shadow.success is True
        assert len(self.client.shadows) == 1

    def test_register_shadow_failure(self):
        shadow = self.client.register_shadow("text", "error", success=False)
        assert shadow.success is False

    def test_post_tick(self):
        tick = self.client.post_tick("test tick")
        assert tick.message == "test tick"
        assert len(self.client.ticks) == 1

    def test_load_room_creates_new(self):
        room = self.client.load_room("test-room")
        assert room.name == "test-room"
        assert "test-room" in self.client.rooms

    def test_load_room_with_context(self):
        room = self.client.load_room("ctx-room", context="some context")
        assert len(room.tiles) == 1
        assert room.tiles[0].value == "some context"

    def test_load_room_idempotent(self):
        self.client.load_room("same-room")
        self.client.load_room("same-room")
        assert len(self.client.rooms) == 1

    def test_publish_room(self):
        result = self.client.publish_room()
        assert "room_id" in result

    def test_from_dataframe(self):
        import pandas as pd
        df = pd.DataFrame({"x": range(50), "y": range(50)})
        tile = self.client.from_dataframe(df, name="test_df")
        assert tile.name == "test_df"
        assert tile.source == "dataframe"
        assert tile.cr_score > 0

    def test_from_function(self):
        def my_func(x):
            return x + 1
        result = self.client.from_function(my_func, name="adder")
        assert result["registered"] is True
        assert "adder" in self.client.tools

    def test_from_model(self):
        class M:
            pass
        result = self.client.from_model(M(), name="test_model")
        assert result["registered"] is True

    def test_from_api(self):
        result = self.client.from_api("https://example.com", name="ex_api")
        assert result["type"] == "api"
        assert "ex_api" in self.client.api_resources


# ── Display rendering ──────────────────────────────────────────────

class TestDisplay:
    def test_render_fleet_empty(self):
        from openconstruct_jupyter.display import render_fleet
        html = render_fleet([])
        assert "No fleet agents" in html

    def test_render_fleet_with_agents(self):
        from openconstruct_jupyter.display import render_fleet
        fleet = [{"agent_id": "a1", "name": "agent-1", "status": "online", "modules": ["vision"]}]
        html = render_fleet(fleet)
        assert "agent-1" in html
        assert "online" in html

    def test_render_room(self):
        from openconstruct_jupyter.display import render_room
        room = {"name": "test", "tiles": [{"name": "tile1", "cr_score": 0.5}]}
        html = render_room(room)
        assert "test" in html
        assert "tile1" in html

    def test_render_tick(self):
        from openconstruct_jupyter.display import render_tick
        html = render_tick("hello tick")
        assert "hello tick" in html
        assert "✅" in html

    def test_render_shadow(self):
        from openconstruct_jupyter.display import render_shadow
        from openconstruct_jupyter.kernel import SenseShadow
        shadow = SenseShadow(sense_type="vision", output="test output")
        html = render_shadow(shadow)
        assert "vision" in html
        assert "test output" in html

    def test_render_config_yaml(self):
        from openconstruct_jupyter.display import render_config_yaml
        html = render_config_yaml({"debug": True, "name": "test"})
        assert "debug" in html
        assert "test" in html


# ── Magic ──────────────────────────────────────────────────────────

class TestMagic:
    def test_load_and_unload(self):
        from openconstruct_jupyter.magic import load_ipython_extension, unload_ipython_extension
        ipython = MagicMock()
        load_ipython_extension(ipython)
        ipython.register_magics.assert_called_once()
        unload_ipython_extension(ipython)  # should not raise


# ── Widgets ────────────────────────────────────────────────────────

class TestWidgets:
    def test_agent_config_widget(self):
        from openconstruct_jupyter.widgets import AgentConfigWidget
        w = AgentConfigWidget()
        assert w.module_dropdown.value == "vision"

    def test_fleet_status_widget(self):
        from openconstruct_jupyter.widgets import FleetStatusWidget
        w = FleetStatusWidget()
        assert "No fleet data" in w.status_html.value

    def test_sense_shadow_widget(self):
        from openconstruct_jupyter.widgets import SenseShadowWidget
        w = SenseShadowWidget()
        w.show("<b>test</b>")
        assert "<b>test</b>" in w.shadow_output.value

    def test_tick_board_widget(self):
        from openconstruct_jupyter.widgets import TickBoardWidget
        w = TickBoardWidget()
        w.add_tick("hello")
        assert "hello" in w.tick_area.value

    def test_policy_widget(self):
        from openconstruct_jupyter.widgets import PolicyWidget
        w = PolicyWidget()
        assert w.policy["auto_register"] is True

    def test_room_graph_widget(self):
        from openconstruct_jupyter.widgets import RoomGraphWidget
        w = RoomGraphWidget()
        w.show_room({"name": "test", "tiles": [{"name": "t1", "cr_score": 0.7}]})
        assert "t1" in w.graph_output.value
