/***********************************************************************
 * testaudio.h
 *  
 *    Audio Library
 *
 *
 * Toby Opferman Copyright (c) 2003
 *
 ***********************************************************************/

#include <windows.h>
#include <mmsystem.h>

#ifndef __WAVELIB_H__
#define __WAVELIB_H__


typedef PVOID HWAVELIB;

#ifdef __cplusplus
extern "C" {
#endif


HWAVELIB WaveLib_Init(PCHAR pAudioFile, BOOL bPause);
void WaveLib_UnInit(HWAVELIB hWaveLib);
void WaveLib_Pause(HWAVELIB hWaveLib, BOOL bPause);

#ifdef __cplusplus

struct command_struct {
    int delay;
};
extern HANDLE events[2];
extern HANDLE memhandle;
extern command_struct* command;
}
#endif



#endif

