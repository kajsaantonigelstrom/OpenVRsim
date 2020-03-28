#include "PositionManager.hpp"

void PositionManager::GetPose(vr::DriverPose_t& _pose)
{
	_pose.vecPosition[0] = px;
	_pose.vecPosition[1] = py;
	_pose.vecPosition[2] = pz;// +2 * std::cos(time_since_epoch_seconds);

	_pose.qRotation.w = rw;
	_pose.qRotation.x = ri;
	_pose.qRotation.y = rj;
	_pose.qRotation.z = rk;
}

std::string PositionManager::HandleCommand(std::string command)
{
    return "";
}

void PositionManager::SetTime(std::chrono::system_clock::time_point t)
{

}

int PositionManager::GetKeys()
{
    return 0;
}

/*

std::string FakeTracker::handlecommand(std::string& cmd)
{
    DriverLog("virtualdriver: cmd: %s\n", cmd);

    vr::EVRInputError result = vr::VRInputError_InvalidDevice;
    switch (cmd[0]) {
    case 'b': // Button state
        std::string butstring = cmd.substr(1, cmd.size() - 1);
        int newval = stoi(butstring);
        if (newval < 0 || newval > 15)
            return "invalid cmd " + cmd;
        buttonState = newval;
    }
    return "ok";
}



    else if (command.find("H") == 0) {
    parsedoubles(doubles, command.substr(2));
    if (doubles.size() == 3)
        result = m_pNullHmdLatest->setpos(doubles[0], doubles[1], doubles[2]);
    else if (doubles.size() == 4)
        result = m_pNullHmdLatest->setrot(doubles[0], doubles[1], doubles[2], doubles[3]);
    else
        result = "Wrong format Hpos";
    }
    else if (command.find("L") == 0) {
    parsedoubles(doubles, command.substr(2));
    if (doubles.size() == 3)
        result = _trackers[0]->setpos(doubles[0], doubles[1], doubles[2]);
    else if (doubles.size() == 4)
        result = _trackers[0]->setrot(doubles[0], doubles[1], doubles[2], doubles[3]);
    else
        result = "Wrong format Lpos";
    }
    else if (command.find("R") == 0) {
    parsedoubles(doubles, command.substr(2));
    if (doubles.size() == 3)
        result = _trackers[1]->setpos(doubles[0], doubles[1], doubles[2]);
    else if (doubles.size() == 4)
        result = _trackers[1]->setrot(doubles[0], doubles[1], doubles[2], doubles[3]);
    else
        result = "Wrong format Rpos";
    }
    */