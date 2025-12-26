import pytest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from src.email_dfa import EmailDFAWithCounter, EmailDFAExpandedStates

VALID = [
    "satria123@gmail.com",
    "user.name_42@domain99.io",
    "A_B.c@D9.net",
]

INVALID = [
    "@gmail.com",           # username kosong
    "satria@.com",          # domain kosong sebelum dot
    "satria@gmail",         # extension tidak ada
    "satria@gmail.c",       # extension 1 huruf
    "sa tri@dom.com",       # spasi tidak diizinkan
    "user@domain..com",     # dot ganda (tidak terdeteksi penuh oleh aturan sederhana, tapi biasanya reject)
    "user@domain.com.",     # ada dot di akhir
]

@pytest.mark.parametrize("email", VALID)
def test_valid_counter(email):
    validator = EmailDFAWithCounter()
    assert validator.validate(email)

@pytest.mark.parametrize("email", INVALID)
def test_invalid_counter(email):
    validator = EmailDFAWithCounter()
    assert not validator.validate(email)

@pytest.mark.parametrize("email", VALID)
def test_valid_expanded(email):
    validator = EmailDFAExpandedStates()
    assert validator.validate(email)

@pytest.mark.parametrize("email", INVALID)
def test_invalid_expanded(email):
    validator = EmailDFAExpandedStates()
    assert not validator.validate(email) 