# CLI Task Management Application

A simple command-line interface task manager with full CRUD operations that maintains state in pure memory.

## Features

- Add, list, show, update, and delete tasks
- Track task completion status
- Pure in-memory storage (state resets on every program execution)
- Interactive session mode
- Colored output (green for completed tasks, yellow for incomplete, red for errors)
- Improved error messages

## Commands

### Single Command Mode
```bash
python src/main.py add "Task description"
python src/main.py list
python src/main.py show <task_id>
python src/main.py update <task_id> --description "New description"
python src/main.py update <task_id> --complete
python src/main.py update <task_id> --incomplete
python src/main.py delete <task_id>
```

### Interactive Session Mode
```bash
python src/main.py
> add "Task description"
> list
> update 1 --complete
> show 1
> exit
```

## Architecture

- `task.py`: Contains Task model and TaskManager with pure in-memory storage logic
- `cli.py`: Handles command-line parsing and user interaction with both single command and interactive modes
- No persistent storage - all state kept in memory only

## Constraints

- All state kept in pure memory (resets on every program execution)
- Clean, modular structure
- No external dependencies beyond Python standard library
- Colored output using ANSI escape codes (standard library only)