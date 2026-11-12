#!/usr/bin/env python3
"""EN-local encrypted Replicate custody. Never prints or accepts a token in argv."""
import argparse
import getpass
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import warnings

NAME = "linkedin-replicate"
CREDS = "/usr/bin/systemd-creds"


def credential_path():
    return Path.home() / ".local/share/graham-linkedin-credentials/replicate.cred"


def crypt(action, raw):
    args = [CREDS, action, "--user", "--name=" + NAME]
    if action == "encrypt":
        args.append("--with-key=host")
    result = subprocess.run(args + ["-", "-"], input=raw, capture_output=True)
    if result.returncode:
        raise ValueError("CREDENTIAL_" + action.upper() + "_FAILED")
    return result.stdout


def valid_token(raw):
    try:
        value = raw.decode("ascii").strip()
    except UnicodeError:
        raise ValueError("INVALID_TOKEN_FORMAT") from None
    if not value.startswith("r8_") or len(value) < 20 or any(c.isspace() for c in value):
        raise ValueError("INVALID_TOKEN_FORMAT")
    return value


def store_token(raw):
    valid_token(raw)
    path = credential_path()
    parent = path.parent
    parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = parent.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid():
        raise ValueError("UNSAFE_CREDENTIAL_DIRECTORY")
    os.chmod(parent, 0o700)
    ciphertext = crypt("encrypt", raw)
    # Verify actual user/host decryption before persisting the credential.
    if crypt("decrypt", ciphertext) != raw:
        raise ValueError("CREDENTIAL_ROUNDTRIP_FAILED")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(ciphertext)
        stream.flush()
        os.fsync(stream.fileno())
    fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    return {"status": "configured", "encrypted": True, "path": str(path)}


def load_token():
    path = credential_path()
    parent = path.parent.lstat()
    if not stat.S_ISDIR(parent.st_mode) or parent.st_uid != os.getuid() or parent.st_mode & 0o077:
        raise ValueError("UNSAFE_CREDENTIAL_DIRECTORY")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise ValueError("UNSAFE_CREDENTIAL_FILE")
        raw = stream.read(65537)
    if len(raw) > 65536:
        raise ValueError("UNSAFE_CREDENTIAL_FILE")
    return valid_token(crypt("decrypt", raw))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["set", "status", "render"])
    parser.add_argument("render_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.action != "render" and args.render_args:
        parser.error("this action accepts no extra arguments")
    if args.action == "set":
        if not sys.stdin.isatty():
            raise ValueError("INTERACTIVE_HIDDEN_INPUT_REQUIRED")
        with warnings.catch_warnings():
            warnings.simplefilter("error", getpass.GetPassWarning)
            token = getpass.getpass("Replicate token (hidden): ").strip()
        print(json.dumps(store_token(token.encode())))
    elif args.action == "status":
        if not credential_path().exists():
            print(json.dumps({"status": "not_configured"}))
        else:
            load_token()
            print(json.dumps({"status": "configured", "encrypted": True, "decryption": "verified"}))
    else:
        # Existing app enforces exact input/spend approval and original-result recovery.
        env = dict(os.environ)
        env["REPLICATE_API_TOKEN"] = load_token()
        launcher = Path.home() / ".local/bin/linkedin-codex"
        os.execve(str(launcher), [str(launcher), "image-render", *args.render_args], env)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        allowed = str(exc) if isinstance(exc, ValueError) else "CREDENTIAL_OPERATION_FAILED"
        print(json.dumps({"status": "failed", "error_code": allowed}), file=sys.stderr)
        sys.exit(2)
