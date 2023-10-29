import tkinter as tk
import requests
import time
import threading


class TypingTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.restart_button = None
        self.title("Typing Test")
        self.geometry("800x600")
        self.api_url = "https://baconipsum.com/api/?type=meat-and-filler&paras=1"
        self.current_paragraph = ""
        self.typing_entry = None
        self.paragraph_label = None
        self.timer_label = None
        self.start_timer_button = None
        self.typing_thread = None
        self.typing_timer_thread = None
        self.is_typing_allowed = False  # To track if typing is allowed
        self.is_timer_running = False  # To track if the timer is running
        self.last_typing_time = time.time()  # To track the last typing time

        self.create_widgets()
        self.new_paragraph()

    def create_widgets(self):
        self.paragraph_label = tk.Label(self, text="", font=("Helvetica", 14), wraplength=700, justify=tk.LEFT)
        self.paragraph_label.pack(pady=20)

        self.typing_entry = tk.Text(self, font=("Helvetica", 14), height=5, width=50, state="disabled")
        self.typing_entry.pack(pady=10)
        self.typing_entry.bind("<Key>", self.on_typing)

        self.start_timer_button = tk.Button(self, text="Start Timer (10 seconds)", command=self.start_timer)
        self.start_timer_button.pack(pady=10)

        self.timer_label = tk.Label(self, text="", font=("Helvetica", 16))
        self.timer_label.pack(pady=20)

        self.restart_button = tk.Button(self, text="Restart Test", command=self.new_paragraph)
        self.restart_button.pack(pady=10)
        self.restart_button.config(state="disabled")  # Initially disable the restart button

    def fetch_paragraph(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            data = response.json()
            self.current_paragraph = data[0]
            self.paragraph_label.config(text=self.current_paragraph)

    def new_paragraph(self):
        self.fetch_paragraph()
        self.typing_entry.delete(1.0, tk.END)
        self.is_typing_allowed = False
        self.timer_label.config(text="")
        self.is_timer_running = False
        self.restart_button.pack_forget()  # Hide the restart button
        self.restart_button.config(state="disabled")  # Disable the restart button when starting a new paragraph

    def start_timer(self):
        # clear the typing entry
        self.typing_entry.delete(1.0, tk.END)
        if not self.is_timer_running:
            self.is_timer_running = True
            self.start_timer_button.pack_forget()  # Hide the timer start button
            self.restart_button.config(state="disabled")  # Disable the restart button while the timer is running
            self.typing_timer_thread = threading.Thread(target=self.typing_timer_thread_func)
            self.typing_timer_thread.daemon = True
            self.typing_timer_thread.start()
            self.typing_entry.config(state="normal")  # Enable typing

    def typing_timer_thread_func(self):
        timer_start_time = time.time()

        for remaining_time in range(10, -1, -1):
            if self.is_typing_allowed:
                timer_start_time = time.time()  # Reset timer when typing
                self.is_typing_allowed = False

            self.timer_label.config(text=f"Time Remaining: {remaining_time} seconds")
            time.sleep(1)

            # Check if the timer should continue
            elapsed_time = time.time() - timer_start_time
            if elapsed_time >= 10:
                break

        self.timer_label.config(text="Time's up!")
        self.typing_entry.config(state="disabled")  # Disable typing
        # hide the timer start button and show the restart button
        self.restart_button.pack(pady=10)
        self.start_timer_button.pack_forget()
        self.start_timer_button.pack(pady=10)  # Show the timer start button
        self.restart_button.pack(pady=10)  # Show the restart button
        self.restart_button.config(state="normal")  # Enable the restart button

    def on_typing(self, event):

        self.is_typing_allowed = True
        if not self.is_timer_running:
            self.start_timer()

        self.last_typing_time = time.time()

        if time.time() - self.last_typing_time >= 10:
            self.is_typing_allowed = False  # User has stopped typing for 5 seconds, reset timer
            self.timer_label.config(text="")


if __name__ == "__main__":
    app = TypingTestApp()
    app.mainloop()
