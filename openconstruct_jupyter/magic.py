"""
%%openconstruct cell magic for IPython / Jupyter.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import display, HTML, Javascript

from .kernel import OCClient
from .display import render_fleet, render_room, render_tick, render_shadow


@magics_class
class OpenConstructMagics(Magics):
    """IPython magics for OpenConstruct."""

    def __init__(self, shell=None, **kwargs):
        super().__init__(shell, **kwargs)
        self._client: OCClient | None = None

    def _get_client(self) -> OCClient:
        if self._client is None:
            self._client = OCClient()
        return self._client

    @magic_arguments()
    @argument("--sense", type=str, default=None, help="Capture cell output as a sense shadow (e.g. vision, text)")
    @argument("--tick", type=str, default=None, help="Post a tick message")
    @argument("--room", type=str, default=None, help="Create or load a Plato room")
    @argument("--fleet", action="store_true", help="Show fleet discovery inline")
    @cell_magic
    def openconstruct(self, line: str, cell: str):
        """OpenConstruct cell magic."""
        args = parse_argstring(self.openconstruct, line)
        client = self._get_client()

        if args.fleet:
            fleet_data = client.discover_fleet()
            display(HTML(render_fleet(fleet_data)))
            return

        if args.tick:
            client.post_tick(args.tick)
            display(HTML(render_tick(args.tick)))
            return

        if args.room:
            room_data = client.load_room(args.room, context=cell)
            display(HTML(render_room(room_data)))
            return

        if args.sense:
            # Execute cell, capture output as a sense shadow
            result = self.shell.run_cell(cell)
            shadow = client.register_shadow(
                sense_type=args.sense,
                output=str(result.result) if result.result else "",
                success=result.success,
            )
            display(HTML(render_shadow(shadow)))
            return

        # Default: execute and show raw output
        self.shell.run_cell(cell)


def load_ipython_extension(ipython):
    """Register the OpenConstruct magics with IPython."""
    ipython.register_magics(OpenConstructMagics)


def unload_ipython_extension(ipython):
    """Unregister the OpenConstruct magics (no-op, IPython handles it)."""
    pass
