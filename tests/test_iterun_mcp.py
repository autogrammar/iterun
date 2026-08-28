from pathlib import Path

import pytest


def test_mcp_permissions_are_disabled_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    from iterun_mcp.server import _require_permission

    monkeypatch.delenv("ITERUN_MCP_ALLOW_MUTATION", raising=False)
    with pytest.raises(PermissionError, match="ITERUN_MCP_ALLOW_MUTATION"):
        _require_permission("ITERUN_MCP_ALLOW_MUTATION", "writes")


def test_mcp_permission_requires_explicit_truthy_value(monkeypatch: pytest.MonkeyPatch) -> None:
    from iterun_mcp.server import _require_permission

    monkeypatch.setenv("ITERUN_MCP_ALLOW_EXECUTE", "0")
    with pytest.raises(PermissionError, match="ITERUN_MCP_ALLOW_EXECUTE"):
        _require_permission("ITERUN_MCP_ALLOW_EXECUTE", "execution")
    monkeypatch.setenv("ITERUN_MCP_ALLOW_EXECUTE", "yes")
    _require_permission("ITERUN_MCP_ALLOW_EXECUTE", "execution")


def test_mcp_workspace_path_is_confined(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from iterun_mcp.server import _require_workspace_path

    allowed = tmp_path / "allowed"
    allowed.mkdir()
    monkeypatch.setenv("ITERUN_MCP_WORKSPACE_ROOT", str(allowed))
    _require_workspace_path(str(allowed / "generated"))
    with pytest.raises(PermissionError, match="ITERUN_MCP_WORKSPACE_ROOT"):
        _require_workspace_path(str(tmp_path / "outside"))
