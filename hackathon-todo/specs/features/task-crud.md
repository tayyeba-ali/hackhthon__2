# Task CRUD - Phase I Feature Specification

## Feature Title
CLI Task Management System - Basic CRUD Operations

## User Stories
- As a user, I want to add tasks so that I can keep track of things to do
- As a user, I want to list all tasks so that I can see what needs to be done
- As a user, I want to view a specific task so that I can see its details
- As a user, I want to update tasks so that I can modify descriptions or completion status
- As a user, I want to delete tasks so that I can remove completed or irrelevant items
- As a user, I want clear error messages when invalid operations are attempted

## Task Data Model
- **id** (integer): Unique identifier for each task (auto-incremented)
- **description** (string): Text description of the task
- **completed** (boolean): Completion status (default: false)

## CLI Commands

### Add Task
```
add <description>
```
- Creates a new task with the given description
- Auto-assigns the next available ID
- Sets completed status to false by default
- Exits with error if description is empty

### List Tasks
```
list
```
- Displays all tasks in the current session
- Shows ID, completion status, and description for each task
- Shows "No tasks found." if no tasks exist

### Show Task
```
show <task_id>
```
- Displays details of a specific task by ID
- Exits with error if task ID is invalid or not found

### Update Task
```
update <task_id> --description <new_description>
update <task_id> --complete
update <task_id> --incomplete
```
- Updates task description or completion status
- Supports updating description only, completion only, or both
- Exits with error if task ID is invalid or not found
- Exits with error if description is empty when updating description

### Delete Task
```
delete <task_id>
```
- Removes the task with the specified ID
- Exits with error if task ID is invalid or not found

## Rules
- Task IDs must be positive integers
- Task descriptions cannot be empty or contain only whitespace
- All state must be kept in memory only (no persistent storage)
- State resets completely on every program execution
- Invalid inputs must result in appropriate error messages
- Completion status can be toggled between complete/incomplete

## Acceptance Criteria
- [ ] Add command successfully creates tasks with unique auto-assigned IDs
- [ ] List command displays all tasks in the current session
- [ ] Show command displays details of a specific task by ID
- [ ] Update command modifies task description and/or completion status
- [ ] Delete command removes the specified task
- [ ] All commands provide appropriate error messages for invalid inputs
- [ ] No state persists between separate program executions
- [ ] All data is stored in memory only with no file I/O
- [ ] Task model includes ID, description, and completion status
- [ ] Error handling covers all edge cases (invalid IDs, empty descriptions, etc.)