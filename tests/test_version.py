from src.django_stripe import __version__


def test_version():
    assert __version__ == "0.0.1"
