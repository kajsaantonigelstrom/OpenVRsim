#include <chrono>
#include <thread>
#include <string> 
#include "zeromqthread.hpp"
#pragma comment(lib, "libzmq-v142-mt-sgd-4_3_3.lib") // debug
//#pragma comment(lib, "libzmq-v142-mt-s-4_3_3.lib") // release
ZeroMQthread::ZeroMQthread(int port)
{
	tcpipstring = "tcp://*:" + std::to_string(port); // "tcp://*:port"
}

std::future<bool> ZeroMQthread::start(bool wait_for_completion, void* callbackobj_, void(*cmdcallback_)(void*, char*))
{
	// start the thread and the infinite message handling loop
	callbackobj = callbackobj_;
	cmdcallback = cmdcallback_;
	if (completion)
		delete completion;
	if (_internal_thread.joinable())
		_internal_thread.join();
	completion = new std::promise<bool>();
	std::future<bool> completion_result = completion->get_future();
	_internal_thread = std::thread([&] {
		completion->set_value(true);
		connect();
		_thread_running = true;
		while (_thread_running) {
			if (!connected)
				connect();
			if (connected)
				handlemessage();
			else 
				std::this_thread::sleep_for(std::chrono::milliseconds(1000));
		}
		});

	if (wait_for_completion) {
		completion_result.wait();
	}
	return completion_result;

}

void ZeroMQthread::connect()
{
	context = zmq_ctx_new();
	responder = zmq_socket(context, ZMQ_REP);
	int rc = zmq_bind(responder, tcpipstring.c_str());
	connected = rc == 0;

}
void ZeroMQthread::handlemessage()
{
	// Wait for a message
	char buffer[200];
	int sz = zmq_recv(responder, buffer, sizeof(buffer), 0);
    if (sz == -1) {
		_thread_running = false;
		zmq_close(responder);
		return;
    }
	// Perform the action
    buffer[sz] = 0;
	cmdcallback(callbackobj, buffer);

	// Send answer
	zmq_send(responder, buffer, strlen(buffer), 0);

}

void ZeroMQthread::stop()
{
	zmq_term(context);
}