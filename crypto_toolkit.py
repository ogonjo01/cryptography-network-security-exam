

import sys
import os
import hashlib
from cryptography.fernet import Fernet, InvalidToken


def generate_key(key_path: str) -> None:

    key = Fernet.generate_key()
    with open(key_path, "wb") as f:
        f.write(key)
    print(f"Key generated and saved to {key_path}")


def load_key(key_path: str) -> bytes:
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Key file not found: {key_path}")
    with open(key_path, "rb") as f:
        return f.read()


def encrypt_file(input_path: str, output_path: str, key_path: str) -> None:
    key = load_key(key_path)
    fernet = Fernet(key)

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    with open(output_path, "wb") as f:
        f.write(encrypted)

    print(f"Encrypted '{input_path}' -> '{output_path}'")


def decrypt_file(input_path: str, output_path: str, key_path: str) -> None:
    key = load_key(key_path)
    fernet = Fernet(key)

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Encrypted file not found: {input_path}")

    with open(input_path, "rb") as f:
        encrypted = f.read()

    try:
        decrypted = fernet.decrypt(encrypted)
    except InvalidToken:
        raise ValueError("Decryption failed: wrong key or corrupted/tampered file")

    with open(output_path, "wb") as f:
        f.write(decrypted)

    print(f"Decrypted '{input_path}' -> '{output_path}'")


def compute_sha256(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def save_hash(file_path: str, hash_output_path: str) -> None:
    digest = compute_sha256(file_path)
    with open(hash_output_path, "w") as f:
        f.write(digest)
    print(f"SHA-256 of '{file_path}': {digest}")
    print(f"Saved to '{hash_output_path}'")


def verify_integrity(file_path: str, hash_file_path: str) -> bool:
    if not os.path.exists(hash_file_path):
        raise FileNotFoundError(f"Stored hash file not found: {hash_file_path}")

    with open(hash_file_path, "r") as f:
        stored_hash = f.read().strip()

    current_hash = compute_sha256(file_path)

    if current_hash == stored_hash:
        print("Integrity check PASSED: file has not changed.")
        return True
    else:
        print("Integrity check FAILED: file has been modified!")
        print(f"  stored hash : {stored_hash}")
        print(f"  current hash: {current_hash}")
        return False


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "generate-key":
            key_path = sys.argv[2] if len(sys.argv) > 2 else "secret.key"
            generate_key(key_path)

        elif command == "encrypt":
            _, _, input_file, output_file, key_file = sys.argv
            encrypt_file(input_file, output_file, key_file)

        elif command == "decrypt":
            _, _, input_file, output_file, key_file = sys.argv
            decrypt_file(input_file, output_file, key_file)

        elif command == "hash":
            _, _, target_file = sys.argv
            
            save_hash(target_file, target_file + ".sha256")

        elif command == "verify":
            _, _, target_file, hash_file = sys.argv
            verify_integrity(target_file, hash_file)

        else:
            print(f"Unknown command: {command}")
            print(__doc__)
            sys.exit(1)

    except (FileNotFoundError, ValueError) as e:
        # Handles missing files / invalid input without crashing (task 2d)
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
