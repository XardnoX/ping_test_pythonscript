import os
import re
import matplotlib.pyplot as plt
from tkinter import Tk, Canvas, Frame, BOTH
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

def read_ping_results(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Extract the ping times using regex
    ping_times = re.findall(r'time=(\d+\.?\d*)', content)
    ping_times = [float(time) for time in ping_times]
    
    if ping_times:
        min_time = min(ping_times)
        max_time = max(ping_times)
        avg_time = sum(ping_times) / len(ping_times)
    else:
        min_time = max_time = avg_time = None
    
    return ping_times, min_time, max_time, avg_time

def generate_timestamp():
    return datetime.now().strftime('%Y%m%d_%H%M%S')

class PingGraphApp(Frame):
    def __init__(self, parent, ping_times, min_time, max_time, avg_time):
        Frame.__init__(self, parent)
        self.parent = parent
        self.ping_times = ping_times
        self.min_time = min_time
        self.max_time = max_time
        self.avg_time = avg_time
        self.initUI()
    
    def initUI(self):
        self.parent.title("Ping Graph")
        self.pack(fill=BOTH, expand=1)
        self.plot_graph()
    
    def plot_graph(self):
        # Create the logs folder if it doesn't exist
        os.makedirs('logs', exist_ok=True)

        fig = plt.figure(figsize=(10, 5))
        plt.plot(self.ping_times, marker='o', linestyle='-', color='b')
        plt.title('Graf')
        
        # Set x-axis label with min, max, and avg ping times
        xlabel = f'Min: {self.min_time} ms, Max: {self.max_time} ms, Avg: {self.avg_time:.2f} ms'
        plt.xlabel(xlabel)
        plt.ylabel('odezva (ms)')
        plt.grid(True)

        # Save the graph to the logs folder with the timestamp
        timestamp = generate_timestamp()
        file_path = f'logs/ping_graph_{timestamp}.png'
        fig.savefig(file_path)
        print(f"Graph saved as {file_path}")

        # Display the graph in the Tkinter window
        canvas = Canvas(self)
        canvas.pack(fill=BOTH, expand=1)

        plot_widget = FigureCanvasTkAgg(fig, canvas)
        plot_widget.get_tk_widget().pack(fill=BOTH, expand=1)
        plot_widget.draw()

if __name__ == "__main__":
    ping_file = 'ping_result.txt'
    ping_times, min_time, max_time, avg_time = read_ping_results(ping_file)

    if ping_times:
        root = Tk()
        app = PingGraphApp(root, ping_times, min_time, max_time, avg_time)  # Pass statistics to the app
        root.geometry("800x600")
        root.mainloop()
    else:
        print("No ping times found in the file.")
