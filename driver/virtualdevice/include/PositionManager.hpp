#pragma once
#include <chrono>
#include <string>
#include <openvr_driver.h>

class PositionManager
{
public:
	// Handle command from controlling program
	std::string HandleCommand(std::string command);
		
	// Set current time
	void SetTime(std::chrono::system_clock::time_point t);
	// Get current pose
	void GetPose(vr::DriverPose_t& pose);
	// Get current key state
	int GetKeys();

	// Position and rotation
	double px = 0;
	double py = 0;
	double pz = 0;
	double rw = 0;
	double ri = 0;
	double rj = 0;
	double rk = 0;
	// Current state
	int keystate; 
	int buttonState = 0; // 1:system 2:grip 4:trigger, 8:app

	// Current time
	std::chrono::system_clock::time_point time_now;
	std::chrono::system_clock::time_point testcase_starttime;
};

