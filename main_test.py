from main import authentication

credentials = {
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine"
}

def test_authentication():
    """Authentification sur un user existant"""
    assert authentication("alice:wonderland") == True

    """Authentification sur un faux user"""
    assert authentication("bad:bad") == False

    """Authentification avec un mauvais mot de passe"""
    assert authentication("alice:bad") == False

