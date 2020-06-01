/***********************************************************************
 * wavetest.c
 *  
 *    Audio Library Test
 *
 *
 *  Supports .WAV files, Very Simplistic Player
 *
 *
 * Toby Opferman Copyright (c) 2004
 *
 ***********************************************************************/
 
 #include <windows.h>
 #include <stdio.h>
 #include <conio.h>
 #include "wavelib.h"
 /***********************************************************************
  * WaveTest_Play
  *  
  *    Play A Wave File
  *
  * Parameters
  *     File Name
  * 
  * Return Value
  *     0
  *
  ***********************************************************************/
  extern HWAVELIB WaveLib_ai_Init(bool);
  extern bool WaveLib_ai_Load(HWAVELIB, char*);
  extern bool WaveLib_ai_Play(HWAVELIB, int);
  extern bool WaveLib_ai_Play_nothread(HWAVELIB, int);
  bool WaveLib_ai_LoadSoundProcess(char* pWaveFile);
  bool WaveLib_ai_RunSoundProcess(int delay_ms);
  void WaveLib_setSoundProcessPath(const char*);

  bool createevents();

  // Test client mode: used to send signals to a process in server mode
#include <chrono>

  void WaveTest_Client() {
      auto starttime = std::chrono::high_resolution_clock::now();
      auto stoptime = std::chrono::high_resolution_clock::now();
      printf("1: setPlay, 2: setExit 3:Exit this program\n");
      while (true) {

          auto ch = _getch();

          starttime = std::chrono::high_resolution_clock::now();

          switch (ch) {
          case 0x31:
              WaveLib_ai_RunSoundProcess(50);
              WaitForSingleObject(events[2], INFINITE);
              stoptime = std::chrono::high_resolution_clock::now();
              printf("Send Play 50\n");
              break;
          case 0x32:
              WaveLib_ai_RunSoundProcess(150);
              WaitForSingleObject(events[2], INFINITE);
              stoptime = std::chrono::high_resolution_clock::now();
              printf("Send Play 150\n");
              break;
          case 0x33:
              WaveLib_ai_RunSoundProcess(1000);
              WaitForSingleObject(events[2], INFINITE);
              stoptime = std::chrono::high_resolution_clock::now();
              printf("Send Play 1000\n");
              break;
          case 0x38:
              printf("Send Exit\n");
              SetEvent(events[1]);
              break;
          case 0x39:
              exit(0);
          }
          auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(stoptime - starttime).count();
          int dur = (int)((duration+500000.0)/1000000);
          dur -= command->delay;
          printf("duration %d\n", dur);
      }
  }

  // Test server mode: sound run directly when signalled
  void WaveTest_Server(char* pszFileName) 
  {
      HWAVELIB hWaveLib = NULL;
      hWaveLib = WaveLib_ai_Init(false);
      if (!WaveLib_ai_Load(hWaveLib, pszFileName))
          exit(-1);
      createevents();

      // Raise priority
      HANDLE procHdl = GetCurrentProcess(); // returns -1
      auto res = SetPriorityClass(procHdl, REALTIME_PRIORITY_CLASS);
      res = GetPriorityClass(procHdl);
      //if (res != REALTIME_PRIORITY_CLASS)
      if (res != HIGH_PRIORITY_CLASS)
          printf("Wrong prio class 0x%x\n", res);

      HANDLE hthread = GetCurrentThread();
      if (SetThreadPriority(hthread, THREAD_PRIORITY_TIME_CRITICAL) == FALSE)
          printf("cannot set thread prio\n");

      while (true) {
          DWORD res = WaitForMultipleObjects(2, events, FALSE, INFINITE);

          if (res == WAIT_OBJECT_0) {
              WaveLib_ai_Play_nothread(hWaveLib, command->delay);
              SetEvent(events[2]);
          }
          else if (res == WAIT_OBJECT_0 + 1)
              exit(0);
      }
  }
  
  // Test Play: sound run in thread when you type '2'
  void WaveTest_Play(char* pszFileName)
  {
      HWAVELIB hWaveLib = NULL;
      printf("1: load, 2: sound, 3: exit\n");
      hWaveLib = WaveLib_ai_Init(true);
      while (1) {
          switch (_getch()) {
          case 0x31:
              printf("load\n");
              WaveLib_ai_Load(hWaveLib, pszFileName);
              break;
          case 0x32:
              printf("playt\n");
              WaveLib_ai_Play(hWaveLib, 800);
              break;
          case 0x33:
              exit(0);
          }
      }
  }


 /***********************************************************************
  * WaveTest_PrintArgs
  *  
  *    Display Program Parameters
  *
  * Parameters
  *     Nothing
  * 
  * Return Value
  *     0
  *
  ***********************************************************************/
 void WaveTest_PrintArgs(void)
 {
     printf("WaveTest .WAV File Player!\n");

     printf("Usage:\n");
     printf("\n   WaveTest <FileName> : sound in a thread in the same process\n");
     printf("\n   WaveTest <FileName> client : start the server and control it from the client\n");
     printf("\n   WaveTest <FileName> server : Used from Unity\n");
     printf("\n   WaveTest priotest : test Priority access\n");

 }


 /***********************************************************************
  * main()
  *
  *    Entry Point
  *
  * Parameters
  *     Number Of Arguements, Arguements
  *
  * Return Value
  *     0
  *
  ***********************************************************************/
 void WaveTest_priotest()
 {
    printf("Priority test\n");
    HANDLE threadHdl = GetCurrentThread();
    HANDLE procHdl = GetCurrentProcess(); // returns -1
    
    auto threadprio = GetThreadPriority(threadHdl);

    auto res = GetPriorityClass(procHdl);
    if (SetPriorityClass(procHdl, REALTIME_PRIORITY_CLASS) == FALSE)
        printf("cannot set process prio\n");

    res = GetPriorityClass(procHdl);
    printf("Process Prio 0x%x\n", res);

    if (SetThreadPriority(threadHdl, THREAD_PRIORITY_TIME_CRITICAL) == FALSE)
        printf("cannot set thread prio\n");

    threadprio = GetThreadPriority(threadHdl);
    printf("Thread prio 0x%x\n", threadprio);

    printf("1: exit");
    while (1) {
        switch (_getch()) {
        case 0x31:
            exit(0);
        }
    }
 }

 int main(int argc, char* argv[])
 {
     if (argc >= 2 && strcmp(argv[1], "priotest") == 0)
         WaveTest_priotest();
     else if (argc >= 3 && strcmp(argv[2], "server") == 0)
         // Run in 'signal mode'
         WaveTest_Server(argv[1]);
     else if (argc >= 3 && strcmp(argv[2], "client") == 0) {
         WaveLib_setSoundProcessPath("..\\x64\\Debug");
         WaveLib_ai_LoadSoundProcess(argv[1]);
         WaveTest_Client();
     }
     else if (argc >= 2) {
         WaveTest_Play(argv[1]);
     }
     else {
         WaveTest_PrintArgs();
     }

     return 0;
 }
