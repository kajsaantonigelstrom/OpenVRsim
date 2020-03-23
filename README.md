
# OpenVRsim
Null driver for openVR (HMD&amp;2controllers) that can be controlled by a Python client

The client is developed using Python 2.7.
Need extra modules:
pip install wxpython
pip install zmq 

The driver is based on the sample example in the openVR SDK.
It installs a HMD and two handles. The movements of these three devices 
will be possible to control from the outside using a socket interface (ZeroMQ)
The purpose is to create a test environment when you do not have an actual HMD available

The driver is developed in c++ using Visual Studio 2019
 
1. Compile and link the .dll in the project OpenVRsim\driver\virtualdevice.sln
2. copy the dll to c:prog\Steam\steamapps\common\SteamVR\drivers\virtualdevice\bin\win64"
3a. To debug the init of the driver, open ...\steamapps\common\SteamVR\bin\win64\vrserver.exe
    in VS2013. As command line args give '--keepalive --earlyload' 
3b. To debug the driver, start openVR and attach a debugger to vrserver.exe

********************************************************************************************
Installation of Steam, SteamVR and the driver
- Install Steam  https://store.steampowered.com/about/
- In Steam, login to your account, get one if you don't have
- In Steam, search for SteamVR and install it
- To start SteamVR you can go through the list of installed apps in Steam
OR just start VRmonitor (c:prog\Steam\steamapps\common\SteamVR\bin\win64)
- To install the driver, this structure is created.
     Directory of z:\Program Files (x86)\Steam\steamapps\common\SteamVR\drivers\virtualdevice
  13-Aug-2019  08:35:30         <DIR>     bin
   8-Sep-2019  17:47:48         <DIR>     resources
     Directory of z:\Program Files (x86)\Steam\steamapps\common\SteamVR\drivers\virtualdevice\bin
  15-Aug-2019  15:41:36         <DIR>     win64
     Directory of z:\Program Files (x86)\Steam\steamapps\common\SteamVR\drivers\virtualdevice\bin\win64
   9-Sep-2019  06:43:06       1,965,056   driver_virtualdevice.dll
   9-Sep-2019  06:43:06      11,431,936   driver_virtualdevice.pdb
     Directory of z:\Program Files (x86)\Steam\steamapps\common\SteamVR\drivers\virtualdevice\resources
   9-Sep-2019  05:52:08         <DIR>     input
  13-Aug-2019  06:49:20         <DIR>     settings
     Directory of z:\Program Files (x86)\Steam\steamapps\common\SteamVR\drivers\virtualdevice\resources\input
   5-Aug-2019  06:31:14           2,319   virtualdevice_profile.json
     Directory of z:\Program Files (x86)\Steam\steamapps\common\SteamVR\drivers\virtualdevice\resources\settings
  15-Aug-2019  15:41:26             446   default.vrsettings
- The dll/pdb file is created compiling/linking the project OpenVRsim\driver\virtualdevice.sln
- The resource folder (.json and .vrsettings files) is copied from OpenVRsim\driver\resources
#####
At this point, when you start VRMonitor, the virtualdevice should be active and you will see the 'test images' panning
and the handles move in circles.
#####
- Install Python 3.7 or later (3.7.4 was latest 2020-03-15)
- Update pip
python -m pip install --upgrade pip
- Install the wx and zmq modules 
  pip install wxpython
  pip install PyOpenGL PyOpenGL_accelerate
  pip install keyboard
  pip install pyquaternion   
  pip install zmq

- Now start the Python program
  python OpenVRsim.py


