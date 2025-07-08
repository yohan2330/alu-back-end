#!/usr/bin/python3
"""
This script fetches an employee's TODO list from the JSONPlaceholder REST API
and exports it to a CSV file. The script takes an employee ID as a command-line
argument and creates a CSV file named '<employee_id>.csv' containing all tasks
owned by the employee. Each row in the CSV file follows the format:
"USER_ID","USERNAME","TASK_COMPLETED_STATUS","TASK_TITLE".
"""

import csv
import requests
import sys


def export_employee_todo_to_csv(employee_id):
    """
    Fetches employee TODO list from JSONPlaceholder API and exports to CSV.

    Args:
        employee_id (int): The ID of the employee whose TODO list is to be fetched.

    Raises:
        requests.exceptions.RequestException: If API request fails.
        ValueError: If JSON data cannot be parsed.
        IOError: If writing to the CSV file fails.
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

        # Get employee username and ID
        employee_username = user_data.get('username', 'Unknown')
        user_id = user_data.get('id', employee_id)

        # Prepare CSV file
        csv_filename = f"{user_id}.csv"
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            for todo in todos_data:
                task_completed = todo.get('completed', False)
                task_title = todo.get('title', '')
                csv_writer.writerow([user_id, employee_username, task_completed, task_title])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error processing data: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error writing to CSV file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Check if employee ID is provided
    if len(sys.argv) != 2:
        print("Usage: python3 1-export_to_CSV.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        export_employee_todo_to_csv(employee_id)
    except ValueError:
        print("Employee ID must be an integer")
        sys.exit(1)
