# Tapo D235 Doorbell for Home Assistant

A HACS custom integration for the **Tapo D235** video doorbell. It connects locally through
[`python-kasa`](https://github.com/python-kasa/python-kasa), using the D235 support branch from
[python-kasa PR #1678](https://github.com/python-kasa/python-kasa/pull/1678).

## What it exposes

Entities are generated from the features that the installed `python-kasa` version reports, so the
integration does not pretend to support controls the device does not actually offer. With the D235
fixture from PR #1678, this includes:

- RTSP camera stream (after RTSP is enabled in the Tapo app)
- Camera on/off (privacy mask)
- Status LED
- Motion, person, pet, and vehicle-detection switches when enabled by the doorbell firmware
- Battery level, low-battery, charging, and any other reported read-only sensors
- Every further `python-kasa` switch, number, select, button, binary sensor, and sensor feature

The D235 firmware also advertises ring/chime, quick-response, package detection, audio,
night-vision, and recording APIs. PR #1678 adds D235 data/support recognition but does **not**
implement those APIs in `python-kasa`; they cannot safely be exposed until the library adds them.

## Install

1. Add this repository as a custom repository in HACS (category: **Integration**) and install it.
2. Restart Home Assistant.
3. Go to **Settings → Devices & services → Add integration** and add **Tapo D235 Doorbell**.
4. Enter the doorbell's stable IP address and its local Tapo Camera Account credentials.
5. Enable RTSP in the Tapo app if you want the camera entity. If you use a different RTSP Camera
   Account, provide it in the optional fields.

The integration is local-polling (30 seconds) and requires no cloud access after setup.

## Notes and limitations

- Give the doorbell a DHCP reservation. Changing its IP requires reconfiguring the integration.
- The camera entity uses `rtsp://<doorbell>:554/stream1`; Home Assistant's Stream integration must
  be available (it is built in) and RTSP must be enabled on the doorbell.
- This is deliberately a separate `tapo_d235` integration; it does not replace or modify Home
  Assistant's built-in TP-Link integration.
- The dependency is pinned to the exact PR branch head so that D235 support is reproducible.
  Update the pin after upstream `python-kasa` support is released and tested.

## Development

The generic entity mapping is in `custom_components/tapo_d235/entity.py`. It maps the library's
feature types as follows: `Sensor`, `BinarySensor`, `Switch`, `Number`, `Choice`, and `Action` to
Home Assistant sensor, binary-sensor, switch, number, select, and button entities respectively.

