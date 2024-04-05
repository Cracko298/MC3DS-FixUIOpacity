#include <windows.h>
#include <string>

extern "C" __declspec(dllexport) const char* getFileFormat(const char* filename) {
    HANDLE hFile = CreateFileA(filename, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        return "File Not Found";
    }

    LARGE_INTEGER li;
    li.QuadPart = 0x20;
    SetFilePointerEx(hFile, li, NULL, FILE_BEGIN); // Skip the first 0x20 bytes

    char buffer[4];
    DWORD bytesRead;
    while (ReadFile(hFile, buffer, 4, &bytesRead, NULL) && bytesRead > 0) {
        if (buffer[0] == '\xFF') {
            CloseHandle(hFile);
            return "ABGR";
        } else if (buffer[3] == '\xFF') {
            CloseHandle(hFile);
            return "RGBA8";
        }

        li.QuadPart = 4;
        SetFilePointerEx(hFile, li, NULL, FILE_CURRENT); // Skip forward 4 bytes
    }

    CloseHandle(hFile);
    return "No Format Found";
}

extern "C" __declspec(dllexport) int getFileVersion(const char* filename) {
    HANDLE hFile = CreateFileA(filename, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        return -1; // File not found or unable to open
    }

    int fileVersion;
    LARGE_INTEGER li;
    DWORD bytesRead;

    // Read file version at 0x04
    li.QuadPart = 0x04;
    SetFilePointerEx(hFile, li, NULL, FILE_BEGIN);
    ReadFile(hFile, &fileVersion, sizeof(int), &bytesRead, NULL);

    CloseHandle(hFile);
    return fileVersion;
}

extern "C" __declspec(dllexport) std::tuple<int, int> getDemensions(const char* filename) {
    HANDLE hFile = CreateFileA(filename, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        return std::make_tuple(-1, -1); // File not found or unable to open
    }

    int width, height;
    LARGE_INTEGER li;
    DWORD bytesRead;

    // Read width at 0x0C
    li.QuadPart = 0x0C;
    SetFilePointerEx(hFile, li, NULL, FILE_BEGIN);
    ReadFile(hFile, &width, sizeof(int), &bytesRead, NULL);

    // Read height at 0x10
    li.QuadPart = 0x10;
    SetFilePointerEx(hFile, li, NULL, FILE_BEGIN);
    ReadFile(hFile, &height, sizeof(int), &bytesRead, NULL);

    CloseHandle(hFile);
    return std::make_tuple(width, height);
}

extern "C" __declspec(dllexport) int getMIPValue(const char* filename) {
    HANDLE hFile = CreateFileA(filename, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        return -1; // File not found or unable to open
    }

    int mipValue;
    LARGE_INTEGER li;
    DWORD bytesRead;

    // Read MIP value at 0x1C
    li.QuadPart = 0x1C;
    SetFilePointerEx(hFile, li, NULL, FILE_BEGIN);
    ReadFile(hFile, &mipValue, sizeof(int), &bytesRead, NULL);

    CloseHandle(hFile);
    return mipValue;
}
