from edcon.edrive.com_modbus import ComModbus
from edcon.edrive.motion_handler import MotionHandler
from edcon.utils.logging import Logging
import time

address = ['10.19.96.157','10.19.96.158']

class Gantry(address):
    coms = [ComModbus(ip_address=add) for add in address]
    mots = [MotionHandler(com) for com in coms]

    def __init__(self):
        self.coms = [ComModbus(ip_address=add) for add in address]
        self.mots = [MotionHandler(com) for com in self.coms]
        for mot in self.mots:
            mot.acknowledge_faults()
            mot.enable_powerstage()
            if not mot.referenced():
                mot.referencing_task()

    def home(self):
        for mot in self.mots:
            mot.position_task(0, 300, nonblocking=True, absolute=True)
        time.sleep(0.1)
        while True:
            target_positions_reached = [mot.target_position_reached() for mot in self.mots]
            Logging.logger.info(f"Target positions reached: {target_positions_reached}")
            if all(target_positions_reached):
                break
            time.sleep(0.1)


    def move(self, position, velocity):
        for [mot,pos] in zip(self.mots,position):
            mot.position_task(pos, velocity, nonblocking=True, absolute=True)



