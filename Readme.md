# IOT portal for MQTT home devices

A Vue-based portal for managing home devices running on MQTT. Device autodiscovery out of the box!
The PoC uses mosquitto broker and containerized IoT devices, written in python.

# Support

The portal supports following device types:

* spinners/fans (RPM-based): `rpm` topic suffix
* AC (temperature-based): `temp` topic suffix
* lamps (color temperature-based): `ct` topic suffix
* generic devices with just an on/off switch: : `state` topic suffix

To have your device registered, just pub/sub on MQTT topic: `home/{device_name}/{param}`,
where `{device_name}` is an arbitrary device name and `{param}` is a value from above bullet list.
