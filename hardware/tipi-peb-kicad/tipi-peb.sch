EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:tipebedge
LIBS:tipi-peb-cache
EELAYER 25 0
EELAYER END
$Descr B 17000 11000
encoding utf-8
Sheet 1 1
Title "TIPI PEB - TI-99/4A to RPi adapter"
Date "2017-10-15"
Rev "0"
Comp "ti994a.cwfk.net"
Comment1 "github.com/jedimatt42/tipi"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L GND #PWR01
U 1 1 5917F66C
P 14000 3300
F 0 "#PWR01" H 14000 3050 50  0001 C CNN
F 1 "GND" H 14000 3150 50  0000 C CNN
F 2 "" H 14000 3300 50  0001 C CNN
F 3 "" H 14000 3300 50  0001 C CNN
	1    14000 3300
	1    0    0    -1  
$EndComp
$Comp
L 27C256 U2
U 1 1 5917F7B0
P 2050 2100
F 0 "U2" H 1900 3100 50  0000 C CNN
F 1 "27C256" H 2050 1100 50  0000 C CNN
F 2 "Housings_DIP:DIP-28_W15.24mm_Socket" H 2050 2100 50  0001 C CNN
F 3 "" H 2050 2100 50  0001 C CNN
	1    2050 2100
	1    0    0    -1  
$EndComp
$Comp
L 74LS245 U7
U 1 1 5917F86D
P 10250 9400
F 0 "U7" H 10350 9975 50  0000 L BNN
F 1 "74HCT245" H 10300 8825 50  0000 L TNN
F 2 "SMD_Packages:SSOP-20" H 10250 9400 50  0001 C CNN
F 3 "" H 10250 9400 50  0001 C CNN
	1    10250 9400
	1    0    0    -1  
$EndComp
$Comp
L C_Small C9
U 1 1 5917FDFE
P 8500 850
F 0 "C9" H 8510 920 50  0000 L CNN
F 1 "0.1uf" H 8510 770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 8500 850 50  0001 C CNN
F 3 "" H 8500 850 50  0001 C CNN
	1    8500 850 
	1    0    0    -1  
$EndComp
Text GLabel 10950 9200 2    60   BiDi ~ 0
TI_D0
Text GLabel 10950 9100 2    60   BiDi ~ 0
TI_D1
Text GLabel 10950 9000 2    60   BiDi ~ 0
TI_D2
Text GLabel 10950 8900 2    60   BiDi ~ 0
TI_D3
Text GLabel 10950 9400 2    60   BiDi ~ 0
TI_D4
Text GLabel 10950 9300 2    60   BiDi ~ 0
TI_D5
Text GLabel 10950 9500 2    60   BiDi ~ 0
TI_D6
Text GLabel 10950 9600 2    60   BiDi ~ 0
TI_D7
Text GLabel 14150 3000 0    60   Output ~ 0
R_LE
Text GLabel 14150 2800 0    60   Output ~ 0
R_CLK
Text GLabel 14650 3000 2    60   Output ~ 0
R_DOUT
Text GLabel 14650 3100 2    60   Input ~ 0
R_DIN
Text GLabel 14150 2900 0    60   Output ~ 0
R_RT
Text GLabel 14650 3200 2    60   Output ~ 0
R_DC
Text GLabel 14150 3100 0    60   Input ~ 0
R_RESET
Text GLabel 7350 3200 0    60   Output ~ 0
R_RESET
Text GLabel 7350 3100 0    60   Input ~ 0
R_DC
Text GLabel 7350 3600 0    60   Input ~ 0
R_RT
Text GLabel 7350 3300 0    60   Output ~ 0
R_DIN
Text GLabel 7350 3500 0    60   Input ~ 0
R_DOUT
Text GLabel 7350 2700 0    60   Input ~ 0
R_CLK
Text GLabel 7350 3400 0    60   Input ~ 0
R_LE
Text GLabel 9750 4100 2    60   Output ~ 0
LED0
Text GLabel 9750 6400 2    60   Input ~ 0
JTAG_TCK
Text GLabel 9750 6200 2    60   Input ~ 0
JTAG_TDI
Text GLabel 9750 6500 2    60   Output ~ 0
JTAG_TDO
Text GLabel 9750 6300 2    60   Input ~ 0
JTAG_TMS
$Comp
L AVR-JTAG-10 JTAG1
U 1 1 591AA716
P 14650 1500
F 0 "JTAG1" H 14480 1830 50  0000 C CNN
F 1 "AVR-JTAG-10" H 14310 1170 50  0000 L BNN
F 2 "Pin_Headers:Pin_Header_Straight_2x05_Pitch2.54mm" V 14080 1520 50  0001 C CNN
F 3 "" H 14650 1500 50  0001 C CNN
	1    14650 1500
	1    0    0    -1  
$EndComp
Text GLabel 13850 1300 0    60   Output ~ 0
JTAG_TCK
Text GLabel 13900 1400 0    60   Input ~ 0
JTAG_TDO
Text GLabel 13850 1500 0    60   Output ~ 0
JTAG_TMS
Text GLabel 13850 1700 0    60   Output ~ 0
JTAG_TDI
$Comp
L +3.3V #PWR02
U 1 1 591AACD3
P 15100 1400
F 0 "#PWR02" H 15100 1250 50  0001 C CNN
F 1 "+3.3V" H 15100 1540 50  0000 C CNN
F 2 "" H 15100 1400 50  0001 C CNN
F 3 "" H 15100 1400 50  0001 C CNN
	1    15100 1400
	0    1    1    0   
$EndComp
$Comp
L GND #PWR03
U 1 1 591AACFB
P 15100 1300
F 0 "#PWR03" H 15100 1050 50  0001 C CNN
F 1 "GND" H 15100 1150 50  0000 C CNN
F 2 "" H 15100 1300 50  0001 C CNN
F 3 "" H 15100 1300 50  0001 C CNN
	1    15100 1300
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR04
U 1 1 591AAD23
P 15100 1700
F 0 "#PWR04" H 15100 1450 50  0001 C CNN
F 1 "GND" H 15100 1550 50  0000 C CNN
F 2 "" H 15100 1700 50  0001 C CNN
F 3 "" H 15100 1700 50  0001 C CNN
	1    15100 1700
	1    0    0    -1  
$EndComp
Text GLabel 7350 6000 0    60   Input ~ 0
B_A0
Text GLabel 7350 5900 0    60   Input ~ 0
B_A1
Text GLabel 7350 5600 0    60   Input ~ 0
B_A2
Text GLabel 9750 3500 2    60   Input ~ 0
B_A3
Text GLabel 9750 3400 2    60   Input ~ 0
B_A4
Text GLabel 9750 3200 2    60   Input ~ 0
B_A5
Text GLabel 7350 5800 0    60   Input ~ 0
B_A6
Text GLabel 7350 5300 0    60   Input ~ 0
B_A7
Text GLabel 9750 3800 2    60   Input ~ 0
B_A8
Text GLabel 7350 5400 0    60   Input ~ 0
B_A9
Text GLabel 9750 3100 2    60   Input ~ 0
B_A10
Text GLabel 9750 3300 2    60   Input ~ 0
B_A11
Text GLabel 9750 3700 2    60   Input ~ 0
B_A12
Text GLabel 7350 5100 0    60   Input ~ 0
B_A13
Text GLabel 7350 5200 0    60   Input ~ 0
B_A14
Text GLabel 7350 5500 0    60   Input ~ 0
B_A15
Text GLabel 7350 5700 0    60   Input ~ 0
B_WE
Text GLabel 2450 9650 2    60   Output ~ 0
B_MEMEN
Text GLabel 9750 3600 2    60   Input ~ 0
B_DBIN
Text GLabel 7350 4000 0    60   Input ~ 0
B_CRUCLK
Text GLabel 1350 1200 0    60   Input ~ 0
B_A15
Text GLabel 1350 1300 0    60   Input ~ 0
B_A14
Text GLabel 1350 1400 0    60   Input ~ 0
B_A13
Text GLabel 1350 1500 0    60   Input ~ 0
B_A12
Text GLabel 1350 1600 0    60   Input ~ 0
B_A11
Text GLabel 1350 1700 0    60   Input ~ 0
B_A10
Text GLabel 1350 1800 0    60   Input ~ 0
B_A9
Text GLabel 1350 1900 0    60   Input ~ 0
B_A8
Text GLabel 1350 2100 0    60   Input ~ 0
B_A6
Text GLabel 1350 2000 0    60   Input ~ 0
B_A7
Text GLabel 1350 2200 0    60   Input ~ 0
B_A5
Text GLabel 1350 2300 0    60   Input ~ 0
B_A4
Text GLabel 1350 2400 0    60   Input ~ 0
B_A3
Text GLabel 1350 2500 0    60   Input ~ 0
DSR_B0
Text GLabel 1350 2600 0    60   Input ~ 0
DSR_B1
Text GLabel 2750 1200 2    60   3State ~ 0
TP_D0
Text GLabel 2750 1300 2    60   3State ~ 0
TP_D1
Text GLabel 2750 1400 2    60   3State ~ 0
TP_D2
Text GLabel 2750 1500 2    60   3State ~ 0
TP_D3
Text GLabel 2750 1600 2    60   3State ~ 0
TP_D4
Text GLabel 2750 1700 2    60   3State ~ 0
TP_D5
Text GLabel 2750 1800 2    60   3State ~ 0
TP_D6
Text GLabel 2750 1900 2    60   3State ~ 0
TP_D7
Text GLabel 7350 1700 0    60   3State ~ 0
TP_D0
Text GLabel 7350 1800 0    60   3State ~ 0
TP_D1
Text GLabel 7350 1900 0    60   3State ~ 0
TP_D2
Text GLabel 7350 2100 0    60   3State ~ 0
TP_D3
Text GLabel 7350 2000 0    60   3State ~ 0
TP_D4
Text GLabel 7350 2200 0    60   3State ~ 0
TP_D5
Text GLabel 7350 2300 0    60   3State ~ 0
TP_D6
Text GLabel 7350 2400 0    60   3State ~ 0
TP_D7
Text GLabel 9550 9600 0    60   3State ~ 0
TP_D0
Text GLabel 9550 9500 0    60   3State ~ 0
TP_D1
Text GLabel 9550 9300 0    60   3State ~ 0
TP_D2
Text GLabel 9550 9400 0    60   3State ~ 0
TP_D3
Text GLabel 9550 8900 0    60   3State ~ 0
TP_D4
Text GLabel 9550 9000 0    60   3State ~ 0
TP_D5
Text GLabel 9550 9100 0    60   3State ~ 0
TP_D6
Text GLabel 9550 9200 0    60   3State ~ 0
TP_D7
$Comp
L +5V #PWR05
U 1 1 594E090D
P 1000 2700
F 0 "#PWR05" H 1000 2550 50  0001 C CNN
F 1 "+5V" H 1000 2840 50  0000 C CNN
F 2 "" H 1000 2700 50  0001 C CNN
F 3 "" H 1000 2700 50  0001 C CNN
	1    1000 2700
	-1   0    0    1   
$EndComp
Text GLabel 1250 3000 0    60   Input ~ 0
DSR_EN
Text GLabel 9750 4900 2    60   Output ~ 0
DSR_EN
Text GLabel 9750 1700 2    60   Output ~ 0
DB_EN
Text GLabel 7350 4800 0    60   Output ~ 0
DB_DIR
Text GLabel 9550 9800 0    60   Input ~ 0
DB_DIR
Text GLabel 9550 9900 0    60   Input ~ 0
DB_EN
Text GLabel 7350 4500 0    60   Output ~ 0
DSR_B0
Text GLabel 7350 4600 0    60   Output ~ 0
DSR_B1
Text GLabel 7350 3000 0    60   Output ~ 0
TI_CRUIN
$Comp
L LM1117-3.3 U8
U 1 1 594EAE75
P 14450 4250
F 0 "U8" H 14550 4000 50  0000 C CNN
F 1 "LM1117-3.3" H 14450 4500 50  0000 C CNN
F 2 "TO_SOT_Packages_SMD:SOT-223" H 14450 4250 50  0001 C CNN
F 3 "" H 14450 4250 50  0001 C CNN
	1    14450 4250
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR06
U 1 1 594EAFBA
P 14450 4550
F 0 "#PWR06" H 14450 4300 50  0001 C CNN
F 1 "GND" H 14450 4400 50  0000 C CNN
F 2 "" H 14450 4550 50  0001 C CNN
F 3 "" H 14450 4550 50  0001 C CNN
	1    14450 4550
	1    0    0    -1  
$EndComp
$Comp
L CP1_Small C16
U 1 1 594EB02A
P 14850 4350
F 0 "C16" H 14860 4420 50  0000 L CNN
F 1 "22uf" H 14860 4270 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 14850 4350 50  0001 C CNN
F 3 "" H 14850 4350 50  0001 C CNN
	1    14850 4350
	1    0    0    -1  
$EndComp
$Comp
L CP1_Small C14
U 1 1 594EB077
P 14050 4350
F 0 "C14" H 14060 4420 50  0000 L CNN
F 1 "10uf" H 14060 4270 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 14050 4350 50  0001 C CNN
F 3 "" H 14050 4350 50  0001 C CNN
	1    14050 4350
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR07
U 1 1 594EB46B
P 15000 4250
F 0 "#PWR07" H 15000 4100 50  0001 C CNN
F 1 "+3.3V" H 15000 4390 50  0000 C CNN
F 2 "" H 15000 4250 50  0001 C CNN
F 3 "" H 15000 4250 50  0001 C CNN
	1    15000 4250
	0    1    1    0   
$EndComp
$Comp
L LED_ALT D1
U 1 1 594FDAB3
P 12350 1200
F 0 "D1" H 12350 1300 50  0000 C CNN
F 1 "LED_ALT" H 12350 1100 50  0000 C CNN
F 2 "LEDs:LED_D3.0mm" H 12350 1200 50  0001 C CNN
F 3 "" H 12350 1200 50  0001 C CNN
	1    12350 1200
	1    0    0    -1  
$EndComp
$Comp
L R R6
U 1 1 594FDB4A
P 12750 1200
F 0 "R6" V 12830 1200 50  0000 C CNN
F 1 "330" V 12750 1200 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 12680 1200 50  0001 C CNN
F 3 "" H 12750 1200 50  0001 C CNN
	1    12750 1200
	0    1    1    0   
$EndComp
$Comp
L +5V #PWR08
U 1 1 594FDBD5
P 13000 1200
F 0 "#PWR08" H 13000 1050 50  0001 C CNN
F 1 "+5V" H 13000 1340 50  0000 C CNN
F 2 "" H 13000 1200 50  0001 C CNN
F 3 "" H 13000 1200 50  0001 C CNN
	1    13000 1200
	-1   0    0    1   
$EndComp
$Comp
L R R5
U 1 1 594FDDEA
P 11650 900
F 0 "R5" V 11730 900 50  0000 C CNN
F 1 "1k" V 11650 900 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 11580 900 50  0001 C CNN
F 3 "" H 11650 900 50  0001 C CNN
	1    11650 900 
	0    1    1    0   
$EndComp
$Comp
L Q_NPN_BCE Q1
U 1 1 594FDE57
P 11900 1100
F 0 "Q1" H 12100 1150 50  0000 L CNN
F 1 "Q_NPN_BCE" H 12100 1050 50  0000 L CNN
F 2 "TO_SOT_Packages_SMD:SOT-23" H 12100 1200 50  0001 C CNN
F 3 "" H 11900 1100 50  0001 C CNN
	1    11900 1100
	0    1    1    0   
$EndComp
$Comp
L GND #PWR09
U 1 1 594FDF4A
P 11600 1200
F 0 "#PWR09" H 11600 950 50  0001 C CNN
F 1 "GND" H 11600 1050 50  0000 C CNN
F 2 "" H 11600 1200 50  0001 C CNN
F 3 "" H 11600 1200 50  0001 C CNN
	1    11600 1200
	1    0    0    -1  
$EndComp
Text GLabel 11400 900  0    60   Input ~ 0
LED0
$Comp
L Conn_02x04_Counter_Clockwise CRUBASE1
U 1 1 594FE925
P 11800 2350
F 0 "CRUBASE1" H 11800 2600 50  0000 C CNN
F 1 "CONN_02X04" H 11800 2100 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x04_Pitch2.54mm" H 11800 1150 50  0001 C CNN
F 3 "" H 11800 1150 50  0001 C CNN
	1    11800 2350
	1    0    0    -1  
$EndComp
Text GLabel 12100 2250 2    60   Output ~ 0
CRUB_0
Text GLabel 12100 2350 2    60   Output ~ 0
CRUB_1
Text GLabel 12100 2450 2    60   Output ~ 0
CRUB_2
Text GLabel 12100 2550 2    60   Output ~ 0
CRUB_3
Text GLabel 9750 5700 2    60   Input ~ 0
CRUB_0
Text GLabel 9750 5800 2    60   Input ~ 0
CRUB_1
Text GLabel 9750 5900 2    60   Input ~ 0
CRUB_2
Text GLabel 9750 6000 2    60   Input ~ 0
CRUB_3
Text GLabel 7350 4300 0    60   Input ~ 0
B_PH3
$Comp
L GND #PWR010
U 1 1 594FF989
P 15100 2900
F 0 "#PWR010" H 15100 2650 50  0001 C CNN
F 1 "GND" H 15100 2750 50  0000 C CNN
F 2 "" H 15100 2900 50  0001 C CNN
F 3 "" H 15100 2900 50  0001 C CNN
	1    15100 2900
	-1   0    0    1   
$EndComp
$Comp
L Conn_02x05_Counter_Clockwise RPi1
U 1 1 594FFC97
P 14350 3000
F 0 "RPi1" H 14350 3300 50  0000 C CNN
F 1 "RPI_CONN_02X05" H 14350 2700 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x05_Pitch2.54mm" H 14350 1800 50  0001 C CNN
F 3 "" H 14350 1800 50  0001 C CNN
	1    14350 3000
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR011
U 1 1 59584F63
P 2050 1100
F 0 "#PWR011" H 2050 950 50  0001 C CNN
F 1 "+5V" H 2050 1240 50  0000 C CNN
F 2 "" H 2050 1100 50  0001 C CNN
F 3 "" H 2050 1100 50  0001 C CNN
	1    2050 1100
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR012
U 1 1 59585050
P 2000 3050
F 0 "#PWR012" H 2000 2800 50  0001 C CNN
F 1 "GND" H 2000 2900 50  0000 C CNN
F 2 "" H 2000 3050 50  0001 C CNN
F 3 "" H 2000 3050 50  0001 C CNN
	1    2000 3050
	1    0    0    -1  
$EndComp
NoConn ~ 14700 1500
NoConn ~ 14700 1600
NoConn ~ 14450 1600
$Comp
L C_Small C2
U 1 1 59595B0D
P 2250 1000
F 0 "C2" H 2260 1070 50  0000 L CNN
F 1 "0.1uf" H 2260 920 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 2250 1000 50  0001 C CNN
F 3 "" H 2250 1000 50  0001 C CNN
	1    2250 1000
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR013
U 1 1 59595DCD
P 2250 800
F 0 "#PWR013" H 2250 550 50  0001 C CNN
F 1 "GND" H 2250 650 50  0000 C CNN
F 2 "" H 2250 800 50  0001 C CNN
F 3 "" H 2250 800 50  0001 C CNN
	1    2250 800 
	-1   0    0    1   
$EndComp
$Comp
L C_Small C13
U 1 1 595963F1
P 10400 8550
F 0 "C13" H 10410 8620 50  0000 L CNN
F 1 "0.1uf" H 10410 8470 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 10400 8550 50  0001 C CNN
F 3 "" H 10400 8550 50  0001 C CNN
	1    10400 8550
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR014
U 1 1 5959655E
P 10250 8650
F 0 "#PWR014" H 10250 8500 50  0001 C CNN
F 1 "+5V" H 10250 8790 50  0000 C CNN
F 2 "" H 10250 8650 50  0001 C CNN
F 3 "" H 10250 8650 50  0001 C CNN
	1    10250 8650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR015
U 1 1 59596997
P 10250 10050
F 0 "#PWR015" H 10250 9800 50  0001 C CNN
F 1 "GND" H 10250 9900 50  0000 C CNN
F 2 "" H 10250 10050 50  0001 C CNN
F 3 "" H 10250 10050 50  0001 C CNN
	1    10250 10050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR016
U 1 1 59596B4F
P 10400 8400
F 0 "#PWR016" H 10400 8150 50  0001 C CNN
F 1 "GND" H 10400 8250 50  0000 C CNN
F 2 "" H 10400 8400 50  0001 C CNN
F 3 "" H 10400 8400 50  0001 C CNN
	1    10400 8400
	-1   0    0    1   
$EndComp
$Comp
L R_Small R7
U 1 1 59612E43
P 13900 2050
F 0 "R7" H 13930 2070 50  0000 L CNN
F 1 "10k" H 13930 2010 50  0000 L CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" H 13900 2050 50  0001 C CNN
F 3 "" H 13900 2050 50  0001 C CNN
	1    13900 2050
	1    0    0    -1  
$EndComp
$Comp
L R_Small R8
U 1 1 59612F26
P 14100 2050
F 0 "R8" H 14130 2070 50  0000 L CNN
F 1 "10k" H 14130 2010 50  0000 L CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" H 14100 2050 50  0001 C CNN
F 3 "" H 14100 2050 50  0001 C CNN
	1    14100 2050
	1    0    0    -1  
$EndComp
$Comp
L R_Small R9
U 1 1 59612F85
P 14300 2050
F 0 "R9" H 14330 2070 50  0000 L CNN
F 1 "10k" H 14330 2010 50  0000 L CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" H 14300 2050 50  0001 C CNN
F 3 "" H 14300 2050 50  0001 C CNN
	1    14300 2050
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR017
U 1 1 59613684
P 14450 2200
F 0 "#PWR017" H 14450 2050 50  0001 C CNN
F 1 "+3.3V" H 14450 2340 50  0000 C CNN
F 2 "" H 14450 2200 50  0001 C CNN
F 3 "" H 14450 2200 50  0001 C CNN
	1    14450 2200
	0    1    1    0   
$EndComp
$Comp
L GND #PWR018
U 1 1 596AC072
P 11450 2450
F 0 "#PWR018" H 11450 2200 50  0001 C CNN
F 1 "GND" H 11450 2300 50  0000 C CNN
F 2 "" H 11450 2450 50  0001 C CNN
F 3 "" H 11450 2450 50  0001 C CNN
	1    11450 2450
	1    0    0    -1  
$EndComp
$Comp
L C_Small C10
U 1 1 596F064F
P 8750 850
F 0 "C10" H 8760 920 50  0000 L CNN
F 1 "0.1uf" H 8760 770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 8750 850 50  0001 C CNN
F 3 "" H 8750 850 50  0001 C CNN
	1    8750 850 
	1    0    0    -1  
$EndComp
$Comp
L C_Small C11
U 1 1 596F06B9
P 9000 850
F 0 "C11" H 9010 920 50  0000 L CNN
F 1 "0.1uf" H 9010 770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 9000 850 50  0001 C CNN
F 3 "" H 9000 850 50  0001 C CNN
	1    9000 850 
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR019
U 1 1 596F06BF
P 9500 750
F 0 "#PWR019" H 9500 600 50  0001 C CNN
F 1 "+3.3V" H 9500 890 50  0000 C CNN
F 2 "" H 9500 750 50  0001 C CNN
F 3 "" H 9500 750 50  0001 C CNN
	1    9500 750 
	1    0    0    -1  
$EndComp
$Comp
L C_Small C12
U 1 1 596F06CB
P 9250 850
F 0 "C12" H 9260 920 50  0000 L CNN
F 1 "0.1uf" H 9260 770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 9250 850 50  0001 C CNN
F 3 "" H 9250 850 50  0001 C CNN
	1    9250 850 
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR020
U 1 1 596F06D1
P 9150 1200
F 0 "#PWR020" H 9150 1050 50  0001 C CNN
F 1 "+3.3V" H 9150 1340 50  0000 C CNN
F 2 "" H 9150 1200 50  0001 C CNN
F 3 "" H 9150 1200 50  0001 C CNN
	1    9150 1200
	0    1    1    0   
$EndComp
$Comp
L GND #PWR021
U 1 1 596F06D7
P 9500 950
F 0 "#PWR021" H 9500 700 50  0001 C CNN
F 1 "GND" H 9500 800 50  0000 C CNN
F 2 "" H 9500 950 50  0001 C CNN
F 3 "" H 9500 950 50  0001 C CNN
	1    9500 950 
	1    0    0    -1  
$EndComp
$Comp
L C_Small C7
U 1 1 596F0DF9
P 8250 850
F 0 "C7" H 8260 920 50  0000 L CNN
F 1 "0.1uf" H 8260 770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 8250 850 50  0001 C CNN
F 3 "" H 8250 850 50  0001 C CNN
	1    8250 850 
	1    0    0    -1  
$EndComp
$Comp
L C_Small C6
U 1 1 596F0E6D
P 8000 850
F 0 "C6" H 8010 920 50  0000 L CNN
F 1 "0.1uf" H 8010 770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 8000 850 50  0001 C CNN
F 3 "" H 8000 850 50  0001 C CNN
	1    8000 850 
	1    0    0    -1  
$EndComp
$Comp
L C_Small C5
U 1 1 596F0E7F
P 7750 850
F 0 "C5" H 7760 920 50  0000 L CNN
F 1 "0.1uf" H 7760 770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 7750 850 50  0001 C CNN
F 3 "" H 7750 850 50  0001 C CNN
	1    7750 850 
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR022
U 1 1 596F5164
P 9000 7000
F 0 "#PWR022" H 9000 6750 50  0001 C CNN
F 1 "GND" H 9000 6850 50  0000 C CNN
F 2 "" H 9000 7000 50  0001 C CNN
F 3 "" H 9000 7000 50  0001 C CNN
	1    9000 7000
	1    0    0    -1  
$EndComp
$Comp
L XC95144XL-TQ100 U6
U 1 1 596EEAA9
P 8550 4100
F 0 "U6" H 7700 6750 50  0000 C CNN
F 1 "XC95144XL-TQ100" H 9250 1450 50  0000 C CNN
F 2 "Housings_QFP:TQFP-100_14x14mm_Pitch0.5mm" H 9800 1350 50  0001 C CNN
F 3 "" H 8500 4150 50  0001 C CNN
	1    8550 4100
	1    0    0    -1  
$EndComp
$Comp
L TEST_1P T5
U 1 1 597515DC
P 14650 2800
F 0 "T5" H 14650 3070 50  0000 C CNN
F 1 "TEST_1P" H 14650 3000 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 14850 2800 50  0001 C CNN
F 3 "" H 14850 2800 50  0001 C CNN
	1    14650 2800
	1    0    0    -1  
$EndComp
$Comp
L TEST_1P T4
U 1 1 5975362C
P 10200 5600
F 0 "T4" H 10200 5870 50  0000 C CNN
F 1 "TEST_1P" H 10200 5800 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 10400 5600 50  0001 C CNN
F 3 "" H 10400 5600 50  0001 C CNN
	1    10200 5600
	0    1    1    0   
$EndComp
$Comp
L TEST_1P T3
U 1 1 5975393E
P 10200 5500
F 0 "T3" H 10200 5770 50  0000 C CNN
F 1 "TEST_1P" H 10200 5700 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 10400 5500 50  0001 C CNN
F 3 "" H 10400 5500 50  0001 C CNN
	1    10200 5500
	0    1    1    0   
$EndComp
$Comp
L TEST_1P T2
U 1 1 597539A7
P 10200 5400
F 0 "T2" H 10200 5670 50  0000 C CNN
F 1 "TEST_1P" H 10200 5600 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 10400 5400 50  0001 C CNN
F 3 "" H 10400 5400 50  0001 C CNN
	1    10200 5400
	0    1    1    0   
$EndComp
$Comp
L TEST_1P T1
U 1 1 59753A11
P 10200 5300
F 0 "T1" H 10200 5570 50  0000 C CNN
F 1 "TEST_1P" H 10200 5500 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 10400 5300 50  0001 C CNN
F 3 "" H 10400 5300 50  0001 C CNN
	1    10200 5300
	0    1    1    0   
$EndComp
$Comp
L R R4
U 1 1 599E6C64
P 11450 2300
F 0 "R4" V 11530 2300 50  0000 C CNN
F 1 "1k" V 11450 2300 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 11380 2300 50  0001 C CNN
F 3 "" H 11450 2300 50  0001 C CNN
	1    11450 2300
	1    0    0    -1  
$EndComp
Text Notes 13300 3150 0    60   ~ 0
GPIO_26
Text Notes 13300 3050 0    60   ~ 0
GPIO_19
Text Notes 13300 2950 0    60   ~ 0
GPIO_13
Text Notes 13300 2850 0    60   ~ 0
GPIO_6
Text Notes 15250 2850 0    60   ~ 0
GPIO_12
Text Notes 15100 3050 0    60   ~ 0
GPIO_16
Text Notes 15100 3150 0    60   ~ 0
GPIO_20
Text Notes 15100 3250 0    60   ~ 0
GPIO_21
$Comp
L TiPEBEdge E1
U 1 1 59BEF870
P 1750 5700
F 0 "E1" H 1450 7250 60  0000 C CNN
F 1 "TiPEBEdge" V 1750 5700 60  0000 C CNN
F 2 "peb-edge-card:ti99-peb-edge" H 1750 7250 60  0001 C CNN
F 3 "" H 1750 7250 60  0001 C CNN
	1    1750 5700
	1    0    0    -1  
$EndComp
Text GLabel 1200 5400 0    60   BiDi ~ 0
TI_D3
Text GLabel 2300 5500 2    60   BiDi ~ 0
TI_D2
Text GLabel 1200 5500 0    60   BiDi ~ 0
TI_D1
Text GLabel 2300 5600 2    60   BiDi ~ 0
TI_D0
Text GLabel 1200 5300 0    60   BiDi ~ 0
TI_D5
Text GLabel 2300 5400 2    60   BiDi ~ 0
TI_D4
Text GLabel 2300 5300 2    60   BiDi ~ 0
TI_D6
Text GLabel 1200 5200 0    60   BiDi ~ 0
TI_D7
$Comp
L 74HC244 U5
U 1 1 59C69B40
P 8150 9400
F 0 "U5" H 8250 10050 50  0000 L CNN
F 1 "74HCT244" H 8200 8750 50  0000 L CNN
F 2 "SMD_Packages:SSOP-20" H 8150 9400 50  0001 C CNN
F 3 "" H 8150 9400 50  0000 C CNN
	1    8150 9400
	1    0    0    -1  
$EndComp
$Comp
L 74HC244 U4
U 1 1 59C69BE6
P 5800 9400
F 0 "U4" H 5900 10050 50  0000 L CNN
F 1 "74HCT244" H 5850 8750 50  0000 L CNN
F 2 "SMD_Packages:SSOP-20" H 5800 9400 50  0001 C CNN
F 3 "" H 5800 9400 50  0000 C CNN
	1    5800 9400
	1    0    0    -1  
$EndComp
$Comp
L 74HC244 U3
U 1 1 59C69C7A
P 3750 9400
F 0 "U3" H 3850 10050 50  0000 L CNN
F 1 "74HCT244" H 3800 8750 50  0000 L CNN
F 2 "SMD_Packages:SSOP-20" H 3750 9400 50  0001 C CNN
F 3 "" H 3750 9400 50  0000 C CNN
	1    3750 9400
	1    0    0    -1  
$EndComp
Text GLabel 8650 8900 2    60   Output ~ 0
B_A0
Text GLabel 8650 9000 2    60   Output ~ 0
B_A1
Text GLabel 8650 9100 2    60   Output ~ 0
B_A2
Text GLabel 8650 9200 2    60   Output ~ 0
B_A3
Text GLabel 8650 9300 2    60   Output ~ 0
B_A4
Text GLabel 8650 9400 2    60   Output ~ 0
B_A5
Text GLabel 8650 9500 2    60   Output ~ 0
B_A6
Text GLabel 8650 9600 2    60   Output ~ 0
B_A7
Text GLabel 6300 8900 2    60   Output ~ 0
B_A8
Text GLabel 6300 9000 2    60   Output ~ 0
B_A9
Text GLabel 6300 9100 2    60   Output ~ 0
B_A10
Text GLabel 6300 9200 2    60   Output ~ 0
B_A11
Text GLabel 6300 9300 2    60   Output ~ 0
B_A12
Text GLabel 6300 9400 2    60   Output ~ 0
B_A13
Text GLabel 6300 9500 2    60   Output ~ 0
B_A14
Text GLabel 6300 9600 2    60   Output ~ 0
B_A15
$Comp
L GND #PWR023
U 1 1 59C6B31F
P 5500 10050
F 0 "#PWR023" H 5500 9800 50  0001 C CNN
F 1 "GND" H 5500 9900 50  0000 C CNN
F 2 "" H 5500 10050 50  0001 C CNN
F 3 "" H 5500 10050 50  0001 C CNN
	1    5500 10050
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR024
U 1 1 59C6B393
P 7850 10050
F 0 "#PWR024" H 7850 9800 50  0001 C CNN
F 1 "GND" H 7850 9900 50  0000 C CNN
F 2 "" H 7850 10050 50  0001 C CNN
F 3 "" H 7850 10050 50  0001 C CNN
	1    7850 10050
	0    -1   -1   0   
$EndComp
$Comp
L R R2
U 1 1 59C6B529
P 5350 10050
F 0 "R2" V 5430 10050 50  0000 C CNN
F 1 "1k" V 5350 10050 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 5280 10050 50  0001 C CNN
F 3 "" H 5350 10050 50  0001 C CNN
	1    5350 10050
	0    1    1    0   
$EndComp
$Comp
L R R3
U 1 1 59C6B916
P 7700 10050
F 0 "R3" V 7780 10050 50  0000 C CNN
F 1 "1k" V 7700 10050 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 7630 10050 50  0001 C CNN
F 3 "" H 7700 10050 50  0001 C CNN
	1    7700 10050
	0    1    1    0   
$EndComp
$Comp
L R R1
U 1 1 59C6CE84
P 3300 10100
F 0 "R1" V 3380 10100 50  0000 C CNN
F 1 "1k" V 3300 10100 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 3230 10100 50  0001 C CNN
F 3 "" H 3300 10100 50  0001 C CNN
	1    3300 10100
	0    1    1    0   
$EndComp
$Comp
L GND #PWR025
U 1 1 59C6CF44
P 3450 10100
F 0 "#PWR025" H 3450 9850 50  0001 C CNN
F 1 "GND" H 3450 9950 50  0000 C CNN
F 2 "" H 3450 10100 50  0001 C CNN
F 3 "" H 3450 10100 50  0001 C CNN
	1    3450 10100
	0    -1   -1   0   
$EndComp
Text GLabel 4250 9000 2    60   Output ~ 0
B_CRUCLK
Text GLabel 4250 9100 2    60   Output ~ 0
B_PH3
Text GLabel 4250 9200 2    60   Output ~ 0
B_DBIN
Text GLabel 1200 7000 0    60   Input ~ 0
TI_CRUIN
Text GLabel 2300 5700 2    60   Output ~ 0
TI_A15
Text GLabel 2300 5800 2    60   Output ~ 0
TI_A13
Text GLabel 2300 5900 2    60   Output ~ 0
TI_A11
Text GLabel 1200 5700 0    60   Output ~ 0
TI_A14
Text GLabel 1200 5800 0    60   Output ~ 0
TI_A12
Text GLabel 1200 5900 0    60   Output ~ 0
TI_A10
Text GLabel 2300 6000 2    60   Output ~ 0
TI_A9
Text GLabel 1200 6000 0    60   Output ~ 0
TI_A8
Text GLabel 2300 6100 2    60   Output ~ 0
TI_A7
Text GLabel 1200 6100 0    60   Output ~ 0
TI_A6
Text GLabel 2300 6200 2    60   Output ~ 0
TI_A5
Text GLabel 2300 6300 2    60   Output ~ 0
TI_A3
Text GLabel 2300 6400 2    60   Output ~ 0
TI_A1
Text GLabel 1200 6200 0    60   Output ~ 0
TI_A4
Text GLabel 1200 6300 0    60   Output ~ 0
TI_A2
Text GLabel 1200 6400 0    60   Output ~ 0
TI_A0
Text GLabel 5300 9600 0    60   Input ~ 0
TI_A15
Text GLabel 5300 9400 0    60   Input ~ 0
TI_A13
Text GLabel 5300 9200 0    60   Input ~ 0
TI_A11
Text GLabel 5300 9000 0    60   Input ~ 0
TI_A9
Text GLabel 5300 9500 0    60   Input ~ 0
TI_A14
Text GLabel 5300 9300 0    60   Input ~ 0
TI_A12
Text GLabel 5300 9100 0    60   Input ~ 0
TI_A10
Text GLabel 5300 8900 0    60   Input ~ 0
TI_A8
Text GLabel 7650 9600 0    60   Input ~ 0
TI_A7
Text GLabel 7650 9400 0    60   Input ~ 0
TI_A5
Text GLabel 7650 9200 0    60   Input ~ 0
TI_A3
Text GLabel 7650 9000 0    60   Input ~ 0
TI_A1
Text GLabel 7650 8900 0    60   Input ~ 0
TI_A0
Text GLabel 7650 9100 0    60   Input ~ 0
TI_A2
Text GLabel 7650 9300 0    60   Input ~ 0
TI_A4
Text GLabel 7650 9500 0    60   Input ~ 0
TI_A6
Wire Wire Line
	13850 1300 14450 1300
Wire Wire Line
	13900 1400 14450 1400
Wire Wire Line
	13850 1500 14450 1500
Wire Wire Line
	13850 1700 14450 1700
Wire Wire Line
	14700 1700 15100 1700
Wire Wire Line
	14700 1400 15100 1400
Wire Wire Line
	14700 1300 15100 1300
Wire Wire Line
	1000 2700 1350 2700
Wire Wire Line
	1350 2900 1350 3000
Wire Wire Line
	1350 3000 1250 3000
Wire Wire Line
	14050 4550 14850 4550
Wire Wire Line
	14050 4550 14050 4450
Wire Wire Line
	14850 4550 14850 4450
Connection ~ 14450 4550
Wire Wire Line
	13900 4250 14150 4250
Connection ~ 14050 4250
Wire Wire Line
	14750 4250 15000 4250
Connection ~ 14850 4250
Wire Wire Line
	12500 1200 12600 1200
Wire Wire Line
	12900 1200 13000 1200
Wire Wire Line
	12100 1200 12200 1200
Wire Wire Line
	11800 900  11900 900 
Wire Wire Line
	11700 1200 11600 1200
Wire Wire Line
	11400 900  11500 900 
Wire Wire Line
	11600 2150 11600 2550
Connection ~ 11600 2250
Connection ~ 11600 2350
Connection ~ 11600 2450
Wire Wire Line
	14000 3300 14000 3200
Wire Wire Line
	14000 3200 14150 3200
Wire Wire Line
	14650 2900 15100 2900
Wire Wire Line
	2050 1100 2050 1150
Wire Wire Line
	2050 1100 2250 1100
Connection ~ 2050 1100
Wire Wire Line
	2250 900  2250 800 
Wire Wire Line
	10400 8650 10250 8650
Wire Wire Line
	10250 8650 10250 8850
Wire Wire Line
	10400 8450 10400 8400
Wire Wire Line
	10250 10050 10250 9950
Connection ~ 10250 8650
Wire Wire Line
	13900 2200 14450 2200
Wire Wire Line
	14300 2200 14300 2150
Wire Wire Line
	14100 2200 14100 2150
Connection ~ 14300 2200
Wire Wire Line
	13900 2200 13900 2150
Connection ~ 14100 2200
Wire Wire Line
	13900 1950 13900 1700
Connection ~ 13900 1700
Wire Wire Line
	14100 1950 14000 1950
Wire Wire Line
	14000 1950 14000 1500
Connection ~ 14000 1500
Wire Wire Line
	14300 1950 14200 1950
Wire Wire Line
	14200 1950 14200 1850
Wire Wire Line
	14200 1850 14100 1850
Wire Wire Line
	14100 1850 14100 1300
Connection ~ 14100 1300
Wire Wire Line
	8150 1200 9150 1200
Connection ~ 8250 1200
Connection ~ 8350 1200
Connection ~ 8650 1200
Connection ~ 8750 1200
Connection ~ 8850 1200
Connection ~ 8950 1200
Wire Wire Line
	7750 750  9500 750 
Connection ~ 8000 750 
Connection ~ 8250 750 
Connection ~ 8500 750 
Connection ~ 8750 750 
Connection ~ 9000 750 
Connection ~ 9250 750 
Wire Wire Line
	7750 950  9500 950 
Connection ~ 8000 950 
Connection ~ 8250 950 
Connection ~ 8500 950 
Connection ~ 8750 950 
Connection ~ 9000 950 
Connection ~ 9250 950 
Wire Wire Line
	8150 7000 9000 7000
Connection ~ 8250 7000
Connection ~ 8350 7000
Connection ~ 8450 7000
Connection ~ 8550 7000
Connection ~ 8650 7000
Connection ~ 8750 7000
Connection ~ 8850 7000
Wire Wire Line
	9750 5600 10200 5600
Wire Wire Line
	9750 5500 10200 5500
Wire Wire Line
	9750 5400 10200 5400
Wire Wire Line
	9750 5300 10200 5300
Wire Wire Line
	11600 2150 11450 2150
Wire Wire Line
	5200 9800 5300 9800
Wire Wire Line
	5300 9900 5200 9900
Wire Wire Line
	7550 9800 7550 10050
Wire Wire Line
	7550 9800 7650 9800
Wire Wire Line
	7650 9900 7550 9900
Connection ~ 7550 9900
Wire Wire Line
	5200 9800 5200 10050
Connection ~ 5200 9900
Text GLabel 2300 7000 2    60   Output ~ 0
TI_MEMEN
Text GLabel 3250 9000 0    60   Input ~ 0
TI_CRUCLK
Text GLabel 3250 9100 0    60   Input ~ 0
TI_PH3
Text GLabel 3250 9200 0    60   Input ~ 0
TI_DBIN
Text GLabel 1200 6500 0    60   Output ~ 0
TI_AMB
Text GLabel 1200 6800 0    60   Output ~ 0
TI_CRUCLK
Text GLabel 2300 6800 2    60   Output ~ 0
TI_DBIN
Text GLabel 2300 6700 2    60   Output ~ 0
TI_PH3
Text GLabel 1250 9650 0    60   Input ~ 0
TI_MEMEN
Text GLabel 4250 8900 2    60   Output ~ 0
B_WE
Text GLabel 3250 8900 0    60   Input ~ 0
TI_WE
Text GLabel 2300 6900 2    60   Output ~ 0
TI_WE
$Comp
L 74LS138 U1
U 1 1 59C72E85
P 1850 9300
F 0 "U1" H 1950 9800 50  0000 C CNN
F 1 "74HCT138" H 2000 8751 50  0000 C CNN
F 2 "SMD_Packages:SO-16-W" H 1850 9300 50  0001 C CNN
F 3 "" H 1850 9300 50  0001 C CNN
	1    1850 9300
	1    0    0    -1  
$EndComp
Text GLabel 2300 6500 2    60   Output ~ 0
TI_AMA
Text GLabel 2300 6600 2    60   Output ~ 0
TI_AMC
Text GLabel 1250 8950 0    60   Input ~ 0
TI_AMA
Text GLabel 1250 9150 0    60   Input ~ 0
TI_AMC
Text GLabel 1250 9050 0    60   Input ~ 0
TI_AMB
Text GLabel 2300 4600 2    60   Output ~ 0
TI_AMD
Text GLabel 1200 4700 0    60   Output ~ 0
TI_AME
Text GLabel 1050 9550 0    60   Input ~ 0
TI_AMD
Text GLabel 1050 9450 0    60   Input ~ 0
TI_AME
Wire Wire Line
	3250 9800 3150 9800
Wire Wire Line
	3150 9600 3150 10100
$Comp
L C_Small C1
U 1 1 59C76A23
P 2000 8550
F 0 "C1" H 2010 8620 50  0000 L CNN
F 1 "0.1uf" H 2010 8470 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 2000 8550 50  0001 C CNN
F 3 "" H 2000 8550 50  0001 C CNN
	1    2000 8550
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR026
U 1 1 59C76A29
P 1850 8650
F 0 "#PWR026" H 1850 8500 50  0001 C CNN
F 1 "+5V" H 1850 8790 50  0000 C CNN
F 2 "" H 1850 8650 50  0001 C CNN
F 3 "" H 1850 8650 50  0001 C CNN
	1    1850 8650
	1    0    0    -1  
$EndComp
Wire Wire Line
	2000 8650 1850 8650
Wire Wire Line
	1850 8650 1850 8850
Wire Wire Line
	2000 8450 2000 8400
Connection ~ 1850 8650
$Comp
L C_Small C3
U 1 1 59C76B96
P 3900 8500
F 0 "C3" H 3910 8570 50  0000 L CNN
F 1 "0.1uf" H 3910 8420 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 3900 8500 50  0001 C CNN
F 3 "" H 3900 8500 50  0001 C CNN
	1    3900 8500
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR027
U 1 1 59C76B9C
P 3750 8600
F 0 "#PWR027" H 3750 8450 50  0001 C CNN
F 1 "+5V" H 3750 8740 50  0000 C CNN
F 2 "" H 3750 8600 50  0001 C CNN
F 3 "" H 3750 8600 50  0001 C CNN
	1    3750 8600
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR028
U 1 1 59C76BA2
P 3900 8350
F 0 "#PWR028" H 3900 8100 50  0001 C CNN
F 1 "GND" H 3900 8200 50  0000 C CNN
F 2 "" H 3900 8350 50  0001 C CNN
F 3 "" H 3900 8350 50  0001 C CNN
	1    3900 8350
	-1   0    0    1   
$EndComp
Wire Wire Line
	3900 8400 3900 8350
Wire Wire Line
	3750 8600 3900 8600
Wire Wire Line
	3750 8600 3750 8700
$Comp
L C_Small C4
U 1 1 59C76D70
P 5950 8500
F 0 "C4" H 5960 8570 50  0000 L CNN
F 1 "0.1uf" H 5960 8420 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 5950 8500 50  0001 C CNN
F 3 "" H 5950 8500 50  0001 C CNN
	1    5950 8500
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR029
U 1 1 59C76D76
P 5800 8600
F 0 "#PWR029" H 5800 8450 50  0001 C CNN
F 1 "+5V" H 5800 8740 50  0000 C CNN
F 2 "" H 5800 8600 50  0001 C CNN
F 3 "" H 5800 8600 50  0001 C CNN
	1    5800 8600
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR030
U 1 1 59C76D7C
P 5950 8350
F 0 "#PWR030" H 5950 8100 50  0001 C CNN
F 1 "GND" H 5950 8200 50  0000 C CNN
F 2 "" H 5950 8350 50  0001 C CNN
F 3 "" H 5950 8350 50  0001 C CNN
	1    5950 8350
	-1   0    0    1   
$EndComp
Wire Wire Line
	5950 8400 5950 8350
Wire Wire Line
	5800 8600 5950 8600
Wire Wire Line
	5800 8600 5800 8700
$Comp
L C_Small C8
U 1 1 59C76E70
P 8300 8500
F 0 "C8" H 8310 8570 50  0000 L CNN
F 1 "0.1uf" H 8310 8420 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 8300 8500 50  0001 C CNN
F 3 "" H 8300 8500 50  0001 C CNN
	1    8300 8500
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR031
U 1 1 59C76E76
P 8150 8600
F 0 "#PWR031" H 8150 8450 50  0001 C CNN
F 1 "+5V" H 8150 8740 50  0000 C CNN
F 2 "" H 8150 8600 50  0001 C CNN
F 3 "" H 8150 8600 50  0001 C CNN
	1    8150 8600
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR032
U 1 1 59C76E7C
P 8300 8350
F 0 "#PWR032" H 8300 8100 50  0001 C CNN
F 1 "GND" H 8300 8200 50  0000 C CNN
F 2 "" H 8300 8350 50  0001 C CNN
F 3 "" H 8300 8350 50  0001 C CNN
	1    8300 8350
	-1   0    0    1   
$EndComp
Wire Wire Line
	8300 8400 8300 8350
Wire Wire Line
	8150 8600 8300 8600
Wire Wire Line
	8150 8600 8150 8700
$Comp
L GND #PWR033
U 1 1 59C76FD1
P 5800 10100
F 0 "#PWR033" H 5800 9850 50  0001 C CNN
F 1 "GND" H 5800 9950 50  0000 C CNN
F 2 "" H 5800 10100 50  0001 C CNN
F 3 "" H 5800 10100 50  0001 C CNN
	1    5800 10100
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR034
U 1 1 59C7705D
P 3750 10100
F 0 "#PWR034" H 3750 9850 50  0001 C CNN
F 1 "GND" H 3750 9950 50  0000 C CNN
F 2 "" H 3750 10100 50  0001 C CNN
F 3 "" H 3750 10100 50  0001 C CNN
	1    3750 10100
	1    0    0    -1  
$EndComp
Wire Wire Line
	850  6600 1200 6600
Wire Wire Line
	1200 6700 1000 6700
Wire Wire Line
	1200 5600 850  5600
Wire Wire Line
	2300 5200 2600 5200
$Comp
L +8V #PWR035
U 1 1 59E1955F
P 1200 4300
F 0 "#PWR035" H 1200 4150 50  0001 C CNN
F 1 "+8V" H 1200 4440 50  0000 C CNN
F 2 "" H 1200 4300 50  0001 C CNN
F 3 "" H 1200 4300 50  0001 C CNN
	1    1200 4300
	1    0    0    -1  
$EndComp
$Comp
L +8V #PWR036
U 1 1 59E1A127
P 13900 4250
F 0 "#PWR036" H 13900 4100 50  0001 C CNN
F 1 "+8V" H 13900 4390 50  0000 C CNN
F 2 "" H 13900 4250 50  0001 C CNN
F 3 "" H 13900 4250 50  0001 C CNN
	1    13900 4250
	0    -1   -1   0   
$EndComp
$Comp
L LM7805_TO220 U9
U 1 1 59E1BD59
P 14450 5200
F 0 "U9" H 14300 5325 50  0000 C CNN
F 1 "LM7805_TO220" H 14450 5325 50  0000 L CNN
F 2 "TO_SOT_Packages_SMD:SOT-223" H 14450 5425 50  0001 C CIN
F 3 "" H 14450 5150 50  0001 C CNN
	1    14450 5200
	1    0    0    -1  
$EndComp
$Comp
L +8V #PWR037
U 1 1 59E1BE02
P 13950 5200
F 0 "#PWR037" H 13950 5050 50  0001 C CNN
F 1 "+8V" H 13950 5340 50  0000 C CNN
F 2 "" H 13950 5200 50  0001 C CNN
F 3 "" H 13950 5200 50  0001 C CNN
	1    13950 5200
	0    -1   -1   0   
$EndComp
$Comp
L CP1_Small C15
U 1 1 59E1BE91
P 14050 5300
F 0 "C15" H 14060 5370 50  0000 L CNN
F 1 "10uf" H 14060 5220 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 14050 5300 50  0001 C CNN
F 3 "" H 14050 5300 50  0001 C CNN
	1    14050 5300
	1    0    0    -1  
$EndComp
$Comp
L CP1_Small C17
U 1 1 59E1BF3C
P 14850 5300
F 0 "C17" H 14860 5370 50  0000 L CNN
F 1 "22uf" H 14860 5220 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 14850 5300 50  0001 C CNN
F 3 "" H 14850 5300 50  0001 C CNN
	1    14850 5300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR038
U 1 1 59E1BFF6
P 14450 5600
F 0 "#PWR038" H 14450 5350 50  0001 C CNN
F 1 "GND" H 14450 5450 50  0000 C CNN
F 2 "" H 14450 5600 50  0001 C CNN
F 3 "" H 14450 5600 50  0001 C CNN
	1    14450 5600
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR039
U 1 1 59E1C3C9
P 15000 5200
F 0 "#PWR039" H 15000 5050 50  0001 C CNN
F 1 "+5V" H 15000 5340 50  0000 C CNN
F 2 "" H 15000 5200 50  0001 C CNN
F 3 "" H 15000 5200 50  0001 C CNN
	1    15000 5200
	0    1    1    0   
$EndComp
Wire Wire Line
	14750 5200 15000 5200
Connection ~ 14850 5200
Wire Wire Line
	13950 5200 14150 5200
Connection ~ 14050 5200
Wire Wire Line
	14050 5400 14050 5550
Wire Wire Line
	14050 5550 14850 5550
Wire Wire Line
	14850 5550 14850 5400
Wire Wire Line
	14450 5500 14450 5600
Connection ~ 14450 5550
Text GLabel 7350 2900 0    60   Input ~ 0
B_MEMEN
NoConn ~ 2300 4300
NoConn ~ 2300 4400
NoConn ~ 2300 4500
NoConn ~ 2300 4700
NoConn ~ 2300 4800
NoConn ~ 2300 4900
NoConn ~ 2300 5000
NoConn ~ 2300 5100
NoConn ~ 1200 4900
NoConn ~ 1200 5000
NoConn ~ 1200 5100
NoConn ~ 1200 7100
NoConn ~ 1200 7200
Wire Wire Line
	950  6900 1200 6900
NoConn ~ 7350 2500
NoConn ~ 7350 2600
NoConn ~ 7350 3700
NoConn ~ 7350 3800
NoConn ~ 7350 4100
NoConn ~ 7350 4200
NoConn ~ 7350 4400
NoConn ~ 7350 4700
NoConn ~ 7350 4900
NoConn ~ 9750 5200
NoConn ~ 9750 5100
NoConn ~ 9750 4800
NoConn ~ 9750 4700
NoConn ~ 9750 4600
NoConn ~ 9750 4500
NoConn ~ 9750 4400
NoConn ~ 9750 4300
NoConn ~ 9750 4200
NoConn ~ 9750 4000
NoConn ~ 9750 3000
NoConn ~ 9750 2900
NoConn ~ 9750 2600
NoConn ~ 9750 2500
NoConn ~ 9750 2400
NoConn ~ 9750 2300
NoConn ~ 9750 2200
NoConn ~ 9750 2100
NoConn ~ 9750 2000
NoConn ~ 9750 1900
NoConn ~ 9750 1800
NoConn ~ 2300 7100
NoConn ~ 2300 7200
$Comp
L GND #PWR040
U 1 1 59E4A124
P 2600 5200
F 0 "#PWR040" H 2600 4950 50  0001 C CNN
F 1 "GND" H 2600 5050 50  0000 C CNN
F 2 "" H 2600 5200 50  0001 C CNN
F 3 "" H 2600 5200 50  0001 C CNN
	1    2600 5200
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR041
U 1 1 59E4AF1D
P 1200 4400
F 0 "#PWR041" H 1200 4150 50  0001 C CNN
F 1 "GND" H 1200 4250 50  0000 C CNN
F 2 "" H 1200 4400 50  0001 C CNN
F 3 "" H 1200 4400 50  0001 C CNN
	1    1200 4400
	0    1    1    0   
$EndComp
$Comp
L GND #PWR042
U 1 1 59E4B3D4
P 1200 4500
F 0 "#PWR042" H 1200 4250 50  0001 C CNN
F 1 "GND" H 1200 4350 50  0000 C CNN
F 2 "" H 1200 4500 50  0001 C CNN
F 3 "" H 1200 4500 50  0001 C CNN
	1    1200 4500
	0    1    1    0   
$EndComp
$Comp
L GND #PWR043
U 1 1 59E4B469
P 1200 4600
F 0 "#PWR043" H 1200 4350 50  0001 C CNN
F 1 "GND" H 1200 4450 50  0000 C CNN
F 2 "" H 1200 4600 50  0001 C CNN
F 3 "" H 1200 4600 50  0001 C CNN
	1    1200 4600
	0    1    1    0   
$EndComp
$Comp
L GND #PWR044
U 1 1 59E4B4FE
P 850 5600
F 0 "#PWR044" H 850 5350 50  0001 C CNN
F 1 "GND" H 850 5450 50  0000 C CNN
F 2 "" H 850 5600 50  0001 C CNN
F 3 "" H 850 5600 50  0001 C CNN
	1    850  5600
	0    1    1    0   
$EndComp
$Comp
L GND #PWR045
U 1 1 59E4B9B5
P 850 6600
F 0 "#PWR045" H 850 6350 50  0001 C CNN
F 1 "GND" H 850 6450 50  0000 C CNN
F 2 "" H 850 6600 50  0001 C CNN
F 3 "" H 850 6600 50  0001 C CNN
	1    850  6600
	0    1    1    0   
$EndComp
$Comp
L GND #PWR046
U 1 1 59E4BB30
P 1000 6700
F 0 "#PWR046" H 1000 6450 50  0001 C CNN
F 1 "GND" H 1000 6550 50  0000 C CNN
F 2 "" H 1000 6700 50  0001 C CNN
F 3 "" H 1000 6700 50  0001 C CNN
	1    1000 6700
	0    1    1    0   
$EndComp
$Comp
L GND #PWR047
U 1 1 59E4BBC5
P 950 6900
F 0 "#PWR047" H 950 6650 50  0001 C CNN
F 1 "GND" H 950 6750 50  0000 C CNN
F 2 "" H 950 6900 50  0001 C CNN
F 3 "" H 950 6900 50  0001 C CNN
	1    950  6900
	0    1    1    0   
$EndComp
NoConn ~ 3250 9300
NoConn ~ 3250 9400
NoConn ~ 3250 9500
NoConn ~ 4250 9300
NoConn ~ 4250 9400
NoConn ~ 4250 9500
NoConn ~ 2450 9550
NoConn ~ 2450 9450
NoConn ~ 2450 9350
NoConn ~ 2450 9250
NoConn ~ 2450 9150
NoConn ~ 2450 9050
NoConn ~ 2450 8950
$Comp
L GND #PWR048
U 1 1 59E3C0E9
P 1850 9900
F 0 "#PWR048" H 1850 9650 50  0001 C CNN
F 1 "GND" H 1850 9750 50  0000 C CNN
F 2 "" H 1850 9900 50  0001 C CNN
F 3 "" H 1850 9900 50  0001 C CNN
	1    1850 9900
	1    0    0    -1  
$EndComp
Wire Wire Line
	1850 9900 1850 9750
$Comp
L GND #PWR049
U 1 1 59E3C39E
P 8150 10100
F 0 "#PWR049" H 8150 9850 50  0001 C CNN
F 1 "GND" H 8150 9950 50  0000 C CNN
F 2 "" H 8150 10100 50  0001 C CNN
F 3 "" H 8150 10100 50  0001 C CNN
	1    8150 10100
	1    0    0    -1  
$EndComp
Text GLabel 3050 9900 0    60   Input ~ 0
DB_EN
Wire Wire Line
	3050 9900 3250 9900
Text GLabel 1200 4800 0    60   Input ~ 0
RDBENA
Text GLabel 4250 9600 2    60   Output ~ 0
RDBENA
Wire Wire Line
	3150 9600 3250 9600
Connection ~ 3150 9800
$Comp
L R R10
U 1 1 59EF200E
P 1100 9950
F 0 "R10" V 1180 9950 50  0000 C CNN
F 1 "4.7k" V 1100 9950 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 1030 9950 50  0001 C CNN
F 3 "" H 1100 9950 50  0001 C CNN
	1    1100 9950
	1    0    0    -1  
$EndComp
$Comp
L R R11
U 1 1 59EF20E5
P 1250 9950
F 0 "R11" V 1330 9950 50  0000 C CNN
F 1 "4.7k" V 1250 9950 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 1180 9950 50  0001 C CNN
F 3 "" H 1250 9950 50  0001 C CNN
	1    1250 9950
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR050
U 1 1 59EF22F3
P 1250 10100
F 0 "#PWR050" H 1250 9850 50  0001 C CNN
F 1 "GND" H 1250 9950 50  0000 C CNN
F 2 "" H 1250 10100 50  0001 C CNN
F 3 "" H 1250 10100 50  0001 C CNN
	1    1250 10100
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR051
U 1 1 59EF241E
P 1100 10100
F 0 "#PWR051" H 1100 9950 50  0001 C CNN
F 1 "+5V" H 1100 10240 50  0000 C CNN
F 2 "" H 1100 10100 50  0001 C CNN
F 3 "" H 1100 10100 50  0001 C CNN
	1    1100 10100
	-1   0    0    1   
$EndComp
Wire Wire Line
	1250 9800 1250 9550
Wire Wire Line
	1250 9550 1050 9550
Wire Wire Line
	1100 9800 1100 9450
Wire Wire Line
	1050 9450 1250 9450
Connection ~ 1100 9450
Connection ~ 1250 9550
$Comp
L GND #PWR052
U 1 1 59EF80F6
P 2000 8400
F 0 "#PWR052" H 2000 8150 50  0001 C CNN
F 1 "GND" H 2000 8250 50  0000 C CNN
F 2 "" H 2000 8400 50  0001 C CNN
F 3 "" H 2000 8400 50  0001 C CNN
	1    2000 8400
	-1   0    0    1   
$EndComp
$EndSCHEMATC
