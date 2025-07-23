import os
import socket
import threading
import customtkinter as ctk
from tkinter import filedialog

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"


class InfoPopup(ctk.CTkToplevel):
    """
    Popup window to display informational messages.
    """

    def __init__(self, parent, message):
        """
        Initialize the popup window.

        Args:
            parent: The parent tkinter window.
            message: The message string to display.
        """
        super().__init__(parent)
        self.title("Info")
        self.geometry("400x150")
        self.resizable(False, False)
        self.grab_set()

        label = ctk.CTkLabel(self, text=message, wraplength=380)
        label.pack(pady=20, padx=10)

        btn_ok = ctk.CTkButton(self, text="OK", command=self.destroy)
        btn_ok.pack(pady=10)


class FileTransferApp(ctk.CTk):
    """
    Main application class for bidirectional file transfer using a GUI.
    """

    def __init__(self):
        """
        Initialize the GUI application and its components.
        """
        super().__init__()

        self.title("Bidirectional File Transfer")
        self.geometry("700x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.dest_folder = None
        self.server_socket = None
        self.is_running = False

        self.server_port = None
        self.peer_host = "127.0.0.1"
        self.peer_port = 5001

        self.create_widgets()

    def create_widgets(self):
        """
        Create and place all GUI widgets in the main window.
        """
        self.btn_choose_folder = ctk.CTkButton(self, text="Choose Destination Folder", command=self.choose_folder)
        self.btn_choose_folder.pack(pady=10)

        server_frame = ctk.CTkFrame(self)
        server_frame.pack(padx=10, pady=10, fill="x")

        lbl_server_port = ctk.CTkLabel(server_frame, text="Server Port:")
        lbl_server_port.grid(row=0, column=0, sticky="w", padx=(10, 5), pady=5)
        self.entry_server_port = ctk.CTkEntry(server_frame)
        self.entry_server_port.grid(row=0, column=1, sticky="ew", pady=5)
        self.entry_server_port.insert(0, "5001")

        self.btn_start_server = ctk.CTkButton(server_frame, text="Start Server", command=self.start_server)
        self.btn_start_server.grid(row=1, column=0, columnspan=2, pady=10)

        server_frame.grid_columnconfigure(1, weight=1)

        peer_frame = ctk.CTkFrame(self)
        peer_frame.pack(padx=10, pady=10, fill="x")

        lbl_peer_ip = ctk.CTkLabel(peer_frame, text="Peer IP:")
        lbl_peer_ip.grid(row=0, column=0, sticky="w", padx=(10, 5), pady=5)
        self.entry_peer_ip = ctk.CTkEntry(peer_frame)
        self.entry_peer_ip.grid(row=0, column=1, sticky="ew", pady=5)
        self.entry_peer_ip.insert(0, self.peer_host)

        lbl_peer_port = ctk.CTkLabel(peer_frame, text="Peer Port:")
        lbl_peer_port.grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)
        self.entry_peer_port = ctk.CTkEntry(peer_frame)
        self.entry_peer_port.grid(row=1, column=1, sticky="ew", pady=5)
        self.entry_peer_port.insert(0, str(self.peer_port))

        self.btn_set_peer = ctk.CTkButton(peer_frame, text="Set Peer", command=self.set_peer)
        self.btn_set_peer.grid(row=2, column=0, columnspan=2, pady=10)

        peer_frame.grid_columnconfigure(1, weight=1)

        self.progress = ctk.CTkProgressBar(self)
        self.progress.set(0)
        self.progress.pack(fill="x", padx=10, pady=(0, 10))

        self.text_log = ctk.CTkTextbox(self, height=15)
        self.text_log.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.btn_send_file = ctk.CTkButton(self, text="Send File to Peer", command=self.send_file)
        self.btn_send_file.pack(pady=10)

    def log(self, message):
        """
        Append a message to the text log widget.

        Args:
            message: String message to append.
        """
        self.text_log.insert("end", message + "\n")
        self.text_log.see("end")

    def choose_folder(self):
        """
        Open a folder selection dialog and set the destination folder.
        """
        folder = filedialog.askdirectory(title="Choose destination folder")
        if folder:
            self.dest_folder = folder
            self.log(f"Destination folder set to: {folder}")
        else:
            self.log("No folder selected.")

    def set_peer(self):
        """
        Read and validate the peer IP and port from input fields, and set them.
        """
        ip = self.entry_peer_ip.get().strip()
        port_str = self.entry_peer_port.get().strip()

        if not ip:
            self.log("Peer IP cannot be empty.")
            return

        try:
            port = int(port_str)
            if not (1 <= port <= 65535):
                raise ValueError
        except ValueError:
            self.log("Invalid peer port.")
            return

        self.peer_host = ip
        self.peer_port = port
        self.log(f"Peer set to {self.peer_host}:{self.peer_port}")

    def start_server(self):
        """
        Start the server socket to listen for incoming file transfer connections.
        """
        if self.is_running:
            self.log("Server is already running.")
            return

        try:
            port = int(self.entry_server_port.get().strip())
            if not (1 <= port <= 65535):
                raise ValueError
            self.server_port = port
        except ValueError:
            self.log("Invalid server port.")
            return

        self.log(f"Starting server on port {self.server_port}...")
        thread = threading.Thread(target=self.server_loop)
        thread.daemon = True
        thread.start()

    def server_loop(self):
        """
        Server main loop that accepts incoming connections and starts a new thread for each client.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.server_socket:
            try:
                self.server_socket.bind(("0.0.0.0", self.server_port))
                self.server_socket.listen(5)
                self.is_running = True
                self.log(f"Server listening on port {self.server_port}")

                while self.is_running:
                    self.server_socket.settimeout(1.0)
                    try:
                        client_socket, address = self.server_socket.accept()
                        client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                        client_thread.daemon = True
                        client_thread.start()
                    except socket.timeout:
                        continue
            except Exception as e:
                self.log(f"Server error: {e}")

    def handle_client(self, client_socket, address):
        """
        Handle a client connection to receive a file and save it.

        Args:
            client_socket: The socket object for the connected client.
            address: The address tuple of the client.
        """
        try:
            self.log(f"Connected with {address}")
            received = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            filename, filesize = received.split(SEPARATOR)
            filename = os.path.basename(filename)
            filesize = int(filesize)

            if not self.dest_folder:
                self.log("No destination folder set.")
                return

            save_path = os.path.join(self.dest_folder, filename)
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(save_path):
                save_path = os.path.join(self.dest_folder, f"{base}({counter}){ext}")
                counter += 1

            with open(save_path, "wb") as f:
                total_received = 0
                self.progress.set(0)
                while total_received < filesize:
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    total_received += len(bytes_read)
                    progress_value = total_received / filesize
                    self.progress.after(0, self.progress.set, progress_value)

            self.log(f"File saved to: {save_path}")
            self.progress.after(0, self.progress.set, 0)
            self.progress.after(0, lambda: InfoPopup(self, f"File received and saved:\n{filename}"))

        except Exception as e:
            self.log(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()

    def send_file(self):
        """
        Open a file dialog to select a file and send it to the configured peer.
        """
        file_path = filedialog.askopenfilename(title="Select file to send")
        if not file_path:
            return

        def send_thread():
            self.btn_send_file.configure(state="disabled")
            try:
                filesize = os.path.getsize(file_path)
                filename = os.path.basename(file_path)

                self.log(f"Connecting to peer {self.peer_host}:{self.peer_port}...")
                self.log("Sending file...")

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(5.0)
                    s.connect((self.peer_host, self.peer_port))
                    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

                    with open(file_path, "rb") as f:
                        while True:
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            s.sendall(bytes_read)

                self.log(f"File '{filename}' sent successfully.")
                self.progress.after(0, lambda: InfoPopup(self, f"File '{filename}' sent successfully."))

            except socket.timeout:
                self.log("Connection timed out. Peer is not responding.")
                self.progress.after(0, lambda: InfoPopup(self, "Connection timed out.\nPeer is not responding."))

            except Exception as e:
                self.log(f"Error sending file: {e}")
                self.progress.after(0, lambda: InfoPopup(self, f"Error sending file:\n{e}"))

            finally:
                self.btn_send_file.after(0, lambda: self.btn_send_file.configure(state="normal"))

        threading.Thread(target=send_thread, daemon=True).start()


if __name__ == "__main__":
    app = FileTransferApp()
    app.mainloop()
