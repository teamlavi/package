from meta_db import server


def test_serve_exists():
    """Test that the top-level serve function exists."""
    assert hasattr(server, "serve")
