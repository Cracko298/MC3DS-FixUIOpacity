import ctypes, sys, os

user_input = sys.argv[1];user_input = user_input.replace('\\','/')
user_input = user_input.replace('"','');dll = ctypes.CDLL('.\\getTextureInfo.dll')
if '.3dst' not in user_input: print(f"Invalid File Format: '{os.path.splitext(user_input)[1]}' was provided.\n");exit(1)

getFileFormat = dll.getFileFormat
getFileFormat.argtypes = [ctypes.c_char_p];getFileFormat.restype = ctypes.c_char_p
bFileFormat = getFileFormat(user_input.encode('utf-8'));dFileFormat = bFileFormat.decode('utf-8')

with open(user_input,'rb+') as f:
    if dFileFormat == 'ABGR':
        f.seek(0x20)
        while True:
            bytes_read = f.read(4)
            if not bytes_read:
                break
            first_byte = bytes_read[0];new_byte = first_byte // 2
            f.seek(-4, 1);f.write(bytes([new_byte]));f.seek(3, 1)
        print("Done\n")
    elif dFileFormat == 'RGBA8':
        f.seek(0x20)
        while True:
            bytes_read = f.read(4)
            if not bytes_read:
                break
            first_byte = bytes_read[3];new_byte = first_byte // 2
            f.seek(-4, 1);f.write(bytes([new_byte]));f.seek(3, 1)
        print("Done\n")
    else:
        print(f"{dFileFormat}, was returned by 'getTextureInfo.dll'.\n")
        raise ValueError