#ifndef SERVER_HPP
#define SERVER_HPP

#include <nlohmann/json.hpp>

using json = nlohmann::json;

// all strings are UTF-8 encoded

/*
request format

DATA_SIZE(a padded with leading spaces and not null-terminated string)
{ (a null terminated json string)
	command : "...",
	data : "..."
}
*/

/*
commands :
	- calc_map_stats
	- calc_user_stats
	- end_server
*/

/*
response format
DATA_SIZE
{
	description : "...",
	data : "..."
}
*/

/*
description :
	- calc_map_stats
	- calc_user_stats
	- server_ended
*/

#define SOCKET_BUFFER 10000
#define DEFAULT_PORT "8123"
#define DEFAULT_BUFLEN 512

// size of the data size string(which is padded)
#define DATA_SIZE_SIZE 100

SOCKET get_client_socket();
json get_request(SOCKET socket);
SOCKET get_client_socket();
SOCKET get_listen_socket();
void process_request(SOCKET socket, json request);
void send_response(SOCKET socket, json response);

#endif
