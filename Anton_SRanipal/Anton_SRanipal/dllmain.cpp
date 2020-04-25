// dllmain.cpp : Defines the entry point for the DLL application.
#include "zeromqthread.hpp"
#include "DirectionManager.hpp"

#include <cstdint>

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

struct SingleEyeData {
    /** The bits containing all validity for this frame.*/
    uint64_t eye_data_validata_bit_mask;
    /** The point in the eye from which the gaze ray originates in meter miles.(right-handed coordinate system)*/
    float gaze_origin_mm[3];
    /** The normalized gaze direction of the eye in [0,1].(right-handed coordinate system)*/
    float gaze_direction_normalized[3];
    /** The diameter of the pupil in meter miles*/
    float pupil_diameter_mm;
    /** A value representing how open the eye is.*/
    float eye_openness;
    /** The normalized position of a pupil in [0,1]*/
    float pupil_position_in_sensor_area[2];
};

struct CombinedEyeData {
    SingleEyeData eye_data;
    int /*bool*/ convergence_distance_validity;
    float convergence_distance_mm;
};

struct TrackingImprovements {
    int count;
    int items[10];
};


struct VerboseData
{
    /** A instance of the struct as @ref EyeData related to the left eye*/
    SingleEyeData left;
    /** A instance of the struct as @ref EyeData related to the right eye*/
    SingleEyeData right;
    /** A instance of the struct as @ref EyeData related to the combined eye*/
    CombinedEyeData combined;
    TrackingImprovements tracking_improvements;
};


struct EyeData {
    int no_user;
    int frame_sequence;
    int timestamp;
    VerboseData verbose_data;
};

class ZMQ
{
public:
    ZMQ() : ZMQthread(5555) {}
    void start();
    void stop();
    void cmdcallback(char* cmd_str);
    DirectionManager dirmgr;
private:
    ZeroMQthread ZMQthread;

};
void ZMQ::start()
{
    extern void cmdcallbackfunction(void* obj, char* buffer);
    ZMQthread.start(true, this, cmdcallbackfunction);
}

void ZMQ::stop() 
{
    ZMQthread.stop();
}

void ZMQ::cmdcallback(char* cmd_str)
{
    std::string command(cmd_str);
    std::string result;
    std::vector<double> doubles;
    if (command.size() > 3) {
        char cmd = command[0];
        if (cmd == 'E')
            result = dirmgr.HandleCommand(command.substr(2));
        else if (cmd == 'G') {
            result = dirmgr.HandleCommand(command.substr(2));
        }
        else
            result = "invalid command " + std::string(cmd_str);
    }
    else
        result = "too short command " + std::string(cmd_str);
    strcpy_s(cmd_str, 200, result.c_str());
    cmd_str[100] = 0;
    return;
}
void cmdcallbackfunction(void* obj, char* buffer)
{
    ((ZMQ*)obj)->cmdcallback(buffer);
    buffer[0] = 'o';
    buffer[1] = 'k';
    buffer[2] = 0x00;
}

ZMQ ZMQobj;

extern "C" __declspec(dllexport) int CreateRuntimeConnection()
{
    return 0;

}
extern "C" __declspec(dllexport) int EyeCalibration_GetLastCommandError()
{
    return 0;

}
extern "C" __declspec(dllexport) int EyeCalibration_Initial()
{
    return 0;

}
extern "C" __declspec(dllexport) int EyeCalibration_Release()
{
    return 0;

}
extern "C" __declspec(dllexport) int EyeCalibration_SendCommand()
{
    return 0;

}
int seqcount = 5;
bool user = false;
extern "C" __declspec(dllexport) int GetEyeData(EyeData * p)

{
    std::chrono::system_clock::time_point t = std::chrono::system_clock::now();
    ZMQobj.dirmgr.SetTime(t);
    Direction dir;
    ZMQobj.dirmgr.GetDir(dir);

    p->frame_sequence = 5000 + seqcount;
    p->no_user = user;
    user = !user;
    p->timestamp = seqcount;
    seqcount++;
    // Set both eyes active
    p->verbose_data.left.eye_data_validata_bit_mask = 0xF;
    p->verbose_data.left.eye_openness = 1.0;
    p->verbose_data.left.pupil_diameter_mm = 1.0;
    p->verbose_data.left.gaze_direction_normalized[0] = (float) dir.x;
    p->verbose_data.left.gaze_direction_normalized[1] = (float) dir.y;
    p->verbose_data.left.gaze_direction_normalized[2] = (float) dir.z;
    p->verbose_data.left.pupil_position_in_sensor_area[0] = 0.5;
    p->verbose_data.left.pupil_position_in_sensor_area[1] = 0.5;


    p->verbose_data.right.eye_data_validata_bit_mask = 0xF;
    p->verbose_data.right.eye_openness = 1.0;
    p->verbose_data.right.pupil_diameter_mm = 1.0;
    p->verbose_data.right.gaze_direction_normalized[0] = (float) dir.x;
    p->verbose_data.right.gaze_direction_normalized[1] = (float) dir.y;
    p->verbose_data.right.gaze_direction_normalized[2] = (float) dir.z;
    p->verbose_data.right.pupil_position_in_sensor_area[0] = 0.5;
    p->verbose_data.right.pupil_position_in_sensor_area[1] = 0.5;

    return 0;
}

extern "C" __declspec(dllexport) int GetEyeDataAndImage()
{
    return 0;

}
extern "C" __declspec(dllexport) int GetEyeData_v2()
{
    return 0;

}
extern "C" __declspec(dllexport) int GetEyeParameter()
{
    return 0;

}
extern "C" __declspec(dllexport) int GetLipData()
{
    return 0;

}
extern "C" __declspec(dllexport) int GetLipData_v2()
{
    return 0;

}
extern "C" __declspec(dllexport) int GetStatus()
{
    return 0;

}
extern "C" __declspec(dllexport) int Initial()
{
    ZMQobj.start(); 
    return 0;
}

extern "C" __declspec(dllexport) int IsUserNeedCalibration()
{
    return 0;

}
extern "C" __declspec(dllexport) BOOL IsViveProEye()
{
    return TRUE;
}

extern "C" __declspec(dllexport) int LaunchEyeCalibration()
{
    return 0;
}
extern "C" __declspec(dllexport) int RegisterEyeDataCallback()
{
    return 0;
}
extern "C" __declspec(dllexport) int RegisterEyeDataCallback_v2()
{
    return 0;

}
extern "C" __declspec(dllexport) int Release()
{
    ZMQobj.stop();
    return 0;

}
extern "C" __declspec(dllexport) int SRanipal_GetVersion()
{
    return 0;

}
extern "C" __declspec(dllexport) int SetEyeParameter()
{
    return 0;

}
extern "C" __declspec(dllexport) int UnregisterEyeDataCallback()
{
    return 0;

}
extern "C" __declspec(dllexport) int UnregisterEyeDataCallback_v2()
{
    return 0;

}
