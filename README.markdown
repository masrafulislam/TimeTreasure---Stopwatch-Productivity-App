# TimeTreasure - Stopwatch Productivity App

## Overview
TimeTreasure is a Python-based desktop application designed to help users track their work time, boost productivity, and gamify their efforts with a coin-based reward system. Built using the `tkinter` library for the graphical user interface (GUI) and `matplotlib` for data visualization, TimeTreasure provides an intuitive way to log work sessions, view historical data, and visualize productivity trends over time.

The app allows users to:
- Start, stop, and reset a stopwatch to track work sessions.
- Earn coins based on time worked (1 coin per 15 minutes).
- View total hours worked, daily coin earnings, and a history of work sessions.
- Visualize daily hours worked over the past 7 days with a bar chart.
- Persist data locally in a JSON file for seamless tracking across sessions.

## Features
- **Stopwatch Functionality**: Start and stop a timer to track work sessions with real-time display of elapsed time.
- **Coin-Based Rewards**: Earn coins for every 15 minutes of work, stored in a virtual "vault."
- **Daily Coin Tracking**: Monitor coins earned daily and view a 7-day coin earnings history.
- **Session History**: Review details of recent work sessions, including start time, end time, and hours worked.
- **Data Visualization**: Generate a bar chart of daily hours worked over the past 7 days using `matplotlib`.
- **Persistent Storage**: Save work sessions, total hours, and coin data to a JSON file for continuity.
- **Daily Reset**: Automatically reset daily hours and coins at midnight to start fresh each day.

## Installation

### Prerequisites
- Python 3.6 or higher
- Required Python libraries:
  - `tkinter` (usually included with Python)
  - `matplotlib`
  - Standard libraries: `json`, `os`, `time`, `datetime`, `threading`, `collections`

### Setup
1. **Clone or Download the Project**:
   - Download the project files or clone the repository to your local machine.
2. **Install Dependencies**:
   - Ensure `matplotlib` is installed by running:
     ```bash
     pip install matplotlib
     ```
   - `tkinter` is included with standard Python installations. If not available, install it using your system's package manager (e.g., `python3-tk` on Ubuntu).
3. **Run the Application**:
   - Navigate to the project directory and run the script:
     ```bash
     python timetreasure.py
     ```

## Usage
1. **Launch the App**:
   - Run `timetreasure.py` to open the GUI window.
2. **Track Work Sessions**:
   - Click **Start** to begin a work session.
   - Click **Stop** to end the session and save the data. You'll earn coins based on the session duration.
   - The timer displays elapsed time in `HH:MM:SS` format.
3. **View Progress**:
   - **Total Hours**: Displays cumulative hours worked.
   - **Vault**: Shows total coins earned.
   - **Today's Coins**: Tracks coins earned on the current day.
4. **Manage Data**:
   - Click **Reset Daily Hours** to clear daily hours and coins (with confirmation).
   - Click **View Sessions** to see a detailed history of work sessions and daily coin earnings.
   - Click **View Hours Graph** to display a bar chart of hours worked over the past 7 days.
5. **Close the App**:
   - Close the window to save all data automatically to `work_timer_data.json`.

## File Structure
- `timetreasure.py`: Main application script containing the `TimeTreasureApp` class and GUI logic.
- `work_timer_data.json`: Auto-generated file to store total hours, vault coins, session details, and daily coin history.

## Technical Details
- **GUI Framework**: Built with `tkinter` for a simple, cross-platform interface.
- **Data Persistence**: Uses `json` to store data locally in `work_timer_data.json`.
- **Visualization**: Leverages `matplotlib` to generate a bar chart of daily hours worked.
- **Threading**: Uses a background thread to check for daily resets without blocking the GUI.
- **Time Tracking**: Converts elapsed time to hours for accurate session logging and coin calculation.

## Limitations
- The app is designed for single-user, local use and does not support multi-user or cloud-based storage.
- The daily reset occurs at midnight based on the system clock and requires the app to be running.
- The graph displays data for the last 7 days only, and session history shows the last 10 sessions.
- No network or file I/O beyond JSON storage is implemented.

## Future Improvements
- Add support for categorizing work sessions (e.g., by project or task).
- Implement customizable coin-earning rates or rewards for milestones.
- Enhance the GUI with themes or additional customization options.
- Add export functionality for session data (e.g., CSV or PDF reports).
- Support cloud-based storage for cross-device synchronization.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes. Ensure that your code follows PEP 8 guidelines and includes appropriate comments.

## Contact
For questions or feedback, please contact the project maintainer at [your-email@example.com].