"""
Task model and TaskManager for the CLI Todo application.
Uses pure in-memory storage with no file I/O.
Each program execution starts with a fresh state.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Task:
    """
    Represents a task with ID, description, and completion status.

    Attributes:
        id: Unique identifier for the task (auto-incremented)
        description: Text description of the task
        completed: Boolean indicating if the task is completed (default: False)
    """
    id: int
    description: str
    completed: bool = False

    def __str__(self):
        """
        Return string representation with colored output using ANSI codes.

        Returns:
            Formatted string with colored status indicator and task details
        """
        if self.completed:
            # Green checkmark for completed tasks
            status = "\033[32m✓\033[0m"  # Green
        else:
            # Yellow empty box for incomplete tasks
            status = "\033[33m \033[0m"  # Yellow
        return f"[{status}] {self.id}: {self.description}"


class TaskNotFoundError(Exception):
    """
    Raised when a task is not found by ID.

    Attributes:
        task_id: The ID of the task that wasn't found
    """
    def __init__(self, message, task_id=None):
        super().__init__(message)
        self.task_id = task_id


class InvalidInputError(Exception):
    """
    Raised when invalid input is provided to a task operation.
    """
    pass


class TaskManager:
    """
    Manages tasks in pure in-memory storage.
    State resets completely on every program execution.
    """

    def __init__(self):
        """Initialize with empty task list and starting ID counter."""
        self._tasks: List[Task] = []
        self._next_id = 1

    def add_task(self, description: str) -> Task:
        """
        Add a new task with the given description.

        Args:
            description: The task description

        Returns:
            The newly created Task object

        Raises:
            InvalidInputError: If description is empty or contains only whitespace
        """
        if not description or not description.strip():
            raise InvalidInputError("Task description cannot be empty.")
        new_task = Task(self._next_id, description.strip())
        self._tasks.append(new_task)
        self._next_id += 1
        return new_task

    def list_tasks(self) -> List[Task]:
        """
        Get a copy of all tasks.

        Returns:
            A list containing copies of all tasks
        """
        return list(self._tasks)  # Return a copy to prevent external modification

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task with the specified ID

        Raises:
            TaskNotFoundError: If no task with the given ID exists
            InvalidInputError: If task_id is not a positive integer
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise InvalidInputError("Task ID must be a positive integer.")
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(
            f"Task with ID {task_id} not found. Use 'list' to see valid IDs or 'add' to create a new task.",
            task_id=task_id
        )

    def update_task(self, task_id: int, description: str = None, completed: bool = None) -> Task:
        """
        Update a task's description or completion status.

        Args:
            task_id: The ID of the task to update
            description: New description (optional)
            completed: New completion status (optional)

        Returns:
            The updated task

        Raises:
            TaskNotFoundError: If no task with the given ID exists
            InvalidInputError: If description is empty or task_id is invalid
        """
        task = self.get_task(task_id)
        if description is not None:
            if not description or not description.strip():
                raise InvalidInputError("Task description cannot be empty.")
            task.description = description.strip()
        if completed is not None:
            task.completed = completed
        return task

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Raises:
            TaskNotFoundError: If no task with the given ID exists
            InvalidInputError: If task_id is not a positive integer
        """
        task = self.get_task(task_id)
        self._tasks.remove(task)