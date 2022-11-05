from __future__ import annotations

import functools
import typing

import nox

SCRIPT_PATHS = ["src"]


def pip_session(
    *args: str, name: str | None = None
) -> typing.Callable[[typing.Callable[[nox.Session], None]], typing.Callable[[nox.Session], None]]:
    def inner(
        callback: typing.Callable[[nox.Session], None]
    ) -> typing.Callable[[nox.Session], None]:
        @nox.session(name=name)
        @functools.wraps(callback)
        def inner(session: nox.Session) -> None:
            for arg in args:
                session.install(arg)
            callback(session)

        return inner

    return inner


@pip_session("black", "codespell", "isort", name="apply-lint")
def format(session: nox.Session) -> None:
    session.run("black", *SCRIPT_PATHS)
    session.run("codespell", "-i", "2", *SCRIPT_PATHS)
    session.run("isort", *SCRIPT_PATHS)


@pip_session("black", "flake8", "codespell", "isort")
def lint(session: nox.Session) -> None:
    session.run("black", "--check", *SCRIPT_PATHS)
    session.run("flake8", *SCRIPT_PATHS)
    session.run("codespell", *SCRIPT_PATHS)
    session.run("isort", "--check", *SCRIPT_PATHS)


@pip_session(".")
def mypy(session: nox.Session) -> None:
    session.run("mypy", *SCRIPT_PATHS)
