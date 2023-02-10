import pytest
from lineReader import readFromFile
from pytest import raises
from unittest.mock import MagicMock

# no need to assert on calling method
# as done so below
# def test_canCallReadFromFile():
#     readFromFile("fileExample")

@pytest.fixture()
def mock_open( monkeypatch ):
    mock_file = MagicMock()
    mock_file.readline = MagicMock(return_value="test_line")
    mock_open = MagicMock(return_value=mock_file)
    monkeypatch.setattr("builtins.open", mock_open)
    return mock_open    
    
def test_returnsCorrectString(mock_open, monkeypatch):
    mock_exist = MagicMock(return_value=True)
    monkeypatch.setattr("os.path.exists", mock_exist)
    result = readFromFile("fileExample")
    mock_open.assert_called_once_with("fileExample", "r")
    assert result == "test_line"
    
def test_throwsExceptionWithBadFile(mock_open, monkeypatch):
    mock_exist = MagicMock(return_value=False)
    monkeypatch.setattr("os.path.exists", mock_exist)
    with raises(Exception):
        result = readFromFile("fileExample")
        