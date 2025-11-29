# NotEd - Encrypted Note-Taking App

NotEd is a secure note-taking application built with Python. It allows users to create, edit, and manage notes with advanced encryption to ensure data privacy.

---

## 🚀 Features
- **Encrypted Notes:** Notes are securely stored using `Fernet` encryption.
- **Password Protection:** Secure access with password management.
- **User-Friendly Interface:** Built with `tkinter` and `customtkinter`.
- **Data Persistence:** Notes are stored in an SQLite database.
- **Cross-Platform:** Easily portable and can be packaged as a standalone app.

---

## 🛠️ Technologies
- **Python 3.10+**
- **Libraries:**
  - `tkinter` and `customtkinter` for the GUI.
  - `cryptography` for encryption.
  - `sqlite3` for database management.

---

## 📂 Project Structure
```plaintext
NotEd/
│
├── src/
│   ├── app.py               # Main application file
│   ├── ui/                  # UI components
│   ├── managers/            # Backend logic (database, encryption, passwords)
│   └── functions/           # Utility functions
│
├── assets/                  # Static files (icons, images, etc.)
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
└── LICENCE                  # Project licence