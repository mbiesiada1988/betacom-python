import pytest
import os


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True
    }


@pytest.fixture(scope="session", autouse=True)
def output():
    if not os.path.isdir('output'):
        os.makedirs('output')
