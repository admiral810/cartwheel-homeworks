from pathlib import Path

import pytest
from fastapi import HTTPException

from server import app as server_app


@pytest.fixture
def server(
    world: dict,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(server_app, "SESSIONS_DB", tmp_path / "sessions.db")
    server_app._SESSIONS.clear()
    yield server_app
    server_app._SESSIONS.clear()


def test_session_rejects_claimed_role_mismatch(server) -> None:
    with pytest.raises(HTTPException) as error:
        server.create_session(server.SessionCreate(user_id=9002, role="shopper"))

    assert error.value.status_code == 403
    assert not server._SESSIONS


def test_token_cannot_authorize_another_session(server) -> None:
    first = server.create_session(
        server.SessionCreate(user_id=9002, role="merchant")
    )
    second = server.create_session(
        server.SessionCreate(user_id=9002, role="merchant")
    )
    assert first["session_id"] != second["session_id"]

    with pytest.raises(HTTPException) as error:
        server._authorize(
            second["session_id"], f"Bearer {first['token']}"
        )

    assert error.value.status_code == 403
