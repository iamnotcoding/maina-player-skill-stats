#ifndef SOCKET_UTIL_H
#define SOCKET_UTIL_H

#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>

int send_all(SOCKET socket, const char* data, int len, int flags);
int recv_all(SOCKET socket, const char* buffer, int len, int flags);

#endif