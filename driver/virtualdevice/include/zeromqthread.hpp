#include <thread>
#include <array>
#include <condition_variable>
#include <mutex>
#include <future>

#define ZMQ_STATIC
#include <zmq.h>
class CSampleDeviceDriver;
class ZeroMQthread
{
public:
	ZeroMQthread();
	std::future<bool> start(bool wait_for_completion, void* callbackobj, void(*cmdcallback)(void*, char*));
	void stop();
private: // Methods
	void handlemessage();
	void connect();
private: // Members
	std::thread	_internal_thread;
	std::promise<bool> completion;

	void (*cmdcallback)(void*, char*);
	void* callbackobj;
	bool _thread_running = false;
	void* context = nullptr;
	void* responder = nullptr;;
	bool connected = false;
};
