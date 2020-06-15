// dllmain.cpp : Defines the entry point for the DLL application.
#include "wavelib.h"
typedef PVOID HWAVELIB;
HWAVELIB WaveLib_ai_Init(bool);
bool WaveLib_ai_Load(HWAVELIB handle, char* pWaveFile);
bool WaveLib_ai_Play(HWAVELIB, int);
bool WaveLib_ai_Exit(HWAVELIB);
bool WaveLib_ai_LoadSoundProcess(char* pWaveFile);
bool WaveLib_ai_RunSoundProcess(int delay_ms);
void WaveLib_setSoundProcessPath(const char*);
void WaveLib_ai_setSoundBufferSize(HWAVELIB, int size_kb);

HWAVELIB handle = nullptr;

extern "C" __declspec(dllexport) bool Initiate()
{
    handle = WaveLib_ai_Init(true);
    return handle != nullptr;

}
extern "C" __declspec(dllexport) bool Close()
{
    WaveLib_ai_Exit(handle);
    return true;

}

extern "C" __declspec(dllexport) bool LoadSound(char * p)
{
    if (handle == nullptr)
        Initiate();
    return WaveLib_ai_Load(handle, p);
}

extern "C" __declspec(dllexport) bool DoPlaySound(int delay_ms)
{
    return WaveLib_ai_Play(handle, delay_ms);

}

extern "C" __declspec(dllexport) bool LoadSoundProcess(char* p)
{
    WaveLib_setSoundProcessPath(".\\Assets\\Plugins");
    return WaveLib_ai_LoadSoundProcess(p);

}

extern "C" __declspec(dllexport) bool RunSoundProcess(int delay_ms)
{
    return WaveLib_ai_RunSoundProcess(delay_ms);

}
extern "C" __declspec(dllexport) void SetSoundBufferSize(int size_kb)
{
    WaveLib_ai_setSoundBufferSize(handle, size_kb);

}
