import os
import PySpin
import matplotlib.pyplot as plt
import sys
import keyboard
import time


class FlirCamController:
    def __init__(self):
        # Flag representing the status of the continue mode
        self.flag_continue = False

        self.frame = []

        # Retrieve singleton reference to system object
        self.system = PySpin.System.GetInstance()

        # Get current library version
        version = self.system.GetLibraryVersion()
        print('Library version: %d.%d.%d.%d' % (version.major, version.minor, version.type, version.build))

        # Retrieve list of cameras from the system
        self.cam_list = self.system.GetCameras()

        num_cameras = self.cam_list.GetSize()

        print('Number of cameras detected: %d' % num_cameras)

        if num_cameras == 0:
            # Finish if there are no cameras
            self.close()
            print('Not enough cameras!')
        else:
            # Choose the first camera
            self.cam = self.cam_list[0]

            # Initialize camera
            self.cam.Init()

    def close(self):
        # Release reference to camera
        # NOTE: Unlike the C++ examples, we cannot rely on pointer objects being automatically
        # cleaned up when going out of scope.
        # The usage of del is preferred to assigning the variable to None.
        if hasattr(self, 'cam'):
            self.cam.DeInit()
            del self.cam
        # Clear camera list before releasing system
        self.cam_list.Clear()

        # Release system instance
        self.system.ReleaseInstance()
        print('Camera closed...')

    def start_continue(self):
        # :param cam: Camera to run on.
        # :type cam: CameraPtr
        # :return: True if successful, False otherwise.
        # :rtype: bool
        if self.flag_continue:
            print('Acquisition already started...')
            return
        
        try:
            result = True

            nodemap_tldevice = self.cam.GetTLDeviceNodeMap()

            # Retrieve GenICam nodemap
            nodemap = self.cam.GetNodeMap()

            sNodemap = self.cam.GetTLStreamNodeMap()

            # Change bufferhandling mode to NewestOnly
            node_bufferhandling_mode = PySpin.CEnumerationPtr(sNodemap.GetNode('StreamBufferHandlingMode'))
            if not PySpin.IsAvailable(node_bufferhandling_mode) or not PySpin.IsWritable(node_bufferhandling_mode):
                print('Unable to set stream buffer handling mode.. Aborting...')
                return False

            # Retrieve entry node from enumeration node
            node_newestonly = node_bufferhandling_mode.GetEntryByName('NewestOnly')
            if not PySpin.IsAvailable(node_newestonly) or not PySpin.IsReadable(node_newestonly):
                print('Unable to set stream buffer handling mode.. Aborting...')
                return False

            # Retrieve integer value from entry node
            node_newestonly_mode = node_newestonly.GetValue()

            # Set integer value from entry node as new value of enumeration node
            node_bufferhandling_mode.SetIntValue(node_newestonly_mode)

            node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
            if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
                print('Unable to set acquisition mode to continuous (enum retrieval). Aborting...')
                return False

            # Retrieve entry node from enumeration node
            node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
            if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(
                    node_acquisition_mode_continuous):
                print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
                return False

            # Retrieve integer value from entry node
            acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()

            # Set integer value from entry node as new value of enumeration node
            node_acquisition_mode.SetIntValue(acquisition_mode_continuous)

            print('Acquisition mode set to continuous...')

            #  Begin acquiring images
            #
            #  *** NOTES ***
            #  What happens when the camera begins acquiring images depends on the
            #  acquisition mode. Single frame captures only a single image, multi
            #  frame catures a set number of images, and continuous captures a
            #  continuous stream of images.
            #
            #  *** LATER ***
            #  Image acquisition must be ended when no more images are needed.
            self.cam.BeginAcquisition()
            self.flag_continue = True

            print('Acquiring images...')

            #  Retrieve device serial number for filename
            #
            #  *** NOTES ***
            #  The device serial number is retrieved in order to keep cameras from
            #  overwriting one another. Grabbing image IDs could also accomplish
            #  this.
            device_serial_number = ''
            node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
            if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
                device_serial_number = node_device_serial_number.GetValue()
                print('Device serial number retrieved as %s...' % device_serial_number)



        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False

        return result

    def stop_continue(self):
        #  End acquisition
        #
        #  *** NOTES ***
        #  Ending acquisition appropriately helps ensure that devices clean up
        #  properly and do not need to be power-cycled to maintain integrity.
        if self.flag_continue:
            self.flag_continue = False
            self.cam.EndAcquisition()
            print('Stop acquiring images...')
        else:
            print('Acquiring already stopped...')

    def acquire_continue(self):
        image_data = []
        image_result = self.cam.GetNextImage(10000)  # GetNextImage( grabTimeout )

        #  Ensure image completion
        if image_result.IsIncomplete():
            print('Image incomplete with image status %d ...' % image_result.GetImageStatus())

        else:
            # Getting the image data as a numpy array
            image_data = image_result.GetNDArray()
            self.frame = image_data

        #  Release image
        #
        #  *** NOTES ***
        #  Images retrieved directly from the camera (i.e. non-converted
        #  images) need to be released in order to keep from filling the
        #  buffer.
        image_result.Release()

        return image_data

    def configure_exposure(self,exposure_time_to_set):
        """
         This function configures a custom exposure time. Automatic exposure is turned
         off in order to allow for the customization, and then the custom setting is
         applied.

         :param cam: Camera to configure exposure for.
         :type cam: CameraPtr
         :return: True if successful, False otherwise.
         :rtype: bool
        """

        print('*** CONFIGURING EXPOSURE ***\n')

        try:
            result = True

            # Turn off automatic exposure mode
            #
            # *** NOTES ***
            # Automatic exposure prevents the manual configuration of exposure
            # times and needs to be turned off for this example. Enumerations
            # representing entry nodes have been added to QuickSpin. This allows
            # for the much easier setting of enumeration nodes to new values.
            #
            # The naming convention of QuickSpin enums is the name of the
            # enumeration node followed by an underscore and the symbolic of
            # the entry node. Selecting "Off" on the "ExposureAuto" node is
            # thus named "ExposureAuto_Off".
            #
            # *** LATER ***
            # Exposure time can be set automatically or manually as needed. This
            # example turns automatic exposure off to set it manually and back
            # on to return the camera to its default state.

            if self.cam.ExposureAuto.GetAccessMode() != PySpin.RW:
                print('Unable to disable automatic exposure. Aborting...')
                return False

            self.cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
            print('Automatic exposure disabled...')

            # Set exposure time manually; exposure time recorded in microseconds
            #
            # *** NOTES ***
            # Notice that the node is checked for availability and writability
            # prior to the setting of the node. In QuickSpin, availability and
            # writability are ensured by checking the access mode.
            #
            # Further, it is ensured that the desired exposure time does not exceed
            # the maximum. Exposure time is counted in microseconds - this can be
            # found out either by retrieving the unit with the GetUnit() method or
            # by checking SpinView.

            if self.cam.ExposureTime.GetAccessMode() != PySpin.RW:
                print('Unable to set exposure time. Aborting...')
                return False

            # Ensure desired exposure time does not exceed the maximum
            print(self.cam.ExposureTime.GetMax())
            print(self.cam.ExposureTime.GetMin())
            exposure_time_to_set = min(self.cam.ExposureTime.GetMax(), exposure_time_to_set)
            exposure_time_to_set = max(self.cam.ExposureTime.GetMin(), exposure_time_to_set)
            self.cam.ExposureTime.SetValue(exposure_time_to_set)
            print('Exposure time set to %s us...\n' % exposure_time_to_set)

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False

        return result


if __name__ == '__main__':
    flir = FlirCamController()
    flir.start_continue()
    flir.acquire_continue()
    flir.acquire_continue()
    flir.acquire_continue()
    plt.imshow(flir.frame)
    plt.show()
    flir.stop_continue()
    flir.close()