
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


********************************************************************************************
Installation of Steam, SteamVR and the driver
- Install Steam  https://store.steampowered.com/about/
- In Steam, login to your account, get one if you don't have
- In Steam, search for SteamVR and install it
- To start SteamVR you can go through the list of installed apps in Steam
OR just start VRmonitor (c:prog\Steam\steamapps\common\SteamVR\bin\win64)
- To install the driver:
In this folder (git repo) locate
driver\copy2SteamVR_drivers\virtualdevice
Copy this folder to
c:\Program Files (x86)\Steam\steamapps\common\SteamVR\drivers\

At this point, when you start VRMonitor, the virtualdevice should be active and you will see the 
SteamVR default landscape and the two hand controllers
********************************************************************************************
A Python program has been developed to give commands to the virtualdevice driver.
- HMD and controllers can be moved and rotated
- Test Cases can be programmed 
To use this progam you have to install the Python interpreter and some add-ons

- Install Python 3.7 or later (3.7.4 was latest 2020-03-15)
- Update pip
python -m pip install --upgrade pip
- Install the needed modules 
  pip install wxpython
  pip install PyOpenGL PyOpenGL_accelerate
  pip install keyboard
  pip install pyquaternion   
  pip install zmq

- Now start the Python program (in the python folder)
  python OpenVRsim.py

********************************************************************************************
For development/debugging the virtualdevice driver:
The driver is developed in c++ using Visual Studio 2019
 
1. Compile and link the .dll in the project OpenVRsim\driver\virtualdevice.sln; for debugging use Solution Config: Debug
2. copy the dll and pdb to c:prog\Steam\steamapps\common\SteamVR\drivers\virtualdevice\bin\win64"
(there is a cp.bat in the driver folder to do this)
3a. To debug the init of the driver, open ...\steamapps\common\SteamVR\bin\win64\vrserver.exe
    in VS2013. As command line args give '--keepalive --earlyload' 
3b. To debug the driver, start openVR and attach a debugger to vrserver.exe

Sometimes you get problem to restart SteamVR. It is resolved by killing the VR Server process in the Task Manager
(under background processes)

