#include "DirectionManager.hpp"

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

void parsedoubles(std::vector<double>& res, const std::string& params)
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

DirectionManager::DirectionManager()
{
    testcase_starttime = std::chrono::system_clock::now();
}

void DirectionManager::GetDir(Direction& dir)
{
    if (running) {
        // Interpolate
        interpolate(time_now.count());

    }
    
    dir.x = direction.values[0];
    dir.y = direction.values[1];
    dir.z = cz;
}

std::string DirectionManager::setdir(double x, double y, double z)
{
    cz = z;
    direction.values[0] = x;
    direction.values[1] = y;
    return "ok";
}


std::string DirectionManager::HandleCommand(std::string command)
{
    std::string result;
    switch (command[0]) {
    case 'D': {
        // Set Direction
        if (!running) {
            std::vector<double> doubles;
            parsedoubles(doubles, command.substr(2));
            if (doubles.size() == 2)
                result = setdir(doubles[0], doubles[1], 1.0);
            else
                result = "Wrong position format";
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
            samples.clear();
            result = "ok";
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

void DirectionManager::SetTime(std::chrono::system_clock::time_point t)
{
    time_now = t - testcase_starttime;
}

void DirectionManager::interpolate(double t)
{

    if (samples.size() == 0)
        return;
    // First find the two samples to interpolate between
    auto previous = samples[0];
    for (size_t i = 0; i < samples.size() - 1; i++) {
        if (t == samples[i].t) {
            //rotpos = samples[i];
            return;
        }
        if (t > samples[i].t&& t < samples[i + 1].t) {
            // linear Interpolation
            Sample& v1 = samples[i];
            Sample& v2 = samples[i + 1];
            double factor = (t - samples[i].t) / (samples[i + 1].t - samples[i].t);
            for (size_t i = 0; i < 2; i++)
                direction.values[i] = v1.values[i] + factor * (v2.values[i] - v1.values[i]);
            return;
        }
    }
    // After interval return last sample
    //rotpos = samples[samples.size() - 1];
}
