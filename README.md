# 🐍 Terminal Snake TUI

A modern, sleek, and responsive implementation of the classic Snake game right in your command line. Built using **Textual** for the terminal user interface (TUI) layout and game loop framework, and **Rich** for beautiful, vibrant text formatting and emoji rendering.

---

## 🎮 Demo

https://github.com/user-attachments/assets/aefcbdbb-4a9d-4680-a163-9b59642eff7a

---

## 🚀 Features

- **Steady, Balanced Gameplay:** Optimized frame rates provide a smooth, retro arcade feel.
- **Persistent High Scores:** Your highest scores are automatically saved to a local file and tracked across game restarts.
- **Pause & Resume:** Life got in the way? Freeze your game at any moment using the dedicated pause state.
- **Windows Terminal Ready:** Includes an optimized setup script designed specifically to circumvent Windows environment encoding quirks.

---

## 🕹️ Controls

| Key / Binding | Action |
|---|---|
| `W` / `Up Arrow` | Move Up |
| `A` / `Left Arrow` | Move Left |
| `S` / `Down Arrow` | Move Down |
| `D` / `Right Arrow` | Move Right |
| `P` | Pause / Unpause |
| `R` | Restart Game |
| `Q` | Quit Game |

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your machine. You will also need to install the project dependencies:

```bash
pip install textual rich

```
### 2. Running the Game
#### On Windows (Recommended)
Double-click the **run.bat** file. This script automatically handles directory mapping, activates UTF-8 rendering configurations, and launches the game in the modern **Windows Terminal** so the game's icons and colors display perfectly.
#### On Linux / macOS
Open your terminal emulator, navigate to the project folder, and run:
```bash
python game.py

```
## 📂 Project Structure
```text
├── config.py             # Global gameplay configurations (dimensions, tick intervals)
├── game.py               # Core application logic, event handlers, and UI rendering
├── run.bat               # Windows execution script optimized for Windows Terminal
├── .gitignore            # Excludes high scores and cache files from version control
└── README.md             # Project documentation

```
## 🎛️ Customization
Want to make the game harder or expand the grid? You don't have to sift through complex loops. Simply open config.py and tweak the baseline attributes:
```python
# config.py
GRID_WIDTH = 30                 # Adjust width dimensions
GRID_HEIGHT = 20                # Adjust height dimensions
STEADY_SPEED = 0.19             # Lower numbers = Faster gameplay

```
## 📄 License
This project is open-source and available under the MIT License.
