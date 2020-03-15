#pragma once

#include <memory>
#include <string>
#include <chrono>
#include <string>
#include <openvr_driver.h>

class FakeTracker : public vr::ITrackedDeviceServerDriver
{
public:
	/// <summary>
	/// Makes a new instance
	/// </summary>
	/// <returns>A new FakeTracker</returns>
	static std::shared_ptr<FakeTracker> make_new();
	virtual ~FakeTracker() = default;

	/// <summary>
	/// Disable move and copy
	/// Because we give the pointer to this to VRServerDriverHost, we dont want it to ever change
	/// </summary>
	FakeTracker(FakeTracker&&) = delete;
	FakeTracker& operator=(FakeTracker&&) = delete;
	FakeTracker(const FakeTracker&) = delete;
	FakeTracker& operator= (const FakeTracker&) = delete;
		
	/// <summary>
	/// Gets this device's serial string
	/// </summary>
	/// <returns>Serial string</returns>
	std::string get_serial() const;

	/// <summary>
	/// Updates the internal state of this device, to be called every time ServerDriver::RunFrame is called
	/// Override this with your custom controller functionality
	/// </summary>
	virtual void update();

	/// <summary>
	/// Gets this devices global(?) index/object id
	/// </summary>
	/// <returns>Index</returns>
	vr::TrackedDeviceIndex_t get_index() const;
	
	/// <summary>
	/// Processes an event
	/// </summary>
	/// <param name="event">The event to be processed</param>
	void process_event(const vr::VREvent_t& event);

	/// <summary>
	/// Activates this device
	/// Is called when vr::VRServerDriverHost()->TrackedDeviceAdded is called
	/// </summary>
	/// <param name="index">The device index</param>
	/// <returns>Error code</returns>
	virtual vr::EVRInitError Activate(vr::TrackedDeviceIndex_t index) override;

	/// <summary>
	/// Deactivates the device
	/// </summary>
	virtual void Deactivate() override;

	/// <summary>
	/// Tells the device to enter stand-by mode
	/// </summary>
	virtual void EnterStandby() override;

	/// <summary>
	/// Gets a specific component from this device
	/// </summary>
	/// <param name="component">Requested component</param>
	/// <returns>Non-owning pointer to the component</returns>
	virtual void* GetComponent(const char* component) override;

	/// <summary>
	/// Handles a debug request
	/// </summary>
	/// <param name="request">Request type</param>
	/// <param name="response_buffer">Response buffer</param>
	/// <param name="response_buffer_size">Response buffer size</param>
	virtual void DebugRequest(const char* request, char* response_buffer, uint32_t response_buffer_size) override;

	/// <summary>
	/// Gets the current device pose
	/// </summary>
	/// <returns>Device Pose</returns>
	virtual vr::DriverPose_t GetPose() override;

	/// <summary>
	/// Sets the current device pose
	/// Note: Be sure to zero initialize the pose struct if you have created a new one
	/// </summary>
	/// <param name="new_pose">New device pose</param>
	virtual void set_pose(vr::DriverPose_t new_pose);
	/// <summary>
	/// Perform a command from outside
	/// </summary>
	/// <param name="new_pose">command string</param>
	std::string FakeTracker::handlecommand(std::string& cmd);
	std::string setpos(double x, double y, double z);
	std::string setrot(double w, double x, double y, double z);

private:
	// Private constructor so the only way to instantiate the class is via the make_new function.
	FakeTracker();

	// Stores the openvr supplied device index.
	vr::TrackedDeviceIndex_t _index;

	// Stores the devices current pose.
	vr::DriverPose_t _pose;

	// Stores the timestamp of the pose.
	std::chrono::milliseconds _pose_timestamp;

	// An identifier for openvr for when we want to make property changes to this device.
	vr::PropertyContainerHandle_t _props;

	// A struct for concise storage of all of the component handles for this device.
	struct TrackerComponents {
		vr::VRInputComponentHandle_t
			_system_click,
			_grip_click,
			_app_click,
			_trigger_value,
			_trackpad_x,
			_trackpad_y,
			_trackpad_click,
			_trackpad_touch,
			_haptic;
		
	};

	int buttonState = 0; // 1:system 2:grip 4:trigger, 8:app
	TrackerComponents _components;

	// Stores the serial for this device. Must be unique.
	std::string _serial;

	// Position and rotation
	double px = 0;
	double py = 0;
	double pz = 0;
	double rw = 0;
	double rx = 0;
	double ry = 0;
	double rz = 0;
};