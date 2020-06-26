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
        self.flag_continue = False
        self.cam.EndAcquisition()
        print('Stop acquiring images...')

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