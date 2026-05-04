import pytest
from stealth_axiom.router import AxiomRouter
from stealth_axiom.recursive_link import RecursiveLink

@pytest.fixture
def router():
    return AxiomRouter()

@pytest.fixture
def link():
    return RecursiveLink()
