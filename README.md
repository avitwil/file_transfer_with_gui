

````markdown
# Bidirectional File Transfer Application

This is a Python GUI application for bidirectional file transfer over a network. It allows users to run a server that listens for incoming file transfers, choose a destination folder to save received files, and send files to a specified peer.

## Features

- Choose a destination folder to save received files.
- Start a server on a specified port to listen for incoming connections.
- Set the IP address and port of a peer to send files to.
- Send files to the configured peer.
- Receive files from peers and save them without overwriting existing files (adds numbered suffix).
- Display transfer progress and logs in the GUI.
- Informational popups for successful transfers or errors.

## Requirements

- Python 3.7 or higher
- `customtkinter` library (for modern themed tkinter widgets)

## Installation

1. Clone this repository or download the source code.
2. Install the required dependencies:

```bash
pip install customtkinter
````

## Usage

Run the application:

```bash
python file_transfer_app.py
```

### How to use

1. Click **Choose Destination Folder** to select where incoming files will be saved.
2. Enter the **Server Port** and click **Start Server** to begin listening for incoming file transfers.
3. Enter the peer's IP address and port in the **Peer IP** and **Peer Port** fields and click **Set Peer**.
4. Click **Send File to Peer** to select and send a file to the configured peer.
5. Monitor logs and progress in the GUI window.

## Notes

* The application currently does not encrypt the file transfer data.
* It is intended for use on trusted local networks.
* If a received file already exists in the destination folder, the application appends a numbered suffix to the filename to avoid overwriting.
* The server runs in a background thread and handles multiple incoming connections concurrently.

## License

This project is provided as-is without any warranty. Use at your own risk.

---

Feel free to contribute improvements or open issues if you encounter bugs.

```

