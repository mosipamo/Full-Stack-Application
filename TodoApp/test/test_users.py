from .utils import *
from ..routers.users import get_current_user, get_db
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "msinatest"
    assert response.json()["first_name"] == "Mohammad Sina"
    assert response.json()["last_name"] == "Parvizi"
    assert response.json()["email"] == "sina.sipamo@gmail.com"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "09383183372"
    

def test_change_password_success(test_user):
    response = client.put("/users/password", 
                        json={"password": "testpassword", "new_password": "passwordtest"})
    
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/users/password", 
                        json={"password": "wrongpassword", "new_password": "passwordtest"})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect password"}


def test_change_phone_number_success(test_user):
    response = client.put("/users/change_phone_number/+939383183372")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT