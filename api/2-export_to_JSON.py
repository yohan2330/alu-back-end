#!/usr/bin/python3
"""
This module retrieves an employee's TODO list progress from a REST API
and exports it to a JSON file.
"""
import json
import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]))
        sys.exit(1)

    employee_id = sys.argv[1]
    
    # Fetch employee data
    user_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}"
    user_response = requests.get(user_url)
    
    if user_response.status_code != 200:
        print("User not found")
        sys.exit(1)
        
    user_data = user_response.json()
    username = user_data.get('username')
    
    # Fetch TODO list
    todos_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}/todos"
    todos_response = requests.get(todos_url)
    todos = todos_response.json()
    
    # Prepare data for JSON
    tasks = [
        {
            "task": task.get('title'),
            "completed": task.get('completed'),
            "username": username
        }
        for task in todos
    ]
    
    # Create JSON structure
    json_data = {employee_id: tasks}
    
    # Write to JSON file
    filename = f"{employee_id}.json"
    with open(filename, 'w') as f:
        json.dump(json_data, f)
