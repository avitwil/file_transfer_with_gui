

````markdown
# Bidirectional File Transfer with GUI

A desktop application for sending and receiving files between two peers over a network, using a clean and modern GUI built with `customtkinter`.

---

## Features

- Bidirectional file transfer using TCP sockets
- Clean and responsive GUI with CustomTkinter
- File receive with progress bar and confirmation popup
- Selectable destination folder for received files
- Configurable peer IP and port
- Basic input validation and error handling

---

## Requirements

- Python 3.8 – 3.11
- Required packages:
  - `customtkinter`
  - `tkinter` (built-in)
  - `socket`, `threading`, `os` (standard library)

Install dependencies:

```bash
pip install customtkinter
````

---

## Running the Application

### From Python source:

```bash
python file_transfer_with_gui.py
```

### Build to EXE (optional):

Using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --hidden-import=customtkinter file_transfer_with_gui.py
```

The compiled `.exe` will be located in the `dist/` directory.

---

## How to Use

1. Run the application on two machines (or two windows).
2. On one instance:

   * Choose a destination folder.
   * Set the server port and start the server.
3. On the second instance:

   * Enter the peer IP and port from the first machine.
   * Click "Send File to Peer" and select a file.
4. The file will be transferred to the destination folder of the first machine.

---

## Screenshot

*You may place a screenshot of the GUI here:*

```
assets/screenshot.png
```

To display it:

```markdown
![GUI Screenshot](assets/screenshot.png)
```

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contributing

Contributions are welcome. Feel free to submit pull requests or open issues for bug reports, suggestions, or improvements.

---

## Author

Created by [avitwil](https://github.com/avitwil) — 2025

```


