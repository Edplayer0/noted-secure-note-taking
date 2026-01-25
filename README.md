# NotEd - Secure and Encrypted Note-Taking Application

**NotEd** is a modern, user-friendly, and secure note-taking application designed to protect your privacy. With advanced encryption, intuitive design, and robust features, NotEd ensures your notes are safe, accessible, and easy to manage.

---

## ✨ Key Features

- **🔒 End-to-End Encryption**  
  Your notes are encrypted using state-of-the-art `Fernet` encryption, ensuring that only you can access your data.

- **🔑 Password Protection**  
  Secure your notes with password authentication. NotEd includes a built-in password manager for seamless access.

- **🖋️ Intuitive User Interface**  
  Built with `tkinter` and `customtkinter`, NotEd offers a clean, modern, and responsive design for an exceptional user experience.

- **📂 Data Backup and Restore**  
  Easily create backups of your notes and restore them when needed, ensuring your data is never lost.

- **📋 SQLite Database Integration**  
  Notes are stored in a lightweight and efficient SQLite database, providing fast and reliable data management.

- **🖥️ Cross-Platform Compatibility**  
  NotEd is designed to work seamlessly on Windows, macOS, and Linux. Package it as a standalone app for easy distribution.

---

## 🛠️ Technologies Used

- **Programming Language:** Python 3.10+
- **Libraries:**
  - `tkinter` and `customtkinter` for the graphical user interface.
  - `cryptography` for secure encryption and decryption.
  - `sqlite3` for database management.
- **Packaging:** `PyInstaller` for creating standalone executables.

---

## 📂 Project Structure

```plaintext
NotEd/
│
├── src/
│   ├── main.py               # Entry point of the application
│   ├── ui/                   # User interface components
│   ├── managers/             # Backend logic (database, encryption, password management)
│   ├── functions/            # Utility functions (backup, restore, etc.)
│   └── assets/               # Static files (icons, images, etc.)
│
├── pyproject.toml            # Project details and dependencies
├── poetry.lock               # Poetry dependencies lock file
├── README.md                 # Project documentation
├── LICENCE                   # MIT Licence
└── .gitignore                # Git ignore file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.14 or higher

### Running the Application
1. Clone the repository:
   ```bash
   git clone https://github.com/Edplayer0/noted-secure-note-taking.git
   cd NotEd
   ```

3. Install the dependencies
   ```bash
   pip install poetry
   poetry install --no-root
   ```

2. Run the application:
   ```bash
   python src/main.py
   ```

### Packaging as an Executable
To create a standalone executable:
```bash
pyinstaller --onedir --noconsole -i assets/icon.ico --add-data=.venv/Lib/site-packages/customtkinter;customtkinter/ --add-data=assets/bitmap.ico;. src/main.py
```

---

## 📦 Features in Development
- **Color themes:** Adjust the application to your favorite theme.

---

## 📜 Licence

This project is licensed under the **MIT Licence**. See the [LICENCE](LICENCE) file for details.

---

## 🤝 Contributing

We welcome contributions! If you'd like to improve NotEd, please fork the repository and submit a pull request.

---

## 📧 Contact

For inquiries, feedback, or support, please contact:  
**Edgar Ayuso Martínez**  
📧 [edgarayusodev@proton.me](mailto:edgarayusodev@proton.me)

---

**NotEd** - Your privacy, your notes, your ideas.
