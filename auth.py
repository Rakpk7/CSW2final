import bcrypt
from pathlib import Path

# ---------- PATHS ----------

DATA_DIR = Path("data1")          # your folder name in the project
DATA_DIR.mkdir(exist_ok=True)     # make sure data1/ exists
USERS_FILE = DATA_DIR / "users.txt"


# ---------- PASSWORD HASHING ----------

def hash_password(plain_password: str) -> str:
    """Return bcrypt hash of a plain text password."""
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def check_password(plain_password: str, stored_hash: str) -> bool:
    """Check if plain password matches the stored bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        stored_hash.encode("utf-8")
    )


# ---------- USERS FILE HELPERS ----------

def load_users():
    """
    Load users from users.txt.
    Format per line: username,hashed_password,role
    """
    users = {}
    if USERS_FILE.exists():
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                username, pwd_hash, role = line.split(",")
                users[username] = (pwd_hash, role)
    return users


def save_user(username: str, pwd_hash: str, role: str):
    """Append a new user line into users.txt."""
    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username},{pwd_hash},{role}\n")


# ---------- REGISTER & LOGIN ----------

def register_user():
    print("\n=== Register User ===")
    users = load_users()

    username = input("Enter new username: ").strip()
    if username in users:
        print("❌ Username already exists.")
        return

    role = input("Enter role (e.g. analyst/data_scientist/it_admin): ").strip()

    password = input("Enter password: ")
    confirm = input("Confirm password: ")

    if password != confirm:
        print("❌ Passwords do not match.")
        return

    pwd_hash = hash_password(password)
    save_user(username, pwd_hash, role)
    print(f"✅ User '{username}' registered with role '{role}'.")


def login_user():
    print("\n=== Login ===")
    users = load_users()

    username = input("Enter username: ").strip()
    if username not in users:
        print("❌ User not found.")
        return

    stored_hash, role = users[username]
    password = input("Enter password: ")

    if check_password(password, stored_hash):
        print(f"✅ Login successful. Welcome {username}! (Role: {role})")
    else:
        print("❌ Incorrect password.")


# ---------- SIMPLE MENU ----------

def main():
    while True:
        print("\n==== AUTH MENU ====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose option (1-3): ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            print("Bye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()