#pragma once
#include <chrono>
#include <string>
#include <vector>

struct Sample {
public:
	Sample() {}
	Sample(std::vector<double>& v) {
		t = v[0];
		for (int i = 0; i+1 < v.size() && i < 7; i++)
			values[i] = v[i+1];
	}
	double t;
	double values[2]{ 0,0 };
};

struct Direction{
public:
	double x;
	double y;
	double z;
};

class DirectionManager
{
public:
	DirectionManager();
	// Handle command from controlling program
	std::string HandleCommand(std::string command);
		
	// Set current time
	void SetTime(std::chrono::system_clock::time_point t);
	// Get current pose
	void GetDir(Direction& dir);
	// Interpolate in the samples vector
	void interpolate(double t);
private:

	std::string setdir(double x, double y, double z);
	double cz;
	
	// Direction
	Sample direction;

	// Test case running
	bool running = false;
	// start time
	std::chrono::system_clock::time_point testcase_starttime;
	// seconds relative start
	std::chrono::duration<double> time_now;

	std::vector<Sample> samples;
};

