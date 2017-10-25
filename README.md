# sysj-py-comms

Python library to enable communication with SystemJ program.

Packet format can be found at [sysj-ems](https://github.com/hjparker/sysj-ems).

## Running a SystemJ example program in `sysj-ems`

```bash
$ ./gradlew run -Ptarget=rpi_local.xml
```

## Temperature, humidity and light values

Each of these values are 2 bytes long (big-endian), and are computed by the following rules:

- Temperature: `First byte + Second byte / 100` Celcius
- Humidity: `First byte + Second byte / 100` %RH
- Light: `((First byte << 8) + Second byte) * 16` Lux


## Packet types for the `SysJOutput` module
- `0x84` - Temperature, humidity and light.
- `0x30` - Turned on(1) or off(0).
- `0x31` - Instantaneous power (W).