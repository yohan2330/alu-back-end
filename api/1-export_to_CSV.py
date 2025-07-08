#!/usr/bin/python3
"""
This script retrieves an employee's TODO list progress from a REST API
and exports it to a CSV file.
"""

import csv
import requests
import sys


def export_employee_todo_to_csv(employee_id):
    """
    Fetches employee TODO list from JSONPlaceholder API and exports to CSV.

    Args:
        employee_id (int): The ID of the employee.
    """
    # API endpoints
    user_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}"
    todos_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}/todos"

    try:
        # Fetch user data
        user_response = requests.get(user_url)
        user_response.raise_for_status()
        user_data = user_response.json()

        # Fetch TODO list data
        todos_response = requests.get(todos_url)
        todos_response.raise_for_status()
        todos_data = todos_response.json()

        # Get employee name and ID
        employee_name = user_data.get('username', 'Unknown')
        user_id = user_data.get('id', employee_id)

        # Prepare CSV file
        csv_filename = f"{user_id}.csv"
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            for todo in todos_data:
                task_completed = todo.get('completed', False)
                task_title = todo.get('title', '')
                csv_writer.writerow([user_id, employee_name, task_completed, task_title])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching
