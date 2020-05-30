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
  extern HWAVELIB WaveLib_ai_Init();
  extern bool WaveLib_ai_Load(HWAVELIB, char*);
  extern bool WaveLib_ai_Play(HWAVELIB, int);
  extern bool WaveLib_ai_Play_nothread(HWAVELIB, int);
  void createevents();

  // Test client mode: used to send signals to a process in server mode
  void WaveTest_Client() {
      createevents();
      printf("1: setPlay, 2: setExit 3:Exit this program\n");
      while (true) {
          switch (_getch()) {
          case 0x31:
              command->delay = 50;
              SetEvent(events[0]);
              printf("Send Play 50\n");
              break;
          case 0x32:
              command->delay = 150;
              SetEvent(events[0]);
              printf("Send Play 150\n");
              break;
          case 0x33:
              command->delay = 1000;
              SetEvent(events[0]);
              printf("Send Play 1000\n");
              break;
          case 0x38:
              printf("Send Exit\n");
              SetEvent(events[1]);
              break;
          case 0x39:
              exit(0);
          }
      }
  }

  // Test server mode: sound run directly when signalled
  void WaveTest_Server(char* pszFileName) 
  {
      HWAVELIB hWaveLib = NULL;
      hWaveLib = WaveLib_ai_Init();
      if (!WaveLib_ai_Load(hWaveLib, pszFileName))
          exit(-1);
      createevents();
      
      while (true) {
          DWORD res = WaitForMultipleObjects(2, events, FALSE, INFINITE);

          if (res == WAIT_OBJECT_0) {
              WaveLib_ai_Play_nothread(hWaveLib, command->delay);
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
      hWaveLib = WaveLib_ai_Init();
      while (1) {
          switch (_getch()) {
          case 0x31:
              printf("load\n");
              WaveLib_ai_Load(hWaveLib, pszFileName);
              break;
          case 0x32:
              printf("playt\n");
              WaveLib_ai_Play(hWaveLib, 2000);
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
     printf("\n   WaveTest <FileName> <client/server>\n\n");
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
 int main(int argc, char* argv[])
 {
     if (argc == 3) {
         if (strcmp(argv[2], "server") == 0)
             // Run in 'signal mode'
             WaveTest_Server(argv[1]);
         else if (strcmp(argv[2], "client") == 0)
             WaveTest_Client();
         else
             WaveTest_PrintArgs();

     }
     else if (argc == 2)
     {
         WaveTest_Play(argv[1]);
     }
     else
     {
         WaveTest_PrintArgs();
     }

     return 0;
 }
