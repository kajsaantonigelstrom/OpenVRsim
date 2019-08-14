# OpenVRsim
Null driver for openVR (HMD&amp;2controllers) that can be controlled by a Python client

The client is developed using Python 2.7.
Need extra modules:
- wx
- zmq 

The driver is based on the sample example in the openVR SDK.
It installs a HMD and two handles. The movements of these three devices 
will be possible to control from the outside using a socket interface (ZeroMQ)
The purpose is to create a test environment when you do not have an actual HMD available

The driver is developed in c++ using Visual Studio 2019
 