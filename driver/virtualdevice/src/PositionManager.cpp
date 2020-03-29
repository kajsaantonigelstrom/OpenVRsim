#include "PositionManager.hpp"

// Helper
void base_splitstring(std::vector<std::string>& dest, const std::string& src, const std::string& sep)
{
    // Empty string must not generate anything in vector
    if (src.empty())
        return;

    size_t first = 0;
    size_t last = src.size();

    do {
        size_t next = src.find_first_of(sep, first);

        if (next == std::string::npos)    // Had it been a container it would have been 'last'
            next = last;        // So that last part gets added (after last separator)

        std::string part;
        if (next > first)
            part = src.substr(first, next - first);

        dest.push_back(part);

        first = next + 1;       // + 1 to remove the separator
    } while (first < last);
}

void parsedoubles(std::vector<double>& res, std::string& params)
{
    std::vector<std::string> strings;
    std::string sep = " ";
    base_splitstring(strings, params, sep);
    res.clear();
    for (auto s : strings) {
        double f = atof(s.c_str());
        res.push_back(f);
    }
}

PositionManager::PositionManager()
{
    testcase_starttime = std::chrono::system_clock::now();
}

void PositionManager::GetPose(vr::DriverPose_t& _pose)
{
    if (running) {
        // Interpolate
        interpolate(time_now.count());

    }
	_pose.vecPosition[0] = rotpos.values[0];
	_pose.vecPosition[1] = rotpos.values[1];
	_pose.vecPosition[2] = rotpos.values[2];

	_pose.qRotation.w = rotpos.values[3];
	_pose.qRotation.x = rotpos.values[4];
	_pose.qRotation.y = rotpos.values[5];
	_pose.qRotation.z = rotpos.values[6];
}

std::string PositionManager::setpos(double x, double y, double z)
{
    rotpos.values[0] = x;
    rotpos.values[1] = y;
    rotpos.values[2] = z;
    return "ok";
}

std::string PositionManager::setrot(double w, double i, double j, double k)
{
    rotpos.values[3] = w;
    rotpos.values[4] = i;
    rotpos.values[5] = j;
    rotpos.values[6] = k;
    return "ok";
}

std::string PositionManager::HandleCommand(std::string command)
{
    std::string result;
    switch (command[0]) {
    case 'P': {
        // Set Position
        if (!running) {
            std::vector<double> doubles;
            parsedoubles(doubles, command.substr(2));
            if (doubles.size() == 3)
                result = setpos(doubles[0], doubles[1], doubles[2]);
            else
                result = "Wrong position format";
        }
        else
            result = "NOP: when test is running";
        break;
    }
    case 'R': {
        // Set Rotation
        if (!running) {
            std::vector<double> doubles;
            parsedoubles(doubles, command.substr(2));
            if (doubles.size() == 4)
                result = setrot(doubles[0], doubles[1], doubles[2], doubles[3]);
            else
                result = "Wrong rotation format";
        }
        else
            result = "NOP: when test is running";
        break;
    }
    case 'K': {
        if (!running) {
            std::string butstring = command.substr(2, command.size() - 1);
            int newval = stoi(butstring);
            if (newval < 0 || newval > 15)
                return "invalid button command " + command;
            buttonState = newval;
        }
        else
            result = "NOP: when test is running";
        break;
    }
    case 'T': {
        // Test case command
        switch (command[2]) {
        case 'r': { // Run test
            running = true;
            testcase_starttime = std::chrono::system_clock::now();
            result = "ok";
            break;
        }
        case 'e': { // End test
            running = false;
            result = "ok";
            break;
        }
        case 'c': { // Clear Test Case
            buttonstates.clear();
            samples.clear();
            result = "ok";
            break;
        }
        case 'k': { // Add key state
            std::vector<double> doubles;
            parsedoubles(doubles, command.substr(4));
            if (doubles.size() == 2) {
                buttonstates.push_back(Buttonstate(doubles[0], (int)doubles[1]));
                result = "ok";
            }
            else
                result = "Wrong format";

            break;
        }
        case 's': { // Add sample
            std::vector<double> doubles;
            parsedoubles(doubles, command.substr(4));
            samples.push_back(Sample(doubles));
            break;
        }
        }
    }
    }
    return result;
}

void PositionManager::SetTime(std::chrono::system_clock::time_point t)
{
    time_now = t - testcase_starttime;
}

int PositionManager::GetKeys()
{
    if (running) {
        // Get buttonstate depending on time
        if (buttonstates.size() > 0) {
            buttonState = buttonstates[0].state;
            for (auto k : buttonstates) {
                if (k.t > time_now.count())
                    break;
                buttonState = k.state;

            }
        }
    }
    return buttonState;
}

void PositionManager::interpolate(double t)
{

    if (samples.size() == 0)
        return;
    // First find the two samples to interpolate between
    auto previous = samples[0];
    for (size_t i = 0; i < samples.size() - 1; i++) {
        if (t == samples[i].t) {
            rotpos = samples[i];
            return;
        }
        if (t > samples[i].t&& t < samples[i + 1].t) {
            // linear Interpolation
            Sample& v1 = samples[i];
            Sample& v2 = samples[i + 1];
            double factor = (t - samples[i].t) / (samples[i + 1].t - samples[i].t);
            for (size_t i = 0; i < 7; i++)
                rotpos.values[i] = v1.values[i] + factor * (v2.values[i] - v1.values[i]);
            return;
        }
    }
    // After interval return last sample
    rotpos = samples[samples.size() - 1];
}
