"""Topology view helper."""


def show_topology(topology):
    from app.views.controller_cli_view import show_topology as _show
    _show(topology.to_dict())
