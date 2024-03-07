from flask import Flask, render_template
from flask_socketio import SocketIO, send
import subprocess
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)
app.config["SECRET"] = "ajuiahfa78fh9f78shfs768fgs7f6"
app.config["DEBUG"] = True
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("message")
def gerenciar_mensagens(mensagem):
    print(f"Mensagem: {mensagem}")
    send(mensagem, broadcast=True)

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Define the path to the file you're monitoring
        if event.src_path == "path_to_your_file":
            # Restart the Flask server in a new thread
            threading.Thread(target=restart_server).start()

def restart_server():
    # Restart the Flask server
    subprocess.Popen(["python", "your_flask_script.py"])

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    # Create a watchdog observer
    observer = Observer()
    # Define the directory you're monitoring
    path = "directory_to_monitor"
    observer.schedule(MyHandler(), path, recursive=True)
    observer.start()

    try:
        # Run the Flask app
        socketio.run(app, host='localhost')
    finally:
        # Stop the watchdog observer when the Flask app exits
        observer.stop()
        observer.join()
