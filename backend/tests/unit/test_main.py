from lavi_worker.routers import main


def test_app_exists():
    """Test that app exists."""
    assert main.app is not None
