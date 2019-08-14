#include <thread>
#include <array>
#include <condition_variable>
#include <mutex>
#include <future>

#define ZMQ_STATIC
#include <zmq.h>

class ZeroMQthread
{
public:
	ZeroMQthread();
	std::future<bool> start(bool wait_for_completion);
private: // Methods
	void handlemessage();
	void connect();
private: // Members
	std::thread	_internal_thread;
	std::promise<bool> completion;

	bool _thread_running = false;
	void* context = nullptr;
	void* responder = nullptr;;
	bool connected = false;
};
