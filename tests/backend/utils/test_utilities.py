import pytest
from src.backend.utils.utilities import hash_password, verify_password, generate_token, SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta
import jwt

def test_hash_password_and_verify_success():
    password = "mysecret"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True

def test_verify_password_fail():
    password = "mysecret"
    wrong_password = "notmysecret"
    hashed = hash_password(password)
    assert verify_password(wrong_password, hashed) is False

def test_generate_token_success():
    email = "user@example.com"
    token = generate_token(email)
    assert isinstance(token, str)
    # Decodifica e verifica payload
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == email
    assert "exp" in payload

def test_generate_token_expired():
    # Gera um token já expirado manualmente
    email = "user@example.com"
    expire = datetime.utcnow() - timedelta(hours=1)
    payload = {"sub": email, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def test_generate_token_invalid_signature():
    email = "user@example.com"
    token = generate_token(email)
    # Tenta decodificar com chave errada
    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(token, "wrong_secret", algorithms=[ALGORITHM])