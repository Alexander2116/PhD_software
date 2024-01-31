from pyFAI import detectors
from collections import OrderedDict


detector = detectors.Detector()
dic = detector.registry
print(dic)

"""
Possible detectors to try:
    Fairchild(); Apex2; 
"""

# Modified Source Code
class Breeze(detectors.Detector):
    """BrukerApex2 detector

    Actually a derivative from the Fairchild detector with higher binning
    """
    MANUFACTURER = "Bruker"

    aliases = ["Breeze", "Bruker"]
    force_pixel = True
    MAX_SHAPE = (4096, 4096)
    DEFAULT_PIXEL1 = DEFAULT_PIXEL2 = 15e-6

    def __init__(self, pixel1=120e-6, pixel2=120e-6):
        """Defaults to 2x2 binning
        """
        super(Breeze, self).__init__(pixel1=pixel1, pixel2=pixel2)
        if (pixel1 != self.DEFAULT_PIXEL1) or (pixel2 != self.DEFAULT_PIXEL2):
            self._binning = (int(round(pixel1 / self.DEFAULT_PIXEL1)),
                             int(round(pixel2 / self.DEFAULT_PIXEL2)))
            self.shape = tuple(s // b for s, b in zip(self.MAX_SHAPE, self._binning))

    def __repr__(self):
        return "Detector %s\t PixelSize= %.3e, %.3e m" % \
            (self.name, self._pixel1, self._pixel2)

    def get_config(self):
        """Return the configuration with arguments to the constructor

        :return: dict with param for serialization
        """
        return OrderedDict((("pixel1", self._pixel1),
                            ("pixel2", self._pixel2)))


br = Breeze(15e-6,15e-6) ## Hopeful good pixel size