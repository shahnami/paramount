import tinytuya
import json
from enum import Enum
from pprint import pprint

class DeviceType(Enum):
    BULB = 'dj'
    OUTLET = 'cz'

class TuyaDeviceController:
    def __init__(self, client_id, secret):
        with open('./data/devices.json', 'r') as f:
            devices = json.load(f)
            self.devices = [
                tinytuya.BulbDevice(device['id'], 'Auto', device['key'], version=3.5)
                if device['category'] == DeviceType.BULB.value 
                else tinytuya.OutletDevice(device['id'], 'Auto', device['key'], version=3.3)
                if device['category'] == DeviceType.OUTLET.value
                else None
                for device in devices
                if device['category'] in (DeviceType.BULB.value, DeviceType.OUTLET.value)
            ]
        pprint(self.devices)

    def get_device_type(self, device_index):
        if not (0 <= device_index < len(self.devices)):
            print(f"Invalid device index: {device_index}")
            return
        device = self.devices[device_index]
        return DeviceType.BULB if isinstance(device, tinytuya.BulbDevice) else DeviceType.OUTLET if isinstance(device, tinytuya.OutletDevice) else None

    def control_device(self, device_index, force_state=None):
        print(f"Control device {device_index + 1}, Force state: {force_state}")
        if not (0 <= device_index < len(self.devices)):
            print(f"Invalid device index: {device_index}")
            return
        device = self.devices[device_index]
        # Determine the state to set based on force_state or current state
        if force_state is None:
            if self.get_device_type(device_index) == DeviceType.BULB:
                current_state = device.status().get('dps', {}).get('20', False)
            elif self.get_device_type(device_index) == DeviceType.OUTLET:
                current_state = device.status().get('dps', {}).get('1', False)
            target_state = not current_state
        else:
            target_state = force_state
        # Set the device state
        if target_state:
            device.turn_on()
        else:
            device.turn_off()
        print(f"Device {device_index + 1} is now {'on' if target_state else 'off'}")

    def control_all(self, state):
        print("control_all", state)
        for index, device in enumerate(self.devices):
            self.control_device(index, state)