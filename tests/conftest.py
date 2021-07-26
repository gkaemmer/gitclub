import subprocess
import signal
import socket
import pytest
from time import sleep
import requests
from functools import partial
import os


def PrefixUrlSession(prefix=None):
    """
    This is just like a normal requests.Session, but the given prefix is
    prepended to each request URL.
    """
    if prefix is None:
        prefix = ""
    else:
        prefix = prefix.rstrip("/") + "/"

    def new_request(prefix, f, method, url, *args, **kwargs):
        return f(method, prefix + url.lstrip("/"), *args, **kwargs)

    s = requests.Session()
    s.request = partial(new_request, prefix, s.request)
    return s


def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex(("127.0.0.1", port))
        return result == 0


def ensure_port_5000_is_open(process):
    sleep(0.5)
    total_time = 0
    while not is_port_open(5000):
        sleep(0.5)
        total_time += 0.5
        if total_time > 5:
            raise RuntimeError(
                "Server took more than 5s to start up. \n"
                + "--- BEGIN STDOUT ---\n"
                + process.stdout.read().decode("ascii")
                + "\n--- END STDOUT ---\n"
                + "\n--- BEGIN STDERR ---\n"
                + process.stderr.read().decode("ascii")
                + "\n--- END STDERR ---\n"
            )


DIRECTORIES = {
    "rails": "../backends/rails",
    "flask-sqlalchemy": "../backends/flask-sqlalchemy",
}


@pytest.fixture(scope="session")
def test_app():
    directory = DIRECTORIES[os.getenv("BACKEND", "flask-sqlalchemy")]
    process = subprocess.Popen(
        ["make", "test-server", "-C", directory], start_new_session=True
    )
    ensure_port_5000_is_open(process)
    yield process
    pgrp = os.getpgid(process.pid)
    os.killpg(pgrp, signal.SIGINT)
    process.wait()
    print("DONE")


@pytest.fixture
def test_client(test_app):
    with PrefixUrlSession("http://localhost:5000") as session:

        def log_in_as(email):
            session.post("/session", json={"email": email})

        session.log_in_as = log_in_as  # type: ignore
        session.post("/_reset")

        yield session