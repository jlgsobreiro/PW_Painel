from cryptography.fernet import Fernet


def write_key():
    key = Fernet.generate_key()  # Generates the key
    with open("key.key", "wb") as key_file:  # Opens the file the key is to be written to
        key_file.write(key)  # Writes the key


write_key()
