import argparse
import os
import json
from datetime import datetime 
import sys 

TASKS_FILE='task.json'

def load_tasks():
    try:
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as f:
                content = f.read().strip()
                if content:  # Only load if file has content
                    return json.loads(content)
        return []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

    
def save_tasks(tasks):
    with open(TASKS_FILE,'w') as f:
        json.dump(tasks,f,indent=4) 
        
#Add Task
def add_task(description):
    tasks = load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    task = {
        'id': new_id,
        'description': description,
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")

#LIST TASK
def list_tasks(status_filter=None):
    tasks = load_tasks()
    if status_filter:
        tasks = [t for t in tasks if t['status'] == status_filter]
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(f"ID: {task['id']}, Desc: {task['description']}, Status: {task['status']}")


# UPDATE TASK
def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print("Task updated successfully.")
            return
    print(f"Task with ID {task_id} not found.", file=sys.stderr)

#Delete Task
def delete_task(task_id):
    tasks = load_tasks()
    original_len = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]
    if len(tasks) < original_len:
        save_tasks(tasks)
        print("Task deleted successfully.")
    else:
        print(f"Task with ID {task_id} not found.", file=sys.stderr)


#Mark Status
def mark_status(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}.")
            return
    print(f"Task with ID {task_id} not found.", file=sys.stderr)


#Main CLI Parser
def main():
    parser = argparse.ArgumentParser(description="Task CLI")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # add
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('description')

    # list
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('status', nargs='?')

    # update
    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('id', type=int)
    update_parser.add_argument('description')

    # delete
    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('id', type=int)

    # mark-in-progress
    ip_parser = subparsers.add_parser('mark-in-progress')
    ip_parser.add_argument('id', type=int)

    # mark-done
    done_parser = subparsers.add_parser('mark-done')
    done_parser.add_argument('id', type=int)

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.description)
    elif args.command == 'list':
        list_tasks(args.status)
    elif args.command == 'update':
        update_task(args.id, args.description)
    elif args.command == 'delete':
        delete_task(args.id)
    elif args.command == 'mark-in-progress':
        mark_status(args.id, 'in-progress')
    elif args.command == 'mark-done':
        mark_status(args.id, 'done')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
