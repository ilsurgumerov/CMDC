# Проверка размера и кодировки
import os

file_path = "Crime and Punishment ascii.txt"
file_size = os.path.getsize(file_path) / 1024 / 1024  # в мегабайтах

with open(file_path, 'rb') as f:
    content = f.read()
    is_ascii = all(b < 128 for b in content)
    line_endings = b'\r\n' in content or b'\n' in content


def validate_text(file_path):
    with open(file_path, 'rb') as f:
        for i, byte in enumerate(f.read()):
            if byte > 127:
                print(f"Non-ASCII char at position {i}: 0x{byte:02X}")
                return False
    return True


print(f"Size: {file_size:.2f} MB")
print(f"Pure ASCII: {is_ascii}")
print(f"Line endings: {'CRLF' if b'\r\n' in content else 'LF'}")
