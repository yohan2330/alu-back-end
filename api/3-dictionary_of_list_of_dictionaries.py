#!/usr/bin/python3
"""
This module retrieves TODO list progress for all employees from a REST API
and exports it to a JSON file.
"""
import json
import requests

if __name__ == "__main__":
    # Fetch all users
    users_url = "https://jsonplaceholder.typicode.com/users"
    users_response = requests.get(users_url)
    users = users_response.json()
    
    # Prepare data for JSON
    all_tasks = {}
    
    for user in users:
        user_id = str(user.get('id'))
        username = user.get('username')
        
        # Fetch TODO list for each user
        todos_url = f"https://jsonplaceholder.typicode.com/users/{user_id}/todos"
        todos_response = requests.get(todos_url)
        todos = todos_response.json()
        
        # Create task list for the user
        tasks = [
            {
                "username": username,
                "task": task.get('title'),
                "completed": task.get('completed')
            }
            for task in todos
        ]
        
        # Add to the dictionary
        all_tasks[user_id] = tasks
    
    # Write to JSON file
    filename = "todo_all_employees.json"
    with open(filename, 'w') as f:
        json.dump(all_tasks, f)
