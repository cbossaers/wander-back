import requests

# tests/test_user.py
from ..classes.class_user import User

def test_user_name():
    user = User("Cristian", "cristian@upv.com", "Password-123")
    assert user.name == "Cristian"

    # Test setting name to an empty value
    try:
        user.name = ""
    except ValueError as e:
        assert str(e) == "Name not provided."
    else:
        assert False, "Expected ValueError for empty name."

def test_user_email():
    user = User("Cristian", "cristian@upv.com", "Password-123")
    assert user.email == "cristian@upv.com"

    # Test setting email to an empty value
    try:
        user.email = ""
    except ValueError as e:
        assert str(e) == "Email not provided."
    else:
        assert False, "Expected ValueError for empty email."

    # Test setting email to an invalid format
    try:
        user.email = "invalid_email"
    except ValueError as e:
        assert str(e) == "Email is invalid."
    else:
        assert False, "Expected ValueError for invalid email format."

def test_user_password():
    user = User("Cristian", "cristian@upv.com", "Password-123")
    assert user.password == "Password-123"

    # Test setting password to an empty value
    try:
        user.password = ""
    except ValueError as e:
        assert str(e) == "Password not provided."
    else:
        assert False, "Expected ValueError for empty password."

    # Test setting password to an invalid format
    try:
        user.password = "Password"
    except ValueError as e:
        assert str(e) == "100"
    else:
        assert False, "Expected ValueError for invalid password format."

URL = "88.17.116.148:7436"

def test_get_user():
    # Prepare test data
    headers = {
        'user': 'manolo@gmail.com'
    }

    # Send request to the API endpoint
    response = requests.get('http://' + URL + '/user/getuser', headers=headers)

    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "manolo@gmail.com"
    assert data["name"] == "Manolo"
    assert data["picture"] == None

def test_get_user_invalid():
    # Prepare test data
    headers = {
        'user': 'fake@upv.com'
    }

    # Send request to the API endpoint
    response = requests.get('http://' + URL + '/user/getuser', headers=headers)

    # Verify the response
    assert response.status_code == 400
    data = response.json()
    assert 'code' in data
    assert 'title' in data
    assert data['code'] == 115
    assert data['title'] == 'User not found'
