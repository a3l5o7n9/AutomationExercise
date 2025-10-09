import requests

from object_classes.user import User

def check_existence_of_user_via_api(user:User):
    # print("Entered 'check_existence_of_user_via_api()'")
    url = 'https://automationexercise.com/api/verifyLogin'
    form_data = {
        'email': f'{user.email}',
        'password': f'{user.password}'
    }

    try:
        response = requests.post(url, data=form_data)
        # print("Exiting 'check_existence_of_user_via_api()'")
        return '"responseCode": 200' in response.text
    except requests.exceptions.ConnectionError as e:
        print("Exception in 'check_existence_of_user_via_api()': Connection Error")
        print(e.msg)
        # print("Exiting 'check_existence_of_user_via_api()'")

def create_user_via_api(user:User):
    # print("Entered 'create_user_via_api()'")
    url = 'https://automationexercise.com/api/createAccount'
    form_data = {
        'name': f'{user.username}',
        'email': f'{user.email}',
        'password': f'{user.password}',
        'title': f'{user.title}',
        'birth_date': f'{user.dob_day}',
        'birth_month': f'{user.dob_month}',
        'birth_year': f'{user.dob_year}',
        'firstname': f'{user.first_name}',
        'lastname': f'{user.last_name}',
        'company': f'{user.company}',
        'address1': f'{user.address1}',
        'address2': f'{user.address2}',
        'country': f'{user.country}',
        'zipcode': f'{user.zipcode}',
        'state': f'{user.state}',
        'city': f'{user.city}',
        'mobile_number': f'{user.mobile_number}'
    }

    try:
        response = requests.post(url, data=form_data)
        # print("Exiting 'create_user_via_api()'")
        return '"responseCode": 201' in response.text
    except requests.exceptions.ConnectionError as e:
        print("Exception in 'create_user_via_api()': Connection Error")
        print(e.msg)
        # print("Exiting 'create_user_via_api()'")

def delete_user_via_api(user:User):
    # print("Entered 'delete_user_via_api()'")
    url = 'https://automationexercise.com/api/deleteAccount'
    form_data = {
        'email': f'{user.email}',
        'password': f'{user.password}'
    }

    try:
        response = requests.delete(url, data=form_data)
        # print("Exiting 'delete_user_via_api()'")
        return '"responseCode": 200' in response.text
    except requests.exceptions.ConnectionError as e:
        print("Exception in 'delete_user_via_api()': Connection Error")
        print(e.msg)
        # print("Exiting 'delete_user_via_api()'")
