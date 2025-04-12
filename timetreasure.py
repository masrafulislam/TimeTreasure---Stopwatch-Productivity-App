import tkinter as tk
from tkinter import messagebox
import time
import json
import os
from datetime import datetime, date, timedelta
import threading
import matplotlib.pyplot as plt
from collections import defaultdict

class TimeTreasureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TimeTreasure - Stopwatch Productivity App")
        self.root.geometry("400x450")

        # Initialize variables
        self.is_running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.total_hours = 0.0
        self.vault = 0
        self.sessions = []  # List to store session details
        self.daily_coins_earned = 0  # Track coins earned for the day
        self.daily_coins_history = {}  # Track daily coin earnings history

        # Load saved data
        self.data_file = "work_timer_data.json"
        self.load_data()

        # GUI Elements
        self.label_timer = tk.Label(root, text="00:00:00", font=("Arial", 24))
        self.label_timer.pack(pady=10)

        self.label_hours = tk.Label(root, text=f"Total Hours: {self.total_hours:.2f}", font=("Arial", 14))
        self.label_hours.pack(pady=5)

        self.label_vault = tk.Label(root, text=f"Vault: {self.vault} coins", font=("Arial", 14))
        self.label_vault.pack(pady=5)

        self.label_daily_coins = tk.Label(root, text=f"Today's Coins: {self.daily_coins_earned}", font=("Arial", 14))
        self.label_daily_coins.pack(pady=5)

        self.button_start = tk.Button(root, text="Start", command=self.start_timer)
        self.button_start.pack(pady=5)

        self.button_stop = tk.Button(root, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.button_stop.pack(pady=5)

        self.button_reset = tk.Button(root, text="Reset Daily Hours", command=self.reset_daily_hours)
        self.button_reset.pack(pady=5)

        self.button_sessions = tk.Button(root, text="View Sessions", command=self.view_sessions)
        self.button_sessions.pack(pady=5)

        self.button_graph = tk.Button(root, text="View Hours Graph", command=self.show_hours_graph)
        self.button_graph.pack(pady=5)

        # Start background thread for daily reset (no coin calculation)
        self.running = True
        self.reset_thread = threading.Thread(target=self.check_daily_reset)
        self.reset_thread.daemon = True
        self.reset_thread.start()

        # Update timer display
        self.update_timer()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.total_hours = data.get('total_hours', 0.0)
                self.vault = data.get('vault', 0)
                self.sessions = data.get('sessions', [])
                self.daily_coins_earned = data.get('daily_coins_earned', 0)
                self.daily_coins_history = data.get('daily_coins_history', {})
        else:
            self.save_data()

    def save_data(self):
        data = {
            'total_hours': self.total_hours,
            'vault': self.vault,
            'sessions': self.sessions,
            'daily_coins_earned': self.daily_coins_earned,
            'daily_coins_history': self.daily_coins_history
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time() - self.elapsed_time
            self.button_start.config(state=tk.DISABLED)
            self.button_stop.config(state=tk.NORMAL)

    def stop_timer(self):
        if self.is_running:
            self.is_running = False
            self.elapsed_time = time.time() - self.start_time
            session_hours = self.elapsed_time / 3600  # Convert seconds to hours
            self.total_hours += session_hours
            session = {
                'start_time': self.start_time,
                'end_time': time.time(),
                'hours': session_hours
            }
            self.sessions.append(session)
            self.elapsed_time = 0

            # Award coins in real-time
            minutes_worked = session_hours * 60
            coins_earned = round(minutes_worked / 15)  # 1 coin per 15 minutes, rounded
            self.vault += coins_earned
            self.daily_coins_earned += coins_earned

            # Update daily coins history
            today_str = str(date.today())
            if today_str in self.daily_coins_history:
                self.daily_coins_history[today_str] += coins_earned
            else:
                self.daily_coins_history[today_str] = coins_earned

            self.label_hours.config(text=f"Total Hours: {self.total_hours:.2f}")
            self.label_vault.config(text=f"Vault: {self.vault} coins")
            self.label_daily_coins.config(text=f"Today's Coins: {self.daily_coins_earned}")
            self.button_start.config(state=tk.NORMAL)
            self.button_stop.config(state=tk.DISABLED)
            self.save_data()
            messagebox.showinfo("Session Saved", f"Work session saved locally!\nEarned {coins_earned} coins for this session.")

    def reset_daily_hours(self):
        if messagebox.askyesno("Confirm", "Reset daily hours to 0?"):
            self.total_hours = 0.0
            self.daily_coins_earned = 0
            self.sessions = [s for s in self.sessions if datetime.fromtimestamp(s['end_time']).date() != date.today()]
            self.label_hours.config(text=f"Total Hours: {self.total_hours:.2f}")
            self.label_daily_coins.config(text=f"Today's Coins: {self.daily_coins_earned}")
            self.save_data()

    def update_timer(self):
        if self.is_running:
            self.elapsed_time = time.time() - self.start_time
        hours, remainder = divmod(int(self.elapsed_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        self.label_timer.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.update_timer)

    def check_daily_reset(self):
        while self.running:
            current_date = str(date.today())
            current_time = datetime.now().time()
            # Check if it's a new day (after midnight)
            if self.sessions:  # Check if sessions list is not empty
                last_session_date = datetime.fromtimestamp(self.sessions[-1]['end_time']).date()
                if current_date != str(last_session_date) and current_time.hour >= 0:
                    self.total_hours = 0.0
                    self.daily_coins_earned = 0
                    self.sessions = [s for s in self.sessions if datetime.fromtimestamp(s['end_time']).date() != date.today()]
                    self.root.after(0, self.update_gui)
                    self.save_data()
            time.sleep(60)  # Check every minute

    def update_gui(self):
        self.label_hours.config(text=f"Total Hours: {self.total_hours:.2f}")
        self.label_vault.config(text=f"Vault: {self.vault} coins")
        self.label_daily_coins.config(text=f"Today's Coins: {self.daily_coins_earned}")

    def view_sessions(self):
        sessions_window = tk.Toplevel(self.root)
        sessions_window.title("Work Sessions")
        sessions_window.geometry("600x500")
        text = tk.Text(sessions_window, height=25, width=70)
        text.pack(pady=10)

        # Display daily coin earnings history
        text.insert(tk.END, "Daily Coin Earnings History (Last 7 Days):\n")
        text.insert(tk.END, "-" * 40 + "\n")
        for date_str, coins in sorted(self.daily_coins_history.items(), reverse=True)[:7]:  # Last 7 days
            text.insert(tk.END, f"{date_str}: {coins} coins\n")
        text.insert(tk.END, "\nRecent Sessions (Last 10):\n")
        text.insert(tk.END, "-" * 40 + "\n")

        # Display recent sessions
        for session in self.sessions[-10:]:  # Show last 10 sessions
            start_dt = datetime.fromtimestamp(session['start_time']).strftime('%Y-%m-%d %H:%M:%S')
            end_dt = datetime.fromtimestamp(session['end_time']).strftime('%Y-%m-%d %H:%M:%S')
            hours = session['hours']
            text.insert(tk.END, f"Start: {start_dt}, End: {end_dt}, Hours: {hours:.2f}\n")
        text.config(state=tk.DISABLED)

    def show_hours_graph(self):
        # Aggregate hours by day
        daily_hours = defaultdict(float)
        for session in self.sessions:
            session_date = datetime.fromtimestamp(session['end_time']).date()
            daily_hours[session_date] += session['hours']

        # Prepare data for the past 7 days
        today = date.today()
        dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]  # Last 7 days, including today
        hours = [daily_hours.get(d, 0) for d in dates]
        date_labels = [d.strftime('%Y-%m-%d') for d in dates]

        # Create bar chart
        plt.figure(figsize=(10, 5))
        plt.bar(date_labels, hours, color='skyblue')
        plt.xlabel('Date')
        plt.ylabel('Hours Worked')
        plt.title('Daily Hours Worked (Last 7 Days)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def on_closing(self):
        self.running = False
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTreasureApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()