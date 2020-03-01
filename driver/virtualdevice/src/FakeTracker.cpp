#include "FakeTracker.hpp"
#include <cmath>
#include <chrono>
#include <thread>

FakeTracker::FakeTracker() : 
	_pose( {0} )
{
	// Create some random but unique serial
	_serial = "ft_" + std::to_string(std::chrono::system_clock::now().time_since_epoch().count());

	// Set up some defalt rotation pointing down -z
	_pose.qRotation.w = 1.0;
	_pose.qRotation.x = 0.0;
	_pose.qRotation.y = 0.0;
	_pose.qRotation.z = 0.0;

	_pose.qWorldFromDriverRotation.w = 1.0;
	_pose.qWorldFromDriverRotation.x = 0.0;
	_pose.qWorldFromDriverRotation.y = 0.0;
	_pose.qWorldFromDriverRotation.z = 0.0;

	_pose.qDriverFromHeadRotation.w = 1.0;
	_pose.qDriverFromHeadRotation.x = 0.0;
	_pose.qDriverFromHeadRotation.y = 0.0;
	_pose.qDriverFromHeadRotation.z = 0.0;

	// To ensure no complaints about tracking
	_pose.poseIsValid = true;
	_pose.result = vr::ETrackingResult::TrackingResult_Running_OK;
	_pose.deviceIsConnected = true;
}

std::shared_ptr<FakeTracker> FakeTracker::make_new()
{
	return std::shared_ptr<FakeTracker>(new FakeTracker());
}

std::string FakeTracker::get_serial() const
{
	return _serial;
}

void FakeTracker::update()
{
	// Update time delta (for working out velocity)
	std::chrono::milliseconds time_since_epoch = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch());
	double time_since_epoch_seconds = time_since_epoch.count() / 1000.0;
	double pose_time_delta_seconds = (time_since_epoch - _pose_timestamp).count() / 1000.0;

	// Update pose timestamp
	_pose_timestamp = time_since_epoch;

	// Copy the previous position data
	double previous_position[3] = { 0 };
	std::copy(std::begin(_pose.vecPosition), std::end(_pose.vecPosition), std::begin(previous_position));

	// Update the position with our new data
    double d = (_index == 1) ? 0 : .5;
    double t = (_index == 1) ? time_since_epoch_seconds : -time_since_epoch_seconds;
	_pose.vecPosition[0] = px;
	_pose.vecPosition[1] = py;
	_pose.vecPosition[2] = pz;// +2 * std::cos(time_since_epoch_seconds);

	// Update the velocity
	_pose.vecVelocity[0] = (_pose.vecPosition[0] - previous_position[0]) / pose_time_delta_seconds;
	_pose.vecVelocity[1] = (_pose.vecPosition[1] - previous_position[1]) / pose_time_delta_seconds;
	_pose.vecVelocity[2] = (_pose.vecPosition[2] - previous_position[2]) / pose_time_delta_seconds;

	// If we are still tracking, update openvr with our new pose data
	if (_index != vr::k_unTrackedDeviceIndexInvalid)
	{
		vr::VRServerDriverHost()->TrackedDevicePoseUpdated(_index, _pose, sizeof(vr::DriverPose_t));
	}
}

vr::TrackedDeviceIndex_t FakeTracker::get_index() const
{
	return _index;
}

void FakeTracker::process_event(const vr::VREvent_t& event)
{
}

std::string errorcode2string(vr::EVRInputError e)
{
	if (e == vr::VRInputError_None)
		return "VRInputError_None";
	if (e == vr::VRInputError_NameNotFound)
		return "VRInputError_NameNotFound";
	if (e == vr::VRInputError_WrongType)
		return "VRInputError_WrongType";
	if (e == vr::VRInputError_InvalidHandle)
		return "VRInputError_InvalidHandle";
	if (e == vr::VRInputError_InvalidParam)
		return "VRInputError_InvalidParam";
	if (e == vr::VRInputError_NoSteam)
		return "VRInputError_NoSteam";
	if (e == vr::VRInputError_MaxCapacityReached)
		return "VRInputError_MaxCapacityReached";
	if (e == vr::VRInputError_IPCError)
		return "VRInputError_IPCError";
	if (e == vr::VRInputError_NoActiveActionSet)
		return "VRInputError_NoActiveActionSet";
	if (e == vr::VRInputError_InvalidDevice)
		return "VRInputError_InvalidDevice";
	if (e == vr::VRInputError_InvalidSkeleton)
		return "VRInputError_InvalidSkeleton";
	if (e == vr::VRInputError_InvalidBoneCount)
		return "VRInputError_InvalidBoneCount";
	if (e == vr::VRInputError_InvalidCompressedData)
		return "VRInputError_InvalidCompressedData";
	if (e == vr::VRInputError_NoData)
		return "VRInputError_NoData";
	if (e == vr::VRInputError_BufferTooSmall)
		return "VRInputError_BufferTooSmall";
	if (e == vr::VRInputError_MismatchedActionManifest)
		return "VRInputError_MismatchedActionManifest";
	if (e == vr::VRInputError_MissingSkeletonData)
		return "VRInputError_MissingSkeletonData";
	if (e == vr::VRInputError_InvalidBoneIndex)
		return "VRInputError_InvalidBoneIndex";
	return "Unknown Error";
}
std::string FakeTracker::handlecommand(std::string& cmd)
{
	vr::EVRInputError result = vr::VRInputError_InvalidDevice;
	switch (cmd[0]) {
	case 's': // System button
		result = vr::VRDriverInput()->UpdateBooleanComponent(_components._system_click, true, 0.0);
		if (result == 0) {
			std::this_thread::sleep_for(std::chrono::milliseconds(500));
			result = vr::VRDriverInput()->UpdateBooleanComponent(_components._system_click, false, 0.0);
			if (result == 0)
				return "OK";
			else
				return errorcode2string(result);
		}
		break;
	case 't': // Trigger
		return "NYI";
		break;
	}
	return "error";
}

std::string FakeTracker::setpos(double x, double y, double z) {
	px = x; py = y; pz = z;
	return "OK";
}
std::string FakeTracker::setrot(double w, double x, double y, double z) {
	rw = w; rx = x; ry = y; rz = z;
	return "OK";
}

vr::EVRInitError FakeTracker::Activate(vr::TrackedDeviceIndex_t index)
{
	// Save the device index
	_index = index;
	
	// Get the properties handle for our controller
	_props = vr::VRProperties()->TrackedDeviceToPropertyContainer(_index);

	// Set our universe ID
	vr::VRProperties()->SetUint64Property(_props, vr::Prop_CurrentUniverseId_Uint64, 2);

	// Add our controller components. (These are the same as the regular vive controller)
	vr::VRDriverInput()->CreateBooleanComponent(_props, "/input/system/click", &_components._system_click);
	vr::VRDriverInput()->CreateBooleanComponent(_props, "/input/grip/click", &_components._grip_click);
	vr::VRDriverInput()->CreateBooleanComponent(_props, "/input/application_menu/click", &_components._app_click);
	vr::VRDriverInput()->CreateScalarComponent(_props, "/input/trigger/value", &_components._trigger_value, vr::EVRScalarType::VRScalarType_Absolute, vr::EVRScalarUnits::VRScalarUnits_NormalizedOneSided);
	vr::VRDriverInput()->CreateScalarComponent(_props, "/input/trackpad/x", &_components._trackpad_x, vr::EVRScalarType::VRScalarType_Absolute, vr::EVRScalarUnits::VRScalarUnits_NormalizedTwoSided);
	vr::VRDriverInput()->CreateScalarComponent(_props, "/input/trackpad/y", &_components._trackpad_y, vr::EVRScalarType::VRScalarType_Absolute, vr::EVRScalarUnits::VRScalarUnits_NormalizedTwoSided);
	vr::VRDriverInput()->CreateBooleanComponent(_props, "/input/trackpad/click", &_components._trackpad_click);
	vr::VRDriverInput()->CreateBooleanComponent(_props, "/input/trackpad/touch", &_components._trackpad_touch);
	vr::VRDriverInput()->CreateHapticComponent(_props, "/output/haptic", &_components._haptic);

	// Set our controller to use the vive controller render model
	vr::VRProperties()->SetStringProperty(_props, vr::Prop_RenderModelName_String, "arrow");

	return vr::VRInitError_None;
}

void FakeTracker::Deactivate()
{
	// Clear device id
	_index = vr::k_unTrackedDeviceIndexInvalid;
}

void FakeTracker::EnterStandby()
{
}

void * FakeTracker::GetComponent(const char * component)
{
	// No extra components on this device so always return nullptr
	return nullptr;
}

void FakeTracker::DebugRequest(const char * request, char* response_buffer, uint32_t response_buffer_size)
{
	// No custom debug requests defined
	if (response_buffer_size >= 1)
		response_buffer[0] = 0;
}

vr::DriverPose_t FakeTracker::GetPose()
{
	return _pose;
}

void FakeTracker::set_pose(vr::DriverPose_t new_pose)
{
	_pose = new_pose;
}