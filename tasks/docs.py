import os
import shutil
from typing import Any

from invoke.tasks import task

from .colors import Color, colorize
from .system import (
    PTY,
    get_current_system,
)

SYSTEM = get_current_system()

@task
def clean(c_r: Any) -> None:
    """Clean documentation build folder"""
    site_dir = "site"
    if os.path.exists(site_dir):
        shutil.rmtree(site_dir)


@task
def build(c_r: Any) -> None:
    """Build Zensical documentation."""
    tmp_str = colorize(
        "\nBuilding Zensical documentation...\n",
        color=Color.HEADER,
        bold=True
    )
    print(tmp_str)
    _command = "zensical build --clean"
    print(f">>> {colorize(_command, color=Color.OKBLUE)}\n")
    c_r.run(_command, pty=PTY)


@task
def serve(c_r: Any) -> None:
    """Serve Zensical documentation with hot reload."""
    tmp_str = colorize(
        "\nStarting Zensical server with hot reload...\n",
        color=Color.HEADER,
        bold=True
    )
    print(tmp_str)

    _command = "zensical serve"
    print(f">>> {colorize(_command, color=Color.OKBLUE)}\n")

    c_r.run(_command, pty=PTY)


@task
def deploy(c_r: Any) -> None:
    """Build documentation for GitHub Pages deployment."""
    tmp_str = colorize(
        "\nPreparing documentation for GitHub Pages deployment...\n",
        color=Color.HEADER,
        bold=True
    )
    print(tmp_str)
    _command = "zensical build --clean"
    print(f">>> {colorize(_command, color=Color.OKBLUE)}\n")
    c_r.run(_command, pty=PTY)


@task(post=[clean, build], default=True)
def all(c_r: Any) -> None:
    """Clean and build documentation."""


@task
def deploy_version(c_r: Any, version: str, alias: str = "latest") -> None:
    """Build documentation for deployment.

    Version labels are retained for task compatibility but are not used by the
    GitHub Pages artifact deployment flow.
    """
    tmp_str = colorize(
        f"\nPreparing docs build for requested label {version}...\n",
        color=Color.HEADER,
        bold=True,
    )
    print(tmp_str)
    if alias != version:
        print(f"Ignoring docs alias {alias} under artifact deployment.\n")
    _command = "zensical build --clean"
    print(f">>> {colorize(_command, color=Color.OKBLUE)}\n")
    c_r.run(_command, pty=PTY)


@task
def set_default_version(c_r: Any, version: str) -> None:
    """Build documentation for deployment.

    Default-version selection is not used with the GitHub Pages artifact
    deployment flow.
    """
    tmp_str = colorize(
        f"\nPreparing docs build for requested default label {version}...\n",
        color=Color.HEADER,
        bold=True,
    )
    print(tmp_str)
    _command = "zensical build --clean"
    print(f">>> {colorize(_command, color=Color.OKBLUE)}\n")
    c_r.run(_command, pty=PTY)
