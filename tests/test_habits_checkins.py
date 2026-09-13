from datetime import datetime

# Testing of habit posting:
def test_posting_a_habit(client, auth_headers):

    habit = {
        "name":"Morning Runing",
        "description":"10km runing non-stop with no water and suppliments."
    }
    new_habit = client.post('/habits', json=habit, headers=auth_headers)
    assert new_habit.status_code == 201

    habit_data = new_habit.json()
    assert "id" in habit_data
    assert "user_id" in habit_data
    assert habit_data['name'] == habit['name']
    assert habit_data['description'] == habit['description']
    assert habit_data['current_streak'] == 0
    assert habit_data['longest_streak'] == 0
    assert isinstance(habit_data['created_at'], str)
    assert datetime.fromisoformat(habit_data['created_at']) # To check if its a datetime format

# Checking the list of habits:
def test_get_list_of_habits(client, auth_headers):

    # Creating test habits:
    habit_1 = {
        "name":"Morning Runing",
        "description":"10km runing non-stop with no water and suppliments."
    }

    habit_2 = {
        "name":"FootBall Practice",
        "description":"Football practice with no water and suppliments."
    }

    habit_3 = {
        "name":"BasketBall Practice",
        "description":"BasketBall practice with no water and suppliments."
    }

    client.post('/habits', json=habit_1, headers=auth_headers)
    client.post('/habits', json=habit_2, headers=auth_headers)
    client.post('/habits', json=habit_3, headers=auth_headers)

    all_habits = client.get(
        '/habits',
        headers=auth_headers
    )
    assert all_habits.status_code == 200
    assert len(all_habits.json()) == 3

    # Checking with each elements:
    # habit_1:
    assert all_habits.json()[0]['id'] == 1
    assert all_habits.json()[0]['name'] == habit_1['name']
    assert all_habits.json()[0]['description'] == habit_1['description']
    assert len(all_habits.json()[0]) == 7

    # habit_2:
    assert all_habits.json()[1]['id'] == 2
    assert all_habits.json()[1]['name'] == habit_2['name']
    assert all_habits.json()[1]['description'] == habit_2['description']
    assert len(all_habits.json()[1]) == 7

    # habit_3:
    assert all_habits.json()[2]['id'] == 3
    assert all_habits.json()[2]['name'] == habit_3['name']
    assert all_habits.json()[2]['description'] == habit_3['description']
    assert len(all_habits.json()[2]) == 7


def test_delete_habit(client, auth_headers):

    habit_1 = {
        "name":"Morning Runing",
        "description":"10km runing non-stop with no water and suppliments."
    }
    habit_response = client.post('/habits', json=habit_1, headers=auth_headers)
    assert habit_response.status_code == 201
    habit_id = habit_response.json()['id']

    habit_data = client.get('/habits', headers=auth_headers)
    assert habit_data.status_code == 200
    assert len(habit_data.json()) == 1

    # Deletion of the habit:
    delete_habit = client.delete(f'/habits/{habit_id}', headers=auth_headers)
    assert delete_habit.status_code == 200
    assert delete_habit.json()['detail'] == f"Habit with id:{habit_id} has been deleted from the database."
    assert len(client.get('/habits', headers=auth_headers).json()) == 0

def test_check_in(client, auth_headers):

    habit_1 = {
        "name":"Morning Runing",
        "description":"10km runing non-stop with no water and suppliments."
    }
    habit_response = client.post('/habits', json=habit_1, headers=auth_headers)
    assert habit_response.status_code == 201
    habit_id = habit_response.json()['id']
    
    habit_data = client.get('/habits', headers=auth_headers)
    assert habit_data.status_code == 200
    assert len(habit_data.json()) == 1

    # Checkin of the habit:
    checkin_habit = client.post(
        f'/habits/{habit_id}/checkin', headers=auth_headers
    )
    assert checkin_habit.status_code == 200
    full_data = checkin_habit.json()
    assert len(full_data) == 4

    # Final check:
    habit_check = client.get(
        '/habits', headers=auth_headers
    )
    assert habit_check.status_code == 200
    assert habit_check.json()[0]['current_streak'] == 1
    assert habit_check.json()[0]['longest_streak'] == 1
