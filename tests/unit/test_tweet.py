import os
import pytest

from cfnbot import tweet


@pytest.fixture
def mock_twitter(mocker):
    mocker.patch('tweet.api')



# TODO: add tweet unit test
