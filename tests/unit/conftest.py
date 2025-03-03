import json
import os
from unittest.mock import patch

import pytest

user_data = """
{
    "id": null,
    "date_of_birth": "1972-05-02T00:00:00",
    "first_name": "John",
    "middle_name": null,
    "last_name": "Doe",
    "sex": "M"
}
"""


@pytest.fixture
def user_json():
    return user_data


@pytest.fixture
def user_dict():
    return json.loads(user_data)


@pytest.fixture(scope="session", autouse=True)
def region():
    return "us-east-2"


@pytest.fixture(scope="session", autouse=True)
def aws_credentials(region):
    """Mocked AWS Credentials for moto."""
    with patch.dict(
        os.environ,
        dict(
            AWS_ACCESS_KEY_ID="testing",
            AWS_SECRET_ACCESS_KEY="testing",
            AWS_SECURITY_TOKEN="testing",
            AWS_SESSION_TOKEN="testing",
            AWS_DEFAULT_REGION=region
        )
    ):
        yield


@pytest.fixture(scope="session", autouse=True)
def db_config(region):
    """Mocked pydantic-setting environment variables."""
    with patch.dict(
        os.environ,
        dict(
            SA_DRIVERNAME="sqlite+aiosqlite",
            SA_DATABASE="./test.db",
            SA_ECHO="True"
        )
    ):
        yield
