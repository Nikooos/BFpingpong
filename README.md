# Office Ping Pong Ladder

A simple CLI-based ping pong ladder system for the office, built in Python.
Players can be added, matches recorded, and the ranking is calculated using the ELO rating system.

## Features

- Add players
- Record matches with scores
- View rankings (with ASCII-art Basic-Fit logo)
- Automatically pushes/pulls changes to GitHub after any update
- Minimal dependencies (Python standard library only)

## How to Use

1. Clone the repo:

   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. Run the script:

   ```bash
   python3 ladder.py
   ```

3. Choose an option from the menu:

   - Add player
   - Record match
   - View ranking
   - View rules
   - Quit

4. Rankings are saved and synced via Git.

## GitHub Integration

This script will automatically:

- `git pull` before changes
- `git add`, `commit`, and `push` after adding a player or match

Make sure you have Git installed and configured on your system.

## File Structure

- `ladder.py`: Main script
- `players.json`: Player data and ratings
- `matches.json`: Match history
- `logo.txt`: ASCII logo
- `.gitignore`: Files to be ignored by Git

## Requirements

- Python 3.x
- Git (installed and configured with SSH or cached credentials)

## License

MIT License
