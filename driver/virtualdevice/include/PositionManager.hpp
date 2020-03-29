#pragma once
#include <chrono>
#include <string>
#include <openvr_driver.h>

struct Sample {
public:
	Sample() {}
	Sample(std::vector<double>& v) {
		t = v[0];
		for (int i = 0; i+1 < v.size() && i < 7; i++)
			values[i] = v[i+1];
	}
	double t;
	double values[7]{ 0,0,0,1,0,0,0 };
};
struct Buttonstate {
public:
	Buttonstate() {}
	Buttonstate(double t_, int state_) {
		t = t_;
		state = state_;
	}
	double t;
	int state;
};

class PositionManager
{
public:
	PositionManager();
	// Handle command from controlling program
	std::string HandleCommand(std::string command);
		
	// Set current time
	void SetTime(std::chrono::system_clock::time_point t);
	// Get current pose
	void GetPose(vr::DriverPose_t& pose);
	// Get current key state
	int GetKeys();
	// Interpolate in the samples vector
	void interpolate(double t);
private:

	std::string setpos(double x, double y, double z);
	std::string setrot(double w, double i, double j, double k);

	// Position and rotation
	Sample rotpos;

	// Current state
	int keystate; 
	int buttonState = 0; // 1:system 2:grip 4:trigger, 8:app
	// Test case running
	bool running = false;
	// start time
	std::chrono::system_clock::time_point testcase_starttime;
	// seconds relative start
	std::chrono::duration<double> time_now;

	std::vector<Sample> samples;
	std::vector<Buttonstate> buttonstates;
};

