from edcon.edrive.com_modbus import ComModbus
from edcon.edrive.motion_handler import MotionHandler
from edcon.utils.logging import Logging

# Enable loglevel info
Logging()

com = ComModbus('10.19.96.157') # 10.19.96.158
with MotionHandler(com) as mot:
    mot.acknowledge_faults()
    mot.enable_powerstage()
    mot.referencing_task()

    mot.position_task(300, 50000)
    mot.position_task(-300, 50000)
    # mot.position_task(300000, 600000, absolute=True)
