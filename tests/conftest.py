import pytest

from app.models.user import UserCreate
from app.db.schema import User
from app.services.user_service import UserService
from tests.test_db import TestingSessionLocal

@pytest.fixture(scope="module")
def default_user():
    session = TestingSessionLocal()
    service = UserService(session=session)
    user = service.create_user(UserCreate(name="Default User", email="default@user.com"))
    yield user