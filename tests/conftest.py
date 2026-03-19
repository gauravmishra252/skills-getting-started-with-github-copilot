import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities as activities_store, app

# Keep an immutable baseline of the initial activities so each test runs in isolation.
BASE_ACTIVITIES = copy.deepcopy(activities_store)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities store before each test."""
    activities_store.clear()
    activities_store.update(copy.deepcopy(BASE_ACTIVITIES))
    yield


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)
