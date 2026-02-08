"""
Command-line interface for the CLI Todo application.
Supports both single command mode and interactive session mode.
Uses pure in-memory storage with no file I/O.
"""

import argparse
import cmd
import sys
from typing import List

from task import TaskManager, TaskNotFoundError, InvalidInputError


class TaskCLI(cmd.Cmd):
    """
    Interactive command-line interface for the task manager.
    Supports multiple commands in a single session.
    """

    intro = 'Welcome to the Task Manager CLI. Type help or ? for a list of commands.\n'
    prompt = '> '

    def __init__(self):
        """Initialize the CLI with a fresh task manager instance."""
        super().__init__()
        self.task_manager = TaskManager()

    def do_add(self, arg):
        """
        Add a new task: add <description>

        Example: add "Buy groceries"
        """
        if not arg:
            self._print_error("Error: Description is required")
            return

        try:
            task = self.task_manager.add_task(arg)
            print(f"Task added: {task}")
        except InvalidInputError as e:
            self._print_error(f"Error: {e}")

    def do_list(self, arg):
        """
        List all tasks: list

        Shows all tasks with their ID, completion status, and description.
        """
        tasks = self.task_manager.list_tasks()
        if not tasks:
            print("No tasks found.")
            return
        for task in tasks:
            print(task)

    def do_show(self, arg):
        """
        Show a single task by ID: show <task_id>

        Example: show 1
        """
        if not arg:
            self._print_error("Error: Task ID is required")
            return

        try:
            task_id = int(arg)
            task = self.task_manager.get_task(task_id)
            print(task)
        except ValueError:
            self._print_error("Error: Task ID must be an integer")
        except TaskNotFoundError as e:
            self._print_error(f"Error: {e}")
        except InvalidInputError as e:
            self._print_error(f"Error: {e}")

    def do_update(self, arg):
        """
        Update an existing task: update <task_id> [options]

        Options:
          --description <text>  Update task description
          --complete            Mark task as complete
          --incomplete          Mark task as incomplete

        Examples:
          update 1 --complete
          update 1 --description "New description"
          update 1 --complete --description "Completed task"
        """
        if not arg:
            self._print_error("Error: Please provide task ID and update parameters")
            return

        # Split the arguments properly
        parts = arg.split()
        if len(parts) < 1:
            self._print_error("Error: Task ID is required")
            return

        try:
            # The first part should be the task_id
            task_id_str = ""
            remaining_args = []

            # Find the first element that looks like a task ID (a number)
            for i, part in enumerate(parts):
                try:
                    int(part)
                    task_id_str = part
                    remaining_args = parts[i+1:]  # Everything after the ID
                    break
                except ValueError:
                    continue

            if not task_id_str:
                self._print_error("Error: Task ID must be an integer")
                return

            task_id = int(task_id_str)

            # Parse remaining arguments for --complete/--incomplete and description
            description = None
            completed = None
            i = 0
            desc_parts = []

            while i < len(remaining_args):
                arg = remaining_args[i]
                if arg == '--complete':
                    completed = True
                elif arg == '--incomplete':
                    completed = False
                else:
                    # This must be part of the description
                    desc_parts.append(arg)
                i += 1

            # Join description parts if any
            if desc_parts:
                description = ' '.join(desc_parts)

            # Check if at least one update parameter is provided
            if description is None and completed is None:
                self._print_error("Error: No update parameters provided. Use --description, --complete, or --incomplete")
                return

            task = self.task_manager.update_task(task_id, description, completed)
            print(f"Task updated: {task}")
        except ValueError:
            self._print_error("Error: Task ID must be an integer")
        except TaskNotFoundError as e:
            self._print_error(f"Error: {e}")
        except InvalidInputError as e:
            self._print_error(f"Error: {e}")

    def do_delete(self, arg):
        """
        Delete a task: delete <task_id>

        Example: delete 1
        """
        if not arg:
            self._print_error("Error: Task ID is required")
            return

        try:
            task_id = int(arg)
            self.task_manager.delete_task(task_id)
            print(f"Task {task_id} deleted.")
        except ValueError:
            self._print_error("Error: Task ID must be an integer")
        except TaskNotFoundError as e:
            self._print_error(f"Error: {e}")
        except InvalidInputError as e:
            self._print_error(f"Error: {e}")

    def _print_error(self, message):
        """
        Print error message in red using ANSI escape codes.

        Args:
            message: The error message to print
        """
        red_start = "\033[31m"
        color_reset = "\033[0m"
        print(f"{red_start}{message}{color_reset}", file=sys.stderr)

    def do_quit(self, arg):
        """
        Quit the application: quit

        Exits the interactive session.
        """
        print("Goodbye!")
        return True

    def do_exit(self, arg):
        """
        Exit the application: exit

        Exits the interactive session.
        """
        return self.do_quit(arg)

    def do_EOF(self, arg):
        """
        Handle EOF (Ctrl+D): EOF

        Exits the interactive session.
        """
        print()
        return self.do_quit(arg)

    def emptyline(self):
        """Override to do nothing on empty lines."""
        pass


def main():
    """Main entry point for the CLI application."""
    # If arguments provided, run in single-command mode
    if len(sys.argv) > 1:
        # Parse command-line arguments for single command execution
        parser = argparse.ArgumentParser(description="CLI Task Management Application")
        subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

        # Add command
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("description", type=str, help="Description of the task")

        # List command
        list_parser = subparsers.add_parser("list", help="List all tasks")

        # Show command
        show_parser = subparsers.add_parser("show", help="Show a single task by ID")
        show_parser.add_argument("task_id", type=int, help="ID of the task to show")

        # Update command
        update_parser = subparsers.add_parser("update", help="Update an existing task")
        update_parser.add_argument("task_id", type=int, help="ID of the task to update")
        update_parser.add_argument("--description", type=str, help="New description for the task")
        group = update_parser.add_mutually_exclusive_group()
        group.add_argument("--complete", action="store_true", help="Mark task as complete")
        group.add_argument("--incomplete", action="store_true", help="Mark task as incomplete")

        # Delete command
        delete_parser = subparsers.add_parser("delete", help="Delete a task")
        delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")

        args = parser.parse_args()

        # Create a single shared TaskManager instance for this session
        task_manager = TaskManager()

        # Handle the command
        if args.command == "add":
            try:
                task = task_manager.add_task(args.description)
                print(f"Task added: {task}")
            except InvalidInputError as e:
                red_start = "\033[31m"
                color_reset = "\033[0m"
                print(f"{red_start}Error: {e}{color_reset}", file=sys.stderr)
                sys.exit(1)
        elif args.command == "list":
            tasks = task_manager.list_tasks()
            if not tasks:
                print("No tasks found.")
                return
            for task in tasks:
                print(task)
        elif args.command == "show":
            try:
                task = task_manager.get_task(args.task_id)
                print(task)
            except TaskNotFoundError as e:
                red_start = "\033[31m"
                color_reset = "\033[0m"
                print(f"{red_start}Error: {e}{color_reset}", file=sys.stderr)
                sys.exit(1)
            except InvalidInputError as e:
                red_start = "\033[31m"
                color_reset = "\033[0m"
                print(f"{red_start}Error: {e}{color_reset}", file=sys.stderr)
                sys.exit(1)
        elif args.command == "update":
            try:
                description = args.description if hasattr(args, 'description') and args.description else None
                completed = None
                if hasattr(args, 'complete') and args.complete:
                    completed = True
                elif hasattr(args, 'incomplete') and args.incomplete:
                    completed = False

                if description is None and completed is None:
                    red_start = "\033[31m"
                    color_reset = "\033[0m"
                    print(f"{red_start}Error: No update parameters provided. Use --description, --complete, or --incomplete.{color_reset}", file=sys.stderr)
                    sys.exit(1)

                task = task_manager.update_task(args.task_id, description, completed)
                print(f"Task updated: {task}")
            except TaskNotFoundError as e:
                red_start = "\033[31m"
                color_reset = "\033[0m"
                print(f"{red_start}Error: {e}{color_reset}", file=sys.stderr)
                sys.exit(1)
            except InvalidInputError as e:
                red_start = "\033[31m"
                color_reset = "\033[0m"
                print(f"{red_start}Error: {e}{color_reset}", file=sys.stderr)
                sys.exit(1)
        elif args.command == "delete":
            try:
                task_manager.delete_task(args.task_id)
                print(f"Task {args.task_id} deleted.")
            except TaskNotFoundError as e:
                red_start = "\033[31m"
                color_reset = "\033[0m"
                print(f"{red_start}Error: {e}{color_reset}", file=sys.stderr)
                sys.exit(1)
            except InvalidInputError as e:
                red_start = "\033[31m"
                color_reset = "\033[0m"
                print(f"{red_start}Error: {e}{color_reset}", file=sys.stderr)
                sys.exit(1)
    else:
        # Run interactive mode
        TaskCLI().cmdloop()


if __name__ == "__main__":
    main()