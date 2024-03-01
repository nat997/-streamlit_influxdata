import math
import pytest
from unittest.mock import patch, MagicMock
from DataMake import get_cpu_usage, get_ram_usage, get_battery_status

@pytest.fixture
def mock_subprocess_run():
    with patch('your_script_name.subprocess.run') as mock_run:
        yield mock_run

def test_get_cpu_usage(mock_subprocess_run):
    mock_subprocess_run.return_value.stdout = "CPU usage: 3.5% user"
    assert math.isclose(get_cpu_usage(), 3.5, rel_tol=1e-9)

def test_get_ram_usage(mock_subprocess_run):
    mock_subprocess_run.return_value.stdout = "Pages free: 2500."
    
    assert math.isclose(get_ram_usage(), 2.5, rel_tol=1e-9)

def test_get_battery_status(mock_subprocess_run):
    mock_subprocess_run.return_value.stdout = " -InternalBattery-0 (id=1234567)    75%; discharging; 5:02 remaining present: true"
    assert math.isclose(get_battery_status(), 2.5, rel_tol=1e-9)
