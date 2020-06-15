/***********************************************************************
 * wavelib.c
 *  
 *    Audio Library
 *
 *
 *  Supports .WAV files, Very Simplistic Parser
 *
 *
 * Toby Opferman Copyright (c) 2003
 *
 ***********************************************************************/
 
 

#include "wavelib.h"
#include <stdio.h>
#pragma comment(lib,"winmm")	

HANDLE events[3];
HANDLE memhandle;

command_struct* command;

bool createevents()
{
    events[0] = CreateEvent(NULL, FALSE, FALSE, "KajsaoAntonsSoundServer");
    events[1] = CreateEvent(NULL, FALSE, FALSE, "Abort_KajsaoAntonsSoundServer");
    events[2] = CreateEvent(NULL, FALSE, FALSE, "Abort_KajsaoAntonsSoundServerReply");
    memhandle = CreateFileMapping(INVALID_HANDLE_VALUE, NULL, PAGE_READWRITE, 0, sizeof(command_struct), "KajsaoAntonsSoundServerMemory");
    auto ecode = GetLastError();
    command = (command_struct*)MapViewOfFile(memhandle, FILE_MAP_ALL_ACCESS, 0, 0, sizeof(command_struct));
    if (ecode == ERROR_ALREADY_EXISTS) {
        printf("Mem exist\n");
        return true;
    }
    printf("New Mem\n");
    return false;

}

void releaseevents()
{
    UnmapViewOfFile(command);
    if (memhandle != nullptr) {
        CloseHandle(memhandle);
    }
    CloseHandle(events[0]);
    CloseHandle(events[1]);
    CloseHandle(events[2]);
}

 /***********************************************************************
  * Internal Structures
  ***********************************************************************/
typedef struct {
    
    UCHAR IdentifierString[4];
    DWORD dwLength;

} RIFF_CHUNK, *PRIFF_CHUNK;


typedef struct {

    WORD  wFormatTag;         // Format category
    WORD  wChannels;          // Number of channels
    DWORD dwSamplesPerSec;    // Sampling rate
    DWORD dwAvgBytesPerSec;   // For buffer estimation
    WORD  wBlockAlign;        // Data block size
    WORD  wBitsPerSample;
    

} WAVE_FILE_HEADER, *PWAVE_FILE_HEADER;


typedef struct _wave_sample {

     WAVEFORMATEX WaveFormatEx;
     char *pSampleData;
     UINT Index;
     UINT Size;
     DWORD dwId;
     DWORD bPlaying;
     struct _wave_sample *pNext;

} WAVE_SAMPLE, *PWAVE_SAMPLE;

#define SOUNDBUFFERS 8
typedef struct {
     HWAVEOUT hWaveOut;
     HANDLE hEvent;
     HANDLE hPlayEvent;
     HANDLE hThread;
     WAVE_SAMPLE WaveSample;
     BOOL bWaveThreadShouldDie; 
     BOOL bEndOfClip;
     WAVEHDR WaveHdr[8];
     char* AudioBuffer[SOUNDBUFFERS];
     BOOL bPaused;
     int PlayDelay;
} WAVELIB, *PWAVELIB;


int SAMPLE_SIZE = 8 * 1024;
void WaveLib_ai_setSoundBufferSize(HWAVELIB handle, int size_kb)
{
    PWAVELIB pWaveLib = (PWAVELIB)handle;
    if (size_kb * 1024 == SAMPLE_SIZE && pWaveLib->AudioBuffer[0] != 0)
        return;
    SAMPLE_SIZE = size_kb * 1024;
    for (int i = 0; i < SOUNDBUFFERS; i++) {
        free(pWaveLib->AudioBuffer[i]);
        pWaveLib->AudioBuffer[i] = (char*)malloc(size_kb * 1024);
    }
}


 /***********************************************************************
  * Internal Functions
  ***********************************************************************/
void CALLBACK WaveLib_WaveOutputCallback(HWAVEOUT hwo, UINT uMsg, DWORD_PTR dwInstance, DWORD_PTR dwParam1, DWORD_PTR dwParam2);
BOOL WaveLib_OpenWaveSample(CHAR *pFileName, PWAVE_SAMPLE pWaveSample);
void WaveLib_WaveOpen(HWAVEOUT hWaveOut, PWAVELIB pWaveLib);
void WaveLib_WaveDone(HWAVEOUT hWaveOut, PWAVELIB pWaveLib);
DWORD WINAPI WaveLib_AudioThread(PVOID pDataInput);
void WaveLib_CreateThread(PWAVELIB pWaveLib);
void WaveLib_SetupAudio(PWAVELIB pWaveLib);
void WaveLib_WaveClose(HWAVEOUT hWaveOut, PWAVELIB pWaveLib);
bool WaveLib_AudioBuffer(PWAVELIB pWaveLib, UINT Index);
void runSound(PWAVELIB pWaveLib);


 /***********************************************************************
  * WaveLib_Init
  *  
  *    Audio!
  *
  * Parameters
  *     
  * 
  * Return Value
  *     Handle To This Audio Session
  *
  ***********************************************************************/
HWAVELIB WaveLib_Init(PCHAR pWaveFile, BOOL bPause)
 {
     PWAVELIB pWaveLib = NULL;
 
     if(pWaveLib = (PWAVELIB)LocalAlloc(LMEM_ZEROINIT, sizeof(WAVELIB)))
     {
         pWaveLib->bPaused = bPause;
         WaveLib_ai_setSoundBufferSize(pWaveLib, 4);
         if(WaveLib_OpenWaveSample(pWaveFile, &pWaveLib->WaveSample))
         {
             if(waveOutOpen(&pWaveLib->hWaveOut, WAVE_MAPPER, &pWaveLib->WaveSample.WaveFormatEx, (DWORD_PTR)WaveLib_WaveOutputCallback, (DWORD_PTR)pWaveLib, CALLBACK_FUNCTION) != MMSYSERR_NOERROR)
             {
                WaveLib_UnInit((HWAVELIB)pWaveLib);
                pWaveLib = NULL;
             }
             else
             {
 
                 if(pWaveLib->bPaused)
                 {
                     waveOutPause(pWaveLib->hWaveOut);
                 }

                 return pWaveLib; // WaveLib_CreateThread(pWaveLib);
             }
         }
         else
         {
             WaveLib_UnInit((HWAVELIB)pWaveLib);
             pWaveLib = NULL;
         }
     }

     return pWaveLib;
 }










 /***********************************************************************
  * WaveLib_Pause
  *  
  *    Audio!
  *
  * Parameters
  *     
  * 
  * Return Value
  *     Handle To This Audio Session
  *
  ***********************************************************************/
 void WaveLib_Pause(HWAVELIB hWaveLib, BOOL bPause)
 {
     PWAVELIB pWaveLib = (PWAVELIB)hWaveLib;

     pWaveLib->bPaused = bPause;

     if(pWaveLib->bPaused)
     {
         waveOutPause(pWaveLib->hWaveOut);
     }
     else
     {
         waveOutRestart(pWaveLib->hWaveOut);
     }
 }

 /***********************************************************************
  * WaveLib_Init
  *  
  *    Audio!
  *
  * Parameters
  *     
  * 
  * Return Value
  *     Handle To This Audio Session
  *
  ***********************************************************************/
 void WaveLib_UnInit(HWAVELIB hWaveLib)
 {
     PWAVELIB pWaveLib = (PWAVELIB)hWaveLib;

     if(pWaveLib)
     {
         if(pWaveLib->hThread)
         {
             pWaveLib->bWaveThreadShouldDie = TRUE;

             SetEvent(pWaveLib->hEvent);
             WaitForSingleObject(pWaveLib->hThread, INFINITE);

             CloseHandle(pWaveLib->hEvent);
             CloseHandle(pWaveLib->hThread);
         }

         if(pWaveLib->hWaveOut)
         {
             waveOutClose(pWaveLib->hWaveOut);
         }


         if(pWaveLib->WaveSample.pSampleData)
         {
             LocalFree(pWaveLib->WaveSample.pSampleData);
         }

         LocalFree(pWaveLib);
     }

 }
 
 
 /***********************************************************************
  * WaveLib_WaveOutputCallback
  *  
  *    Audio Callback 
  *
  * Parameters
  *     
  * 
  * Return Value
  *     Handle To This Audio Session
  *
  ***********************************************************************/ 
void CALLBACK WaveLib_WaveOutputCallback(HWAVEOUT hwo, UINT uMsg, DWORD_PTR dwInstance, DWORD_PTR dwParam1, DWORD_PTR dwParam2)
{
    PWAVELIB pWaveLib = (PWAVELIB)dwInstance;

    switch(uMsg)
    {
      case WOM_OPEN:
            WaveLib_WaveOpen(hwo, pWaveLib);
            break;

       case WOM_DONE:
            WaveLib_WaveDone(hwo, pWaveLib);
            break;

       case WOM_CLOSE:
            WaveLib_WaveClose(hwo, pWaveLib);
            break;
    }
}



 
 /***********************************************************************
  * WaveLib_WaveOpen
  *  
  *    Audio Callback 
  *
  * Parameters
  *     
  * 
  * Return Value
  *     Handle To This Audio Session
  *
  ***********************************************************************/
void WaveLib_WaveOpen(HWAVEOUT hWaveOut, PWAVELIB pWaveLib)
{
  // Do Nothing
}


 /***********************************************************************
  * WaveLib_WaveDone
  *  
  *    Audio Callback 
  *
  * Parameters
  *     
  * 
  * Return Value
  *     Handle To This Audio Session
  *
  ***********************************************************************/
void WaveLib_WaveDone(HWAVEOUT hWaveOut, PWAVELIB pWaveLib)
{
    SetEvent(pWaveLib->hEvent);
}


 /***********************************************************************
  * WaveLib_WaveClose
  *  
  *    Audio Callback 
  *
  * Parameters
  *     
  * 
  * Return Value
  *     Handle To This Audio Session
  *
  ***********************************************************************/
void WaveLib_WaveClose(HWAVEOUT hWaveOut, PWAVELIB pWaveLib)
{
  // Do Nothing
}



 /***********************************************************************
  * WaveLib_OpenWaveFile
  *  
  *    Audio Callback 
  *
  * Parameters
  *     
  * 
  * Return Value
  *     Handle To This Audio Session
  *
  ***********************************************************************/
BOOL WaveLib_OpenWaveSample(CHAR *pFileName, PWAVE_SAMPLE pWaveSample)
{
    BOOL bSampleLoaded = FALSE;
    HANDLE hFile;
    RIFF_CHUNK RiffChunk = {0};
    DWORD dwBytes, dwReturnValue;
    WAVE_FILE_HEADER WaveFileHeader;
    DWORD dwIncrementBytes;

    if(hFile = CreateFile(pFileName, GENERIC_READ, 0, NULL, OPEN_EXISTING, 0, NULL))
    {
        char szIdentifier[5] = {0};

        SetFilePointer(hFile, 12, NULL, FILE_CURRENT);
        

        ReadFile(hFile, &RiffChunk, sizeof(RiffChunk), &dwBytes, NULL);
        ReadFile(hFile, &WaveFileHeader, sizeof(WaveFileHeader), &dwBytes, NULL);

        pWaveSample->WaveFormatEx.wFormatTag      = WaveFileHeader.wFormatTag;         
        pWaveSample->WaveFormatEx.nChannels       = WaveFileHeader.wChannels;          
        pWaveSample->WaveFormatEx.nSamplesPerSec  = WaveFileHeader.dwSamplesPerSec;    
        pWaveSample->WaveFormatEx.nAvgBytesPerSec = WaveFileHeader.dwAvgBytesPerSec;   
        pWaveSample->WaveFormatEx.nBlockAlign     = WaveFileHeader.wBlockAlign;  
        pWaveSample->WaveFormatEx.wBitsPerSample  = WaveFileHeader.wBitsPerSample;
        pWaveSample->WaveFormatEx.cbSize          = 0;

        dwIncrementBytes = dwBytes;

        do {
             SetFilePointer(hFile, RiffChunk.dwLength - dwIncrementBytes, NULL, FILE_CURRENT);
             
             dwReturnValue = GetLastError();

             if(dwReturnValue == 0)
             {
                 dwBytes = ReadFile(hFile, &RiffChunk, sizeof(RiffChunk), &dwBytes, NULL);
             
                 dwIncrementBytes = 0;

                 memcpy(szIdentifier, RiffChunk.IdentifierString, 4); 
             }

        } while(_stricmp(szIdentifier, "data") && dwReturnValue == 0) ;

        if(dwReturnValue == 0)
        {
            pWaveSample->pSampleData = (char *)LocalAlloc(LMEM_ZEROINIT, RiffChunk.dwLength);

            pWaveSample->Size = RiffChunk.dwLength;

            ReadFile(hFile, pWaveSample->pSampleData, RiffChunk.dwLength, &dwBytes, NULL);

            CloseHandle(hFile);

            bSampleLoaded = TRUE;
        }
    }

    return bSampleLoaded;
}





 /***********************************************************************
  * WaveLib_CreateThread
  *  
  *    Audio Callback 
  *
  * Parameters
  *     
  * 
  * Return Value
  *     Handle To This Audio Session
  *
  ***********************************************************************/
void WaveLib_CreateEvents(PWAVELIB pWaveLib)
{
    pWaveLib->hEvent = CreateEvent(NULL, FALSE, FALSE, NULL); // Event used during play
    pWaveLib->hPlayEvent = CreateEvent(NULL, FALSE, FALSE, NULL); // Event when play should start
}

void WaveLib_CreateThread(PWAVELIB pWaveLib)
{
    DWORD dwThreadId;
    pWaveLib->hThread = CreateThread(NULL, 0, WaveLib_AudioThread, pWaveLib, 0, &dwThreadId);

}

 /***********************************************************************
  * WaveLib_AudioThread
  *  
  *    Audio Thread
  *
  * Parameters
  *     
  * 
  * Return Value
  *     Handle To This Audio Session
  *
  ***********************************************************************/
DWORD WINAPI WaveLib_AudioThread(PVOID pDataInput)
{
    PWAVELIB pWaveLib = (PWAVELIB)pDataInput;
    DWORD dwReturnValue = 0;

    while (!pWaveLib->bWaveThreadShouldDie)
    {
        WaitForSingleObject(pWaveLib->hPlayEvent, INFINITE);
        Sleep(pWaveLib->PlayDelay);
        runSound(pWaveLib);
    }
    return dwReturnValue;
}

#include <chrono>

void runSound(PWAVELIB pWaveLib)
{
    DWORD dwReturnValue = 0;
    UINT Index;
    pWaveLib->WaveSample.Index = 0;
    pWaveLib->bEndOfClip = false;

    WaveLib_SetupAudio(pWaveLib);
    WaitForSingleObject(pWaveLib->hEvent, INFINITE);

    while (!pWaveLib->bEndOfClip)
    {

        for (Index = 0; Index < 8; Index++)
        {
            if (pWaveLib->WaveHdr[Index].dwFlags & WHDR_DONE)
            {
                WaveLib_AudioBuffer(pWaveLib, Index);
                waveOutWrite(pWaveLib->hWaveOut, &pWaveLib->WaveHdr[Index], sizeof(WAVEHDR));
                if (pWaveLib->bEndOfClip)
                    break;
            }
        }
        WaitForSingleObject(pWaveLib->hEvent, INFINITE);

    }

    waveOutReset(pWaveLib->hWaveOut);
}


 /***********************************************************************
  * WaveLib_AudioBuffer
  *  
  * 
  *
  ***********************************************************************/
bool WaveLib_AudioBuffer(PWAVELIB pWaveLib, UINT Index)
{
    int size_left = pWaveLib->WaveSample.Size - pWaveLib->WaveSample.Index;
    if (size_left == 0)
        return false;

    UINT uiBytesNotUsed = SAMPLE_SIZE;

    pWaveLib->WaveHdr[Index].dwFlags &= ~WHDR_DONE;

    if(size_left < uiBytesNotUsed)
    {
        uiBytesNotUsed -= size_left;
        memcpy(pWaveLib->AudioBuffer[Index], pWaveLib->WaveSample.pSampleData + pWaveLib->WaveSample.Index, size_left);
        memset(pWaveLib->AudioBuffer[Index] + size_left, 0, uiBytesNotUsed);
        pWaveLib->WaveSample.Index = pWaveLib->WaveSample.Size;
        uiBytesNotUsed = 0;

//        uiBytesNotUsed -= size_left;
//        memcpy(pWaveLib->AudioBuffer[Index], pWaveLib->WaveSample.pSampleData + pWaveLib->WaveSample.Index, size_left);
//        pWaveLib->WaveSample.Index = pWaveLib->WaveSample.Size;
        pWaveLib->bEndOfClip = true;
    }
    else
    {
       memcpy(pWaveLib->AudioBuffer[Index], pWaveLib->WaveSample.pSampleData + pWaveLib->WaveSample.Index, uiBytesNotUsed);
       pWaveLib->WaveSample.Index += SAMPLE_SIZE;
       uiBytesNotUsed = 0;
    }

    pWaveLib->WaveHdr[Index].lpData = pWaveLib->AudioBuffer[Index];

    pWaveLib->WaveHdr[Index].dwBufferLength = SAMPLE_SIZE - uiBytesNotUsed;
    return true;
}






 /***********************************************************************
  * WaveLib_SetupAudio
  *  
  *    Audio Thread
  *
  * Parameters
  *     
  * 
  * Return Value
  *     Handle To This Audio Session
  *
  ***********************************************************************/
void WaveLib_SetupAudio(PWAVELIB pWaveLib)
{
    UINT Index = 0;

    for(Index = 0; Index < 8; Index++)
    {
        pWaveLib->WaveHdr[Index].dwBufferLength = SAMPLE_SIZE;
        pWaveLib->WaveHdr[Index].lpData         = pWaveLib->AudioBuffer[Index]; 

        waveOutPrepareHeader(pWaveLib->hWaveOut, &pWaveLib->WaveHdr[Index], sizeof(WAVEHDR));

        WaveLib_AudioBuffer(pWaveLib, Index);

        waveOutWrite(pWaveLib->hWaveOut, &pWaveLib->WaveHdr[Index], sizeof(WAVEHDR));
        if (pWaveLib->bEndOfClip)
            return;
    }
}


bool WaveLib_ai_Exit(HWAVELIB handle)
{
    PWAVELIB pWaveLib = (PWAVELIB)handle;
    pWaveLib->bWaveThreadShouldDie = true;
    SetEvent(pWaveLib->hPlayEvent);
    return true;
}

HWAVELIB WaveLib_ai_Init(bool usethread)
{
    PWAVELIB pWaveLib = (PWAVELIB)LocalAlloc(LMEM_ZEROINIT, sizeof(WAVELIB));
    WaveLib_ai_setSoundBufferSize(pWaveLib, 4);
    WaveLib_CreateEvents(pWaveLib);
    if (usethread) {
        pWaveLib->bWaveThreadShouldDie = false;
        WaveLib_CreateThread(pWaveLib);
        HANDLE hthread = GetCurrentThread();
        if (SetThreadPriority(hthread, THREAD_PRIORITY_TIME_CRITICAL) == FALSE)
            printf("cannot set thread prio\n");
        if (GetThreadPriority(hthread) != THREAD_PRIORITY_TIME_CRITICAL)
            printf("wrong thread prio 0x%x", GetThreadPriority(hthread));
    }
    return (HWAVELIB)pWaveLib;
}

bool WaveLib_ai_Load(HWAVELIB handle, char* pWaveFile)
{
    PWAVELIB pWaveLib = (PWAVELIB) handle;
    if (handle == nullptr)
        return false;

    //pWaveLib->bPaused = bPause;
    if (WaveLib_OpenWaveSample(pWaveFile, &pWaveLib->WaveSample))  {
        if (waveOutOpen(&pWaveLib->hWaveOut, WAVE_MAPPER, &pWaveLib->WaveSample.WaveFormatEx, (DWORD_PTR) WaveLib_WaveOutputCallback, (DWORD_PTR)pWaveLib, CALLBACK_FUNCTION) != MMSYSERR_NOERROR)
        {
            WaveLib_UnInit((HWAVELIB)pWaveLib);
            return false;
        }
        else
        {
            if (pWaveLib->bPaused)
            {
                waveOutPause(pWaveLib->hWaveOut);
            }
            return true;
        }
    }
    else
    {
        WaveLib_UnInit((HWAVELIB)pWaveLib);
        return false;
    }

    return false;

}

bool WaveLib_ai_Play(HWAVELIB handle, int delay)
{
    if (handle != nullptr) {
        PWAVELIB pWaveLib = (PWAVELIB)handle;
        pWaveLib->PlayDelay = delay;
        SetEvent(pWaveLib->hPlayEvent);
        return true;
    }
    return false;
}
bool WaveLib_ai_Play_nothread(HWAVELIB handle, int delay)
{
    if (handle != nullptr) {
        PWAVELIB pWaveLib = (PWAVELIB)handle;
        Sleep(delay);
        runSound(pWaveLib);
        return true;
    }
    return false;
}
#include <stdio.h>
char WaveLib_ai_SoundProcessName[200];
void WaveLib_setSoundProcessPath(const char* name) {
    strcpy_s(WaveLib_ai_SoundProcessName, sizeof(WaveLib_ai_SoundProcessName), name);
    strcat_s(WaveLib_ai_SoundProcessName, sizeof(WaveLib_ai_SoundProcessName), "\\SoundPlayer.exe");
}

bool WaveLib_ai_LoadSoundProcess(char* pWaveFile)
{
    if (createevents())
        return true; // The process is still alive

    // Start a new server process
    char cmd[200];
    sprintf_s(cmd, 200, "%s %s server", WaveLib_ai_SoundProcessName, pWaveFile);
    
    STARTUPINFO si;
    PROCESS_INFORMATION processinfo;
    si.cb = sizeof(STARTUPINFO);
    si.lpReserved = NULL;
    si.lpTitle = NULL;
    si.lpDesktop = NULL;
    si.dwX = si.dwY = si.dwXSize = si.dwYSize = 0L;
    si.dwFlags = 0;
    si.wShowWindow = SW_NORMAL;
    si.lpReserved2 = NULL;
    si.cbReserved2 = 0;
    BOOL createres = CreateProcess(
        NULL, // pointer to name of executable module 
        cmd, // const_cast<wchar_t*>(cmd.c_str()),           // pointer to command line string
        NULL,                // pointer to process security attributes 
        NULL,                // pointer to thread security attributes 
        TRUE,                // handle inheritance flag 
        0,                   // creation flags 
        NULL,                // pointer to new environment block 
        NULL,                // pointer to current directory name 
        &si,         // pointer to STARTUPINFO 
        &processinfo         // pointer to PROCESS_INFORMATION  
    );
    //if (!createres)
    //    EXCEPT_RETURN_M(IO, NORMAL, "Cannot start adamserver");
    //processid = processinfo.dwProcessId;

    return true;
}

bool WaveLib_ai_RunSoundProcess(int delay_ms) 
{
    command->delay = delay_ms;
    SetEvent(events[0]);
    return true;
}
