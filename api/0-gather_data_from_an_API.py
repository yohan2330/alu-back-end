#!/usr/bin/python3
"""
This script retrieves and displays an employee's TODO list progress
from a REST API given an employee ID.
"""

import requests
import sys

def get_employee_todo_progress(employee_id):
    """
    Fetches and displays employee TODO list progress from JSONPlaceholder API.
    
    Args:
        employee_id (int): The ID of the employee
    """
    # API endpoints
    user_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}"
    todos_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}/todos"
    
    try:
        # Fetch user data
        user_response = requests.get(user_url)
        user_response.raise_for_status()  # Raise exception for bad status codes
        user_data = user_response.json()
        
        # Fetch TODO list data
        todos_response = requests.get(todos_url)
        todos_response.raise_for_status()
        todos_data = todos_response.json()
        
        # Get employee name
        employee_name = user_data.get('name', 'Unknown')
        
        # Calculate task statistics
        total_tasks = len(todos_data)
        completed_tasks = sum(1 for todo in todos_data if todo.get('completed', False))
        
        # Print the required output
        print(f"Employee {employee_name} is done with tasks({completed_tasks}/{total_tasks}):")
        for todo in todos_data:
            if todo.get('completed', False):
                print(f"\t {todo.get('title', '')}")
                
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error processing data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if employee ID is provided
    if len(sys.argv) != 2:
        print("Usage: python3 0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)
    
    try:
        employee_id = int(sys.argv[1])
        get_employee_todo_progress(employee_id)
    except ValueError:
        print("Employee ID must be an integer")
        sys.exit(1)
