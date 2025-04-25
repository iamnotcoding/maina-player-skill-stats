#include <stdbool.h>

#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>

int send_all(SOCKET socket, const char* data, int len, int flags) {
	int total_sent = 0;
	int bytes_left = len;
	int bytes_sent;

	while (total_sent < len) {
		bytes_sent = send(socket, data + total_sent, bytes_left, flags);
		if (bytes_sent == SOCKET_ERROR) {
			return SOCKET_ERROR;
		}

		total_sent += bytes_sent;
		bytes_left -= bytes_sent;
	}

	return total_sent;
}

int recv_all(SOCKET socket, const char* buffer, int len, int flags) {
	int total_recved = 0;
	int bytes_left = len;
	int bytes_recved;

	while (total_recved < len) {
		bytes_recved = recv(socket, buffer + total_recved, bytes_left, flags);
		if (bytes_recved == SOCKET_ERROR) {
			return SOCKET_ERROR;
		}

		total_recved += bytes_recved;
		bytes_left -= bytes_recved;
	}

	return total_recved;
}
