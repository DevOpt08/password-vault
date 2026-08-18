Password Vault (CLI)

A command-line password manager, written in Python. It stores credentials for different services behind a single master password, saves them to a local file, and only reveals a stored password once you've re-entered the master password.

This is the capstone project for Phase 0 of my journey into backend development, built with a security-first mindset. The goal wasn't just to make it work — it was to make deliberate, defensible security decisions at every step and understand why each one matters.

What it does
Creates a master password on first run and stores it hashed (never in plain text).
Locks the vault on open — you must enter the master password before you can see anything.
Lets you add, list, and reveal credentials from a simple menu.
Masks passwords when listing entries — the actual password is only shown through a deliberate, authenticated "reveal" action.
Saves everything to a local JSON file so your entries survive between sessions.
Handles bad input, missing files, and corrupted files without crashing.
Why I built it this way (a few key decisions)
The master password is hashed with bcrypt, not stored. I only ever need to check if you typed it correctly — I never need to read it back. So it's hashed one-way. If someone steals the file, they get a fingerprint, not the password. bcrypt also salts each hash automatically (defeating precomputed-hash attacks) and is deliberately slow (making brute-force expensive).
Stored credentials are not hashed. The whole point of a vault is to give your passwords back to you, so they can't be one-way hashed. (See "Known limitations" — these are currently plain text, and encryption is planned for a later phase.)
Revealing a password re-asks for the master password. Unlocking the vault gets you in the door, but viewing an actual secret asks again — so a walked-away-from, unlocked terminal doesn't hand everything over.
The vault checks who you are before telling you what's inside. You can't even find out whether a service exists in the vault without authenticating first. This prevents leaking information about which accounts are stored.
Project structure

The code is split across modules by responsibility, so each file has one clear job:

security.py — password hashing and verification (bcrypt).
storage.py — reading and writing the vault to a JSON file, with error handling.
auth.py — the decorator that gates sensitive actions behind the master password.
models.py — a PasswordEntry class (see note in Known limitations).
main.py — the "conductor": ties everything together, runs the menu, and handles the flow.
Getting started

You'll need Python 3 installed.

1. Clone the repository

git clone https://github.com/DevOpt08/password-vault.git
cd password-vault

2. Set up a virtual environment (keeps this project's dependencies isolated)

python -m venv venv

Activate it:

Windows (PowerShell): venv\Scripts\Activate.ps1
Mac/Linux: source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Run it

python main.py

On your first run, it'll ask you to set a master password. After that, every run asks you to unlock the vault before showing the menu.

How to use it

Once running, you'll see a menu:

1) Add — store a new service, username, and password.
2) List — see all your stored services and usernames (passwords stay hidden).
3) Reveal — show the actual password for one service (asks for the master password first).
4) Quit — exit.
Known limitations

I'm documenting these on purpose — knowing what a system doesn't do is as important as knowing what it does. Some of these are deliberate simplifications for this learning phase, with fixes planned for later.

Stored passwords are kept in plain text inside the JSON file. This is the biggest limitation. Proper encryption requires key management, which is a topic for a later phase — so for now, this is a conscious, documented simplification, not something I overlooked.
No file-access restrictions. Anyone who can read the vault file on the machine can read its contents. Locking this down is an operating-system-level concern beyond this project's current scope.
models.py is currently a learning artifact. I built the PasswordEntry class to practice object-oriented programming, but the final version stores entries as plain dictionaries for simpler JSON handling. Fully integrating the class (with object-to-JSON serialization) is a planned refactor.
Single-attempt unlock. Entering the wrong master password exits immediately, rather than allowing a few retries with a lockout. A capped retry loop would be a reasonable future improvement.
What I learned

This project pulled together the core Python I'd been building toward — classes, decorators, type hints, error handling, and modules — and applied all of it through a security lens. The biggest takeaways: hash what you only need to verify, never log or display secrets casually, fail loudly on corruption but gracefully on expected-empty cases, and authenticate before revealing anything at all.

It's a small program, but every decision in it was made on purpose.

Built as part of a structured, mentor-guided path toward backend development. Phase 0 of 6.