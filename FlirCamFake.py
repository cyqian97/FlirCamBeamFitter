import PySpin
from fitgauss import gauss2d
from numpy import zeros, uint8
import numpy as np

class FakeCam:
    def ExposureTime(self):
        return 10


class FakeCamContoller:
    def __init__(self):
        # Flag representing the status of the continue mode
        self.flag_continue = False
        self.framewidth = 0
        self.frameheight = 0
        self.frame = []
        self.background = []
        self.nobackground = []
        self.framecount = 0
        self.exposuretimeupperlimit = 1000000
        self.average_frames = 0
        self.cam_init_setting()

    def cam_init_setting(self):

        result = True

        # set frame size after binning
        self.framewidth = 2000
        self.frameheight = 1500
        self.frame = zeros((self.frameheight, self.framewidth), dtype=uint8)
        self.background = zeros((self.frameheight, self.framewidth), dtype=uint8)
        self.nobackground = zeros((self.frameheight, self.framewidth), dtype=uint8)
        self.floatzeroframe = zeros((self.frameheight, self.framewidth))



    def close(self):
        print('Camera closed...')

    def start_continue(self):
        # :param cam: Camera to run on.
        # :type cam: CameraPtr
        # :return: True if successful, False otherwise.
        # :rtype: bool
        if self.flag_continue:
            print('Acquisition already started...')
            return

        self.flag_continue = True
        print('Acquiring images...')

        return True

    def stop_continue(self):
        #  End acquisition
        #
        #  *** NOTES ***
        #  Ending acquisition appropriately helps ensure that devices clean up
        #  properly and do not need to be power-cycled to maintain integrity.
        if self.flag_continue:
            self.flag_continue = False
            print('Stop acquiring images...')
        else:
            print('Acquiring already stopped...')
        return True

    def acquire_continue(self):
        xx, yy = np.meshgrid(np.arange(self.framewidth), np.arange(self.frameheight))
        image_data = (gauss2d(500, 800, 100, 400, 1, 0, xx, yy) + 1 + np.random.rand(*(xx.shape)) * 0.5)*50
        if self.average_frames > 1:
            image_data = image_data/self.average_frames
            for i in range(self.average_frames - 1):
                image_data += ((gauss2d(500, 800, 100, 400, 1, 0, xx, yy) + 1 + np.random.rand(*(xx.shape)) * 0.5)*50) / self.average_frames

        image_data = image_data.astype(np.uint8)
        self.frame = image_data
        self.framecount += 1

        return image_data

    def configure_exposure(self,exposure_time_to_set):
        print('*** CONFIGURING EXPOSURE ***\n')

        try:
            result = True
            print('Exposure time set to %s us...\n' % 10)

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False

        return result

    def reset_exposure(self):
        print('Automatic exposure enabled...')

        return True

    def get_exposure(self):
        return 10

    def set_background(self):
        self.background = self.frame

    def clear_background(self):
        self.background = self.nobackground


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    flir = FakeCamContoller()
    flir.start_continue()
    flir.acquire_continue()
    flir.acquire_continue()
    flir.acquire_continue()
    print(flir.frame.shape)
    plt.imshow(flir.frame)
    plt.show()
    flir.stop_continue()
    flir.close()