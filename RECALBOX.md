#RECALBOX 18.04.20
#python /usr/lib/python2.7/site-packages/configgen/emulatorlauncher.pyc -h
usage: emulatorlauncher.pyc [-h] [-p1index P1INDEX] [-p1guid P1GUID]
                            [-p1name P1NAME] [-p1devicepath P1DEVICEPATH]
                            [-p1nbaxes P1NBAXES] [-p2index P2INDEX]
                            [-p2guid P2GUID] [-p2name P2NAME]
                            [-p2devicepath P2DEVICEPATH] [-p2nbaxes P2NBAXES]
                            [-p3index P3INDEX] [-p3guid P3GUID]
                            [-p3name P3NAME] [-p3devicepath P3DEVICEPATH]
                            [-p3nbaxes P3NBAXES] [-p4index P4INDEX]
                            [-p4guid P4GUID] [-p4name P4NAME]
                            [-p4devicepath P4DEVICEPATH] [-p4nbaxes P4NBAXES]
                            [-p5index P5INDEX] [-p5guid P5GUID]
                            [-p5name P5NAME] [-p5devicepath P5DEVICEPATH]
                            [-p5nbaxes P5NBAXES] -system SYSTEM -rom ROM
                            [-emulator EMULATOR] [-core CORE] [-ratio RATIO]
                            [-demo DEMO] [-netplay NETPLAY]

emulator-launcher script

optional arguments:
  -h, --help            show this help message and exit
  -p1index P1INDEX      player1 controller index
  -p1guid P1GUID        player1 controller SDL2 guid
  -p1name P1NAME        player1 controller name
  -p1devicepath P1DEVICEPATH
                        player1 controller device
  -p1nbaxes P1NBAXES    player1 controller number of axes
  -p2index P2INDEX      player2 controller index
  -p2guid P2GUID        player2 controller SDL2 guid
  -p2name P2NAME        player2 controller name
  -p2devicepath P2DEVICEPATH
                        player2 controller device
  -p2nbaxes P2NBAXES    player2 controller number of axes
  -p3index P3INDEX      player3 controller index
  -p3guid P3GUID        player3 controller SDL2 guid
  -p3name P3NAME        player3 controller name
  -p3devicepath P3DEVICEPATH
                        player3 controller device
  -p3nbaxes P3NBAXES    player3 controller number of axes
  -p4index P4INDEX      player4 controller index
  -p4guid P4GUID        player4 controller SDL2 guid
  -p4name P4NAME        player4 controller name
  -p4devicepath P4DEVICEPATH
                        player4 controller device
  -p4nbaxes P4NBAXES    player4 controller number of axes
  -p5index P5INDEX      player5 controller index
  -p5guid P5GUID        player5 controller SDL2 guid
  -p5name P5NAME        player5 controller name
  -p5devicepath P5DEVICEPATH
                        player5 controller device
  -p5nbaxes P5NBAXES    player5 controller number of axes
  -system SYSTEM        select the system to launch
  -rom ROM              rom absolute path
  -emulator EMULATOR    force emulator
  -core CORE            force emulator core
  -ratio RATIO          force game ratio
  -demo DEMO            mode demo
  -netplay NETPLAY      host/client
#

#RECALBOX 18.06.27
#python /usr/lib/python2.7/site-packages/configgen/emulatorlauncher.pyc -h
usage: emulatorlauncher.pyc [-h] [-p1index P1INDEX] [-p1guid P1GUID]
                            [-p1name P1NAME] [-p1devicepath P1DEVICEPATH]
                            [-p1nbaxes P1NBAXES] [-p2index P2INDEX]
                            [-p2guid P2GUID] [-p2name P2NAME]
                            [-p2devicepath P2DEVICEPATH] [-p2nbaxes P2NBAXES]
                            [-p3index P3INDEX] [-p3guid P3GUID]
                            [-p3name P3NAME] [-p3devicepath P3DEVICEPATH]
                            [-p3nbaxes P3NBAXES] [-p4index P4INDEX]
                            [-p4guid P4GUID] [-p4name P4NAME]
                            [-p4devicepath P4DEVICEPATH] [-p4nbaxes P4NBAXES]
                            [-p5index P5INDEX] [-p5guid P5GUID]
                            [-p5name P5NAME] [-p5devicepath P5DEVICEPATH]
                            [-p5nbaxes P5NBAXES] -system SYSTEM -rom ROM
                            [-emulator EMULATOR] [-core CORE] [-ratio RATIO]
                            [-demo DEMO] [-netplay NETPLAY]
                            [-netplay_ip NETPLAY_IP]
                            [-netplay_port NETPLAY_PORT] [-hash HASH]

emulator-launcher script

optional arguments:
  -h, --help            show this help message and exit
  -p1index P1INDEX      player1 controller index
  -p1guid P1GUID        player1 controller SDL2 guid
  -p1name P1NAME        player1 controller name
  -p1devicepath P1DEVICEPATH
                        player1 controller device
  -p1nbaxes P1NBAXES    player1 controller number of axes
  -p2index P2INDEX      player2 controller index
  -p2guid P2GUID        player2 controller SDL2 guid
  -p2name P2NAME        player2 controller name
  -p2devicepath P2DEVICEPATH
                        player2 controller device
  -p2nbaxes P2NBAXES    player2 controller number of axes
  -p3index P3INDEX      player3 controller index
  -p3guid P3GUID        player3 controller SDL2 guid
  -p3name P3NAME        player3 controller name
  -p3devicepath P3DEVICEPATH
                        player3 controller device
  -p3nbaxes P3NBAXES    player3 controller number of axes
  -p4index P4INDEX      player4 controller index
  -p4guid P4GUID        player4 controller SDL2 guid
  -p4name P4NAME        player4 controller name
  -p4devicepath P4DEVICEPATH
                        player4 controller device
  -p4nbaxes P4NBAXES    player4 controller number of axes
  -p5index P5INDEX      player5 controller index
  -p5guid P5GUID        player5 controller SDL2 guid
  -p5name P5NAME        player5 controller name
  -p5devicepath P5DEVICEPATH
                        player5 controller device
  -p5nbaxes P5NBAXES    player5 controller number of axes
  -system SYSTEM        select the system to launch
  -rom ROM              rom absolute path
  -emulator EMULATOR    force emulator
  -core CORE            force emulator core
  -ratio RATIO          force game ratio
  -demo DEMO            mode demo
  -netplay NETPLAY      host/client
  -netplay_ip NETPLAY_IP
                        host IP
  -netplay_port NETPLAY_PORT
                        host port (not used in client mode)
  -hash HASH            force rom crc
#

#RECALBOX 18.06.27
#Ajout %NETPLAY% dans la ligne de lancement
<command>python /usr/lib/python2.7/site-packages/configgen/emulatorlauncher.pyc %CONTROLLERSCONFIG% -system %SYSTEM% -rom %ROM% -emulator %EMULATOR% -core %CORE% -ratio %RATIO% %NETPLAY%</command>

#Extrait code source SystemData.cpp
command = strreplace(command, "%ROM%", rom);
command = strreplace(command, "%CONTROLLERSCONFIG%", controlersConfig);
command = strreplace(command, "%SYSTEM%", game->metadata.get("system"));
command = strreplace(command, "%BASENAME%", basename);
command = strreplace(command, "%ROM_RAW%", rom_raw);
if (core != "")
{
	command = strreplace(command, "%EMULATOR%", "libretro");
	command = strreplace(command, "%CORE%", core);
}
else
{
	command = strreplace(command, "%EMULATOR%", game->metadata.get("emulator"));
	command = strreplace(command, "%CORE%", game->metadata.get("core"));
}
command = strreplace(command, "%RATIO%", game->metadata.get("ratio"));

if (netplay == "client")
{
	command = strreplace(command, "%NETPLAY%", "-netplay client -netplay_port " + port + " -netplay_ip " + ip);
}
else if (netplay == "host")
{
    std::string hash = game->metadata.get("hash");
    std::string hashcmd = "";
    if (hash != "")
    {
        hashcmd = " -hash " + hash;
    }
	command = strreplace(command, "%NETPLAY%", "-netplay host -netplay_port " + RecalboxConf::getInstance()->get("global.netplay.port") + hashcmd);
}
else
{
	command = strreplace(command, "%NETPLAY%", "");
}


#Debug 18.04.20
echo "ARGS:$@" >>/recalbox/share/system/logs/gamelistlauncher.log

python /usr/lib/python2.7/site-packages/configgen/emulatorlauncher.pyc -p1index 0 -p1guid 030000006d04000018c2000010010000 -p1name Logitech -system snes -rom /recalbox/share/roms/mario/A\ Very\ Super\ Mario\ World.zip -emulator libretro -core snes9x_next -ratio auto

P00:/recalbox/scripts/gamelistpower/trace_arg.sh
P01:-p1index
P02:0
P03:-p1guid
P04:030000006d04000018c2000010010000
P05:-p1name
P06:Logitech Logitech RumblePad 2 USB
P07:-p1nbaxes
P08:4
P09:-p1devicepath
P10:/dev/input/event1
P11:-system
P12:dreamcast
P13:-rom
P14:/recalbox/share/roms/dreamcast_test/Mr. Driller.cdi
P15:-emulator
P16:default
P17:-core
P18:default
P19:-ratio
P20:auto

#es_systems.cfg COLLECTION
	<!--NORDIC POWER-->
  <system>
    <fullname>collections</fullname>
    <name>collections</name>
    <path>/recalbox/share/roms/collections</path>
    <extension>.sh .SH</extension>
    <command>%ROM% %CONTROLLERSCONFIG% %RATIO%</command>
    <platform>dreamcast</platform>
    <theme>favorites</theme>
  </system>

#launcher

#!/bin/sh
RATIO=${@:$#}
set -- "${@:1:$#-1}"
python /usr/lib/python2.7/site-packages/configgen/emulatorlauncher.pyc "$@" -system dreamcast -rom /recalbox/share/roms/dreamcast/Puyo\ Puyo\ Fever.cdi -emulator default -core default -ratio "$RATIO"


