// The execution chracterset of this file MUST be UTF-8
// c++ version 20 is required

#include <iostream>
#include <vector>

#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>

#include <nlohmann/json.hpp>
#include "server.hpp"
extern "C"
{
#include "socket_util.h"
}

using json = nlohmann::json;

using namespace std;

SOCKET ListenSocket = INVALID_SOCKET;

// generates a new socket and destorys it after the receving is done
json get_request(SOCKET socket)
{
	json json_data;
	int recvbuflen = DEFAULT_BUFLEN;
	char data_len_str[DATA_SIZE_SIZE + 1];
	char* raw_data;

	// recevie the size of the data 
	if (recv_all(socket, data_len_str, DATA_SIZE_SIZE, 0) == SOCKET_ERROR)
	{
		closesocket(socket);
		WSACleanup();
		throw format("recv failed: {}\n", WSAGetLastError());
	}

	int data_size = atoi(data_len_str);

	cout << "data size : " << data_size << endl;

	raw_data = new char[data_size];

	// recevie the data
	if (recv_all(socket, raw_data, data_size, 0) == SOCKET_ERROR)
	{
		closesocket(socket);
		WSACleanup();
		throw format("recv failed: {}\n", WSAGetLastError());
	}

	cout << "raw data : " << raw_data << endl;

	json_data = json::parse(raw_data);

	delete[] raw_data;

	return json_data;
}

SOCKET get_client_socket()
{
	SOCKET ClientSocket;

	ClientSocket = INVALID_SOCKET;

	// Accept a client socket
	ClientSocket = accept(ListenSocket, NULL, NULL);
	if (ClientSocket == INVALID_SOCKET) {
		closesocket(ListenSocket);
		WSACleanup();
		throw format("accept failed: {}\n", WSAGetLastError());
	}

	// No longer need server socket
	closesocket(ListenSocket);

	return ClientSocket;
}

SOCKET get_listen_socket()
{
	int iResult;
	WSADATA wsaData;

	// Initialize Winsock
	iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
	if (iResult != 0) {
		throw format("WSAStartup failed: {}\n", iResult);
	}

	struct addrinfo* result = NULL, * ptr = NULL, hints;

	ZeroMemory(&hints, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_protocol = IPPROTO_TCP;
	hints.ai_flags = AI_PASSIVE;

	// Resolve the local address and port to be used by the server
	iResult = ::getaddrinfo((PCSTR)NULL, DEFAULT_PORT, &hints, &result);

	if (iResult != 0) {
		WSACleanup();
		throw format("getaddrinfo failed: {}\n", iResult);
	}

	SOCKET ListenSocket = INVALID_SOCKET;

	// Create a SOCKET for the server to listen for client connections

	ListenSocket = socket(result->ai_family, result->ai_socktype, result->ai_protocol);

	if (ListenSocket == INVALID_SOCKET) {
		freeaddrinfo(result);
		WSACleanup();
		throw format("Error at socket(): {}\n", WSAGetLastError());
	}

	// Setup the TCP listening socket
	iResult = ::bind(ListenSocket, result->ai_addr, (int)result->ai_addrlen);
	if (iResult == SOCKET_ERROR) {
		freeaddrinfo(result);
		closesocket(ListenSocket);
		WSACleanup();
		throw format("bind failed: {}\n", WSAGetLastError());
	}

	freeaddrinfo(result);

	return ListenSocket;
}

void send_response(SOCKET socket, json response)
{
	int iResult;
	string response_str = response.dump();
	int data_size = response_str.length() + 1;

	// send the size of the data
	iResult = send_all(socket, format("{:{}}", response.dump().length(), DATA_SIZE_SIZE).c_str(), DATA_SIZE_SIZE, 0);

	if (iResult == SOCKET_ERROR) {
		closesocket(socket);
		WSACleanup();
		throw format("send failed: {}\n", WSAGetLastError());
	}

	iResult = send(socket, response.dump().c_str(), response.dump().length(), 0);

	if (iResult == SOCKET_ERROR) {
		closesocket(socket);
		WSACleanup();
		throw format("send failed: {}\n", WSAGetLastError());
	}
}

void process_request(SOCKET socket, json request)
{
	json response;
	cout << "command : " << request["command"] << endl;

	// process the request
	if (request["command"] == "calc_map_stats")
	{
		// process the map stats
	}
	else if (request["command"] == "calc_user_stats")
	{
		// process the user stats
	}
	else if (request["command"] == "end_server")
	{
		// end the server
		cout << "Ending server due to the end_server command" << endl;
		response["description"] = "server_ended";
		send_response(socket, response);
		closesocket(socket);
		exit(0);
	}
}

int main()
{
	ListenSocket = get_listen_socket();

	system("chcp 65001"); // set cmd encoding to UTF-8

	if (listen(ListenSocket, SOMAXCONN) == SOCKET_ERROR) {
		closesocket(ListenSocket);
		WSACleanup();
		throw format("listen failed: {}\n", WSAGetLastError());
	}

	SOCKET socket = get_client_socket();

	// The main loop
	while (true)
	{
		json request;

		try
		{
			request = get_request(socket);
		}
		catch (const std::exception& e)
		{
			cout << "Error: " << e.what() << endl;
			break;
		}

		try
		{
			process_request(socket, request);
		}
		catch (const std::exception& e)
		{
			cout << "Error: " << e.what() << endl;
			break;
		}
	}

	return 0;
}