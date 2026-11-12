"""Real systemd encryption with synthetic, non-authorizing token material."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/replicate_credential.py"
spec = importlib.util.spec_from_file_location("replicate_credential", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
CANARY = b"r8_" + b"synthetic_not_a_real_token_" * 2


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    path = tmp_path / "credentials/replicate.cred"
    monkeypatch.setattr(module, "credential_path", lambda: path)
    return path


def test_real_encryption_roundtrip_permissions_no_plaintext(isolated):
    result = module.store_token(CANARY)
    assert result["encrypted"] is True
    assert CANARY not in isolated.read_bytes()
    assert isolated.stat().st_mode & 0o777 == 0o600
    assert isolated.parent.stat().st_mode & 0o777 == 0o700
    assert module.load_token() == CANARY.decode()


def test_existing_token_is_not_overwritten(isolated):
    module.store_token(CANARY)
    original = isolated.read_bytes()
    with pytest.raises(FileExistsError):
        module.store_token(b"r8_" + b"different_synthetic_token" * 2)
    assert isolated.read_bytes() == original


def test_corruption_is_rejected_without_token_output(isolated):
    module.store_token(CANARY)
    isolated.write_bytes(b"corrupt encrypted credential")
    with pytest.raises(ValueError, match="CREDENTIAL_DECRYPT_FAILED"):
        module.load_token()


def test_unsafe_permissions_and_symlinks_are_rejected(isolated):
    module.store_token(CANARY)
    isolated.chmod(0o644)
    with pytest.raises(ValueError, match="UNSAFE_CREDENTIAL_FILE"):
        module.load_token()
    isolated.chmod(0o600)
    saved = isolated.with_suffix(".original")
    isolated.rename(saved)
    isolated.symlink_to(saved)
    with pytest.raises(OSError):
        module.load_token()


def test_noninteractive_set_refuses_secret_stdin(tmp_path):
    result = subprocess.run([sys.executable, str(SCRIPT), "set"], input=CANARY,
        capture_output=True, env={**os.environ, "HOME": str(tmp_path)})
    assert result.returncode == 2
    assert b"INTERACTIVE_HIDDEN_INPUT_REQUIRED" in result.stderr
    assert CANARY not in result.stdout + result.stderr
    assert not (tmp_path / ".local/share/graham-linkedin-credentials/replicate.cred").exists()


def test_token_format_is_checked_before_encryption(isolated):
    with pytest.raises(ValueError, match="INVALID_TOKEN_FORMAT"):
        module.store_token(b"not a token")
    assert not isolated.exists()


def test_render_passes_token_only_in_environment_to_existing_command(tmp_path, monkeypatch):
    path = tmp_path / ".local/share/graham-linkedin-credentials/replicate.cred"
    monkeypatch.setattr(module, "credential_path", lambda: path)
    module.store_token(CANARY)
    launcher = tmp_path / ".local/bin/linkedin-codex"
    launcher.parent.mkdir(parents=True)
    launcher.write_text("#!" + sys.executable + "\nimport os,sys,json\n"
        "assert os.environ['REPLICATE_API_TOKEN'].startswith('r8_')\n"
        "assert not any(os.environ['REPLICATE_API_TOKEN'] in x for x in sys.argv)\n"
        "print(json.dumps({'action':sys.argv[1], 'token_present':True}))\n")
    launcher.chmod(0o755)
    result = subprocess.run([sys.executable, str(SCRIPT), "render", "--id", "post"],
        env={**os.environ, "HOME": str(tmp_path)}, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert b'"action": "image-render"' in result.stdout
    assert b'"token_present": true' in result.stdout
    assert CANARY not in result.stdout + result.stderr
