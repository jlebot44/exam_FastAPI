from main import authentication


def test_authentication():
    """Authentification sur un user existant"""
    assert authentication("alice:wonderland")

    """Authentification sur un faux user"""
    assert not authentication("bad:bad")

    """Authentification avec un mauvais mot de passe"""
    assert not authentication("alice:bad")
