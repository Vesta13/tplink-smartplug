# TP-Link WiFi SmartPlug Client

Forked from https://github.com/softScheck/tplink-smartplug
Thank's to softScheck GmbH for this python client

- add nightmode for led
- add return for relay_state 0 on 1 off
- add return for currentRunTime in second
- add return currentTime in HH:MM:SS
- add return for currentPower in w
- add return for voltage in v
- add total current dailyConsumption in kwh
- add resert emeter counter


## tplink-smartplug.py ##

A python client for the proprietary TP-Link Smart Home protocol to control TP-Link HS100 and HS110 WiFi Smart Plugs.
The SmartHome protocol runs on TCP port 9999 and uses a trivial XOR autokey encryption that provides no security. 

There is no authentication mechanism and commands are accepted independent of device state (configured/unconfigured).


Commands are formatted using JSON, for example:

  `{"system":{"get_sysinfo":null}}`

Instead of `null` we can also write `{}`. Commands can be nested, for example:

  `{"system":{"get_sysinfo":null},"time":{"get_time":null}}`

A full list of commands is provided in [tplink-smarthome-commands.txt](tplink-smarthome-commands.txt).


#### Usage ####

   `./tplink-smarthome.py -t <ip> [-c <cmd> || -j <json>]`

Provide the target IP using `-t` and a command to send using either `-c` or `-j`. Commands for the `-c` flag:

| Command            | Description                          |
|--------------------|--------------------------------------|
| on                 | Turns on the plug                    |
| off                | Turns off the plug                   |
| system             | Returns device info                  |
| cloudinfo          | Returns cloud connectivity info      |
| wlanscan           | Scan for nearby access points        |
| time               | Returns the system time              |
| schedule           | Lists configured schedule rules      |
| countdown          | Lists configured countdown rules     |
| antitheft          | Lists configured antitheft rules     |
| reboot             | Reboot the device                    |
| reset              | Reset the device to factory settings |
| relay_state        | 0 off 1 on                           |
| nightmodeon        | Turn on the plug led                 |
| nightmodeoff       | Turn off the plug led                |
| currentRunTime     | return current time in second since  |
|                    | the relay_state is 1                 |
| currentRunTimeHour | return current time in HH:MM:SS      |
|                    | since the relay_state is 1           |
|                    |										|
|currentPower        | return currentPower in w             |
|voltage             | return current Voltage               |
|dailyConsumption    | return current daily consumption Kwh |
|totalConsumption    | return total from last counter reset |
|                    |	consumption Kwh                     |
|resetcounter        | return emeter counter                |


More advanced commands such as creating or editing rules can be issued using the `-j` flag by providing the full JSON string for the command. Please consult [tplink-smarthome-commands.txt](tplink-smarthome-commands.txt) for a comprehensive list of commands.

