import ctypes, sys, os

try:
    opacity_value = int(sys.argv[2])
except ValueError:
    opacity_value = sys.argv[2]
    print(f"Invalid Agrument Passed: '{opacity_value}'.\nPlease Provide an Integer for Second Argument.\n"); exit(1)

user_input = sys.argv[1];user_input = user_input.replace('\\','/')
user_input = user_input.replace('"','');dll = ctypes.CDLL('.\\getTextureInfo.dll')
if '.3dst' not in user_input: print(f"Invalid File Format: '{os.path.splitext(user_input)[1]}' was provided.\n");exit(1)
if os.path.exists(user_input) == False: print(f"Invalid PATH Provided: '{user_input}', was provided.\n ");exit(1)

getFileFormat = dll.getFileFormat
getFileFormat.argtypes = [ctypes.c_char_p];getFileFormat.restype = ctypes.c_char_p
bFileFormat = getFileFormat(user_input.encode('utf-8'));dFileFormat = bFileFormat.decode('utf-8')
print(f"{dFileFormat}")

with open(user_input,'rb+') as f:
    if dFileFormat == 'ABGR':
        f.seek(0x20)
        while True:
            bytes_read = f.read(4)
            if len(bytes_read) < 4:  # Check if there are at least 4 bytes left
                break
            if bytes_read[0] > 0:
                first_byte = bytes_read[0];new_byte = opacity_value
                f.seek(-4, 1);f.write(bytes([new_byte]));f.seek(3, 1)
            else:
                first_byte = bytes_read[0];new_byte = 0
                f.seek(-4, 1);f.write(bytes([new_byte]));f.seek(3, 1)
        f.seek(0x08)
        f.write(b'\x01')
        print("Done\n")
    elif dFileFormat == 'RGBA8':
        f.seek(0x20)
        while True:
            bytes_read = f.read(4)
            if len(bytes_read) < 4:  # Check if there are at least 4 bytes left
                break
            if bytes_read[3] > 0:
                first_byte = bytes_read[3];new_byte = opacity_value
                f.seek(-1, 1);f.write(bytes([new_byte]));f.seek(1, 1)
            else:
                first_byte = bytes_read[3];new_byte = 0
                f.seek(-1, 1);f.write(bytes([new_byte]));f.seek(1, 1)
            f.seek(-1,1)
        f.seek(0x08)
        f.write(b'\x02')
        print("Done\n")
    else:
        print(f"{dFileFormat}, was returned by 'getTextureInfo.dll'.\n");exit(1)
