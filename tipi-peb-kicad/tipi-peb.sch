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
Date "2017-09-23"
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
L 74LS245 U3
U 1 1 5917F86D
P 10250 9400
F 0 "U3" H 10350 9975 50  0000 L BNN
F 1 "74HCT245" H 10300 8825 50  0000 L TNN
F 2 "SMD_Packages:SSOP-20" H 10250 9400 50  0001 C CNN
F 3 "" H 10250 9400 50  0001 C CNN
	1    10250 9400
	1    0    0    -1  
$EndComp
$Comp
L C_Small C6
U 1 1 5917FDFE
P 8500 850
F 0 "C6" H 8510 920 50  0000 L CNN
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
F 2 "Connect:IDC_Header_Straight_10pins" V 14080 1520 50  0001 C CNN
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
L +3.3V #PWR04
U 1 1 591AACD3
P 15100 1400
F 0 "#PWR04" H 15100 1250 50  0001 C CNN
F 1 "+3.3V" H 15100 1540 50  0000 C CNN
F 2 "" H 15100 1400 50  0001 C CNN
F 3 "" H 15100 1400 50  0001 C CNN
	1    15100 1400
	0    1    1    0   
$EndComp
$Comp
L GND #PWR05
U 1 1 591AACFB
P 15100 1300
F 0 "#PWR05" H 15100 1050 50  0001 C CNN
F 1 "GND" H 15100 1150 50  0000 C CNN
F 2 "" H 15100 1300 50  0001 C CNN
F 3 "" H 15100 1300 50  0001 C CNN
	1    15100 1300
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR06
U 1 1 591AAD23
P 15100 1700
F 0 "#PWR06" H 15100 1450 50  0001 C CNN
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
L +5V #PWR07
U 1 1 594E090D
P 1000 2700
F 0 "#PWR07" H 1000 2550 50  0001 C CNN
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
L LM1117-3.3 U4
U 1 1 594EAE75
P 13100 6300
F 0 "U4" H 13200 6050 50  0000 C CNN
F 1 "LM1117-3.3" H 13100 6550 50  0000 C CNN
F 2 "TO_SOT_Packages_SMD:SOT-223" H 13100 6300 50  0001 C CNN
F 3 "" H 13100 6300 50  0001 C CNN
	1    13100 6300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR08
U 1 1 594EAFBA
P 13100 6600
F 0 "#PWR08" H 13100 6350 50  0001 C CNN
F 1 "GND" H 13100 6450 50  0000 C CNN
F 2 "" H 13100 6600 50  0001 C CNN
F 3 "" H 13100 6600 50  0001 C CNN
	1    13100 6600
	1    0    0    -1  
$EndComp
$Comp
L CP1_Small C2
U 1 1 594EB02A
P 13500 6400
F 0 "C2" H 13510 6470 50  0000 L CNN
F 1 "22uf" H 13510 6320 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 13500 6400 50  0001 C CNN
F 3 "" H 13500 6400 50  0001 C CNN
	1    13500 6400
	1    0    0    -1  
$EndComp
$Comp
L CP1_Small C1
U 1 1 594EB077
P 12700 6400
F 0 "C1" H 12710 6470 50  0000 L CNN
F 1 "10uf" H 12710 6320 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 12700 6400 50  0001 C CNN
F 3 "" H 12700 6400 50  0001 C CNN
	1    12700 6400
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR09
U 1 1 594EB46B
P 13650 6300
F 0 "#PWR09" H 13650 6150 50  0001 C CNN
F 1 "+3.3V" H 13650 6440 50  0000 C CNN
F 2 "" H 13650 6300 50  0001 C CNN
F 3 "" H 13650 6300 50  0001 C CNN
	1    13650 6300
	0    1    1    0   
$EndComp
$Comp
L +5V #PWR010
U 1 1 594EB4B3
P 12550 6300
F 0 "#PWR010" H 12550 6150 50  0001 C CNN
F 1 "+5V" H 12550 6440 50  0000 C CNN
F 2 "" H 12550 6300 50  0001 C CNN
F 3 "" H 12550 6300 50  0001 C CNN
	1    12550 6300
	0    -1   -1   0   
$EndComp
$Comp
L LED_ALT D1
U 1 1 594FDAB3
P 14950 6200
F 0 "D1" H 14950 6300 50  0000 C CNN
F 1 "LED_ALT" H 14950 6100 50  0000 C CNN
F 2 "LEDs:LED_D3.0mm" H 14950 6200 50  0001 C CNN
F 3 "" H 14950 6200 50  0001 C CNN
	1    14950 6200
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 594FDB4A
P 15350 6200
F 0 "R2" V 15430 6200 50  0000 C CNN
F 1 "330" V 15350 6200 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 15280 6200 50  0001 C CNN
F 3 "" H 15350 6200 50  0001 C CNN
	1    15350 6200
	0    1    1    0   
$EndComp
$Comp
L +5V #PWR011
U 1 1 594FDBD5
P 15600 6200
F 0 "#PWR011" H 15600 6050 50  0001 C CNN
F 1 "+5V" H 15600 6340 50  0000 C CNN
F 2 "" H 15600 6200 50  0001 C CNN
F 3 "" H 15600 6200 50  0001 C CNN
	1    15600 6200
	-1   0    0    1   
$EndComp
$Comp
L R R1
U 1 1 594FDDEA
P 14250 5900
F 0 "R1" V 14330 5900 50  0000 C CNN
F 1 "1k" V 14250 5900 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 14180 5900 50  0001 C CNN
F 3 "" H 14250 5900 50  0001 C CNN
	1    14250 5900
	0    1    1    0   
$EndComp
$Comp
L Q_NPN_BCE Q1
U 1 1 594FDE57
P 14500 6100
F 0 "Q1" H 14700 6150 50  0000 L CNN
F 1 "Q_NPN_BCE" H 14700 6050 50  0000 L CNN
F 2 "TO_SOT_Packages_SMD:SOT-23" H 14700 6200 50  0001 C CNN
F 3 "" H 14500 6100 50  0001 C CNN
	1    14500 6100
	0    1    1    0   
$EndComp
$Comp
L GND #PWR012
U 1 1 594FDF4A
P 14200 6200
F 0 "#PWR012" H 14200 5950 50  0001 C CNN
F 1 "GND" H 14200 6050 50  0000 C CNN
F 2 "" H 14200 6200 50  0001 C CNN
F 3 "" H 14200 6200 50  0001 C CNN
	1    14200 6200
	1    0    0    -1  
$EndComp
Text GLabel 14000 5900 0    60   Input ~ 0
LED0
$Comp
L Conn_02x04_Counter_Clockwise CRUBASE1
U 1 1 594FE925
P 13950 7950
F 0 "CRUBASE1" H 13950 8200 50  0000 C CNN
F 1 "CONN_02X04" H 13950 7700 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x04_Pitch2.54mm" H 13950 6750 50  0001 C CNN
F 3 "" H 13950 6750 50  0001 C CNN
	1    13950 7950
	1    0    0    -1  
$EndComp
Text GLabel 14250 7850 2    60   Output ~ 0
CRUB_0
Text GLabel 14250 7950 2    60   Output ~ 0
CRUB_1
Text GLabel 14250 8050 2    60   Output ~ 0
CRUB_2
Text GLabel 14250 8150 2    60   Output ~ 0
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
L GND #PWR013
U 1 1 594FF989
P 15100 2900
F 0 "#PWR013" H 15100 2650 50  0001 C CNN
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
F 2 "Connect:IDC_Header_Straight_10pins" H 14350 1800 50  0001 C CNN
F 3 "" H 14350 1800 50  0001 C CNN
	1    14350 3000
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR014
U 1 1 59584F63
P 2050 1100
F 0 "#PWR014" H 2050 950 50  0001 C CNN
F 1 "+5V" H 2050 1240 50  0000 C CNN
F 2 "" H 2050 1100 50  0001 C CNN
F 3 "" H 2050 1100 50  0001 C CNN
	1    2050 1100
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR015
U 1 1 59585050
P 2000 3050
F 0 "#PWR015" H 2000 2800 50  0001 C CNN
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
L C_Small C11
U 1 1 59595B0D
P 2250 1000
F 0 "C11" H 2260 1070 50  0000 L CNN
F 1 "0.1uf" H 2260 920 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 2250 1000 50  0001 C CNN
F 3 "" H 2250 1000 50  0001 C CNN
	1    2250 1000
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR016
U 1 1 59595DCD
P 2250 800
F 0 "#PWR016" H 2250 550 50  0001 C CNN
F 1 "GND" H 2250 650 50  0000 C CNN
F 2 "" H 2250 800 50  0001 C CNN
F 3 "" H 2250 800 50  0001 C CNN
	1    2250 800 
	-1   0    0    1   
$EndComp
$Comp
L C_Small C10
U 1 1 595963F1
P 10400 8550
F 0 "C10" H 10410 8620 50  0000 L CNN
F 1 "0.1uf" H 10410 8470 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 10400 8550 50  0001 C CNN
F 3 "" H 10400 8550 50  0001 C CNN
	1    10400 8550
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR017
U 1 1 5959655E
P 10250 8650
F 0 "#PWR017" H 10250 8500 50  0001 C CNN
F 1 "+5V" H 10250 8790 50  0000 C CNN
F 2 "" H 10250 8650 50  0001 C CNN
F 3 "" H 10250 8650 50  0001 C CNN
	1    10250 8650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR018
U 1 1 59596997
P 10250 10050
F 0 "#PWR018" H 10250 9800 50  0001 C CNN
F 1 "GND" H 10250 9900 50  0000 C CNN
F 2 "" H 10250 10050 50  0001 C CNN
F 3 "" H 10250 10050 50  0001 C CNN
	1    10250 10050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR019
U 1 1 59596B4F
P 10400 8400
F 0 "#PWR019" H 10400 8150 50  0001 C CNN
F 1 "GND" H 10400 8250 50  0000 C CNN
F 2 "" H 10400 8400 50  0001 C CNN
F 3 "" H 10400 8400 50  0001 C CNN
	1    10400 8400
	-1   0    0    1   
$EndComp
$Comp
L R_Small R4
U 1 1 59612E43
P 13900 2050
F 0 "R4" H 13930 2070 50  0000 L CNN
F 1 "10k" H 13930 2010 50  0000 L CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" H 13900 2050 50  0001 C CNN
F 3 "" H 13900 2050 50  0001 C CNN
	1    13900 2050
	1    0    0    -1  
$EndComp
$Comp
L R_Small R5
U 1 1 59612F26
P 14100 2050
F 0 "R5" H 14130 2070 50  0000 L CNN
F 1 "10k" H 14130 2010 50  0000 L CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" H 14100 2050 50  0001 C CNN
F 3 "" H 14100 2050 50  0001 C CNN
	1    14100 2050
	1    0    0    -1  
$EndComp
$Comp
L R_Small R6
U 1 1 59612F85
P 14300 2050
F 0 "R6" H 14330 2070 50  0000 L CNN
F 1 "10k" H 14330 2010 50  0000 L CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" H 14300 2050 50  0001 C CNN
F 3 "" H 14300 2050 50  0001 C CNN
	1    14300 2050
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR020
U 1 1 59613684
P 14450 2200
F 0 "#PWR020" H 14450 2050 50  0001 C CNN
F 1 "+3.3V" H 14450 2340 50  0000 C CNN
F 2 "" H 14450 2200 50  0001 C CNN
F 3 "" H 14450 2200 50  0001 C CNN
	1    14450 2200
	0    1    1    0   
$EndComp
$Comp
L GND #PWR021
U 1 1 596AC072
P 13600 8050
F 0 "#PWR021" H 13600 7800 50  0001 C CNN
F 1 "GND" H 13600 7900 50  0000 C CNN
F 2 "" H 13600 8050 50  0001 C CNN
F 3 "" H 13600 8050 50  0001 C CNN
	1    13600 8050
	1    0    0    -1  
$EndComp
$Comp
L C_Small C7
U 1 1 596F064F
P 8750 850
F 0 "C7" H 8760 920 50  0000 L CNN
F 1 "0.1uf" H 8760 770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 8750 850 50  0001 C CNN
F 3 "" H 8750 850 50  0001 C CNN
	1    8750 850 
	1    0    0    -1  
$EndComp
$Comp
L C_Small C8
U 1 1 596F06B9
P 9000 850
F 0 "C8" H 9010 920 50  0000 L CNN
F 1 "0.1uf" H 9010 770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 9000 850 50  0001 C CNN
F 3 "" H 9000 850 50  0001 C CNN
	1    9000 850 
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR022
U 1 1 596F06BF
P 9500 750
F 0 "#PWR022" H 9500 600 50  0001 C CNN
F 1 "+3.3V" H 9500 890 50  0000 C CNN
F 2 "" H 9500 750 50  0001 C CNN
F 3 "" H 9500 750 50  0001 C CNN
	1    9500 750 
	1    0    0    -1  
$EndComp
$Comp
L C_Small C9
U 1 1 596F06CB
P 9250 850
F 0 "C9" H 9260 920 50  0000 L CNN
F 1 "0.1uf" H 9260 770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 9250 850 50  0001 C CNN
F 3 "" H 9250 850 50  0001 C CNN
	1    9250 850 
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR023
U 1 1 596F06D1
P 9150 1200
F 0 "#PWR023" H 9150 1050 50  0001 C CNN
F 1 "+3.3V" H 9150 1340 50  0000 C CNN
F 2 "" H 9150 1200 50  0001 C CNN
F 3 "" H 9150 1200 50  0001 C CNN
	1    9150 1200
	0    1    1    0   
$EndComp
$Comp
L GND #PWR024
U 1 1 596F06D7
P 9500 950
F 0 "#PWR024" H 9500 700 50  0001 C CNN
F 1 "GND" H 9500 800 50  0000 C CNN
F 2 "" H 9500 950 50  0001 C CNN
F 3 "" H 9500 950 50  0001 C CNN
	1    9500 950 
	1    0    0    -1  
$EndComp
$Comp
L C_Small C5
U 1 1 596F0DF9
P 8250 850
F 0 "C5" H 8260 920 50  0000 L CNN
F 1 "0.1uf" H 8260 770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 8250 850 50  0001 C CNN
F 3 "" H 8250 850 50  0001 C CNN
	1    8250 850 
	1    0    0    -1  
$EndComp
$Comp
L C_Small C4
U 1 1 596F0E6D
P 8000 850
F 0 "C4" H 8010 920 50  0000 L CNN
F 1 "0.1uf" H 8010 770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 8000 850 50  0001 C CNN
F 3 "" H 8000 850 50  0001 C CNN
	1    8000 850 
	1    0    0    -1  
$EndComp
$Comp
L C_Small C3
U 1 1 596F0E7F
P 7750 850
F 0 "C3" H 7760 920 50  0000 L CNN
F 1 "0.1uf" H 7760 770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 7750 850 50  0001 C CNN
F 3 "" H 7750 850 50  0001 C CNN
	1    7750 850 
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR025
U 1 1 596F5164
P 9000 7000
F 0 "#PWR025" H 9000 6750 50  0001 C CNN
F 1 "GND" H 9000 6850 50  0000 C CNN
F 2 "" H 9000 7000 50  0001 C CNN
F 3 "" H 9000 7000 50  0001 C CNN
	1    9000 7000
	1    0    0    -1  
$EndComp
$Comp
L XC95144XL-TQ100 U1
U 1 1 596EEAA9
P 8550 4100
F 0 "U1" H 7700 6750 50  0000 C CNN
F 1 "XC95144XL-TQ100" H 9250 1450 50  0000 C CNN
F 2 "Housings_QFP:TQFP-100_14x14mm_Pitch0.5mm" H 9800 1350 50  0001 C CNN
F 3 "" H 8500 4150 50  0001 C CNN
	1    8550 4100
	1    0    0    -1  
$EndComp
$Comp
L TEST_1P T1
U 1 1 597515DC
P 14650 2800
F 0 "T1" H 14650 3070 50  0000 C CNN
F 1 "TEST_1P" H 14650 3000 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 14850 2800 50  0001 C CNN
F 3 "" H 14850 2800 50  0001 C CNN
	1    14650 2800
	1    0    0    -1  
$EndComp
$Comp
L TEST_1P T2
U 1 1 5975362C
P 10200 5600
F 0 "T2" H 10200 5870 50  0000 C CNN
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
L TEST_1P T4
U 1 1 597539A7
P 10200 5400
F 0 "T4" H 10200 5670 50  0000 C CNN
F 1 "TEST_1P" H 10200 5600 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 10400 5400 50  0001 C CNN
F 3 "" H 10400 5400 50  0001 C CNN
	1    10200 5400
	0    1    1    0   
$EndComp
$Comp
L TEST_1P T5
U 1 1 59753A11
P 10200 5300
F 0 "T5" H 10200 5570 50  0000 C CNN
F 1 "TEST_1P" H 10200 5500 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 10400 5300 50  0001 C CNN
F 3 "" H 10400 5300 50  0001 C CNN
	1    10200 5300
	0    1    1    0   
$EndComp
$Comp
L R R3
U 1 1 599E6C64
P 13600 7900
F 0 "R3" V 13680 7900 50  0000 C CNN
F 1 "1k" V 13600 7900 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 13530 7900 50  0001 C CNN
F 3 "" H 13600 7900 50  0001 C CNN
	1    13600 7900
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
P 3100 5700
F 0 "E1" H 2800 7250 60  0000 C CNN
F 1 "TiPEBEdge" V 3100 5700 60  0000 C CNN
F 2 "" H 3100 7250 60  0001 C CNN
F 3 "" H 3100 7250 60  0001 C CNN
	1    3100 5700
	1    0    0    -1  
$EndComp
Text GLabel 2550 5400 0    60   BiDi ~ 0
TI_D3
Text GLabel 3650 5500 2    60   BiDi ~ 0
TI_D2
Text GLabel 2550 5500 0    60   BiDi ~ 0
TI_D1
Text GLabel 3650 5600 2    60   BiDi ~ 0
TI_D0
Text GLabel 2550 5300 0    60   BiDi ~ 0
TI_D5
Text GLabel 3650 5400 2    60   BiDi ~ 0
TI_D4
Text GLabel 3650 5300 2    60   BiDi ~ 0
TI_D6
Text GLabel 2550 5200 0    60   BiDi ~ 0
TI_D7
$Comp
L 74HC244 U8
U 1 1 59C69B40
P 8150 9400
F 0 "U8" H 8250 10050 50  0000 L CNN
F 1 "74HC244" H 8200 8750 50  0000 L CNN
F 2 "" H 8150 9400 50  0000 C CNN
F 3 "" H 8150 9400 50  0000 C CNN
	1    8150 9400
	1    0    0    -1  
$EndComp
$Comp
L 74HC244 U7
U 1 1 59C69BE6
P 5800 9400
F 0 "U7" H 5900 10050 50  0000 L CNN
F 1 "74HC244" H 5850 8750 50  0000 L CNN
F 2 "" H 5800 9400 50  0000 C CNN
F 3 "" H 5800 9400 50  0000 C CNN
	1    5800 9400
	1    0    0    -1  
$EndComp
$Comp
L 74HC244 U6
U 1 1 59C69C7A
P 3750 9400
F 0 "U6" H 3850 10050 50  0000 L CNN
F 1 "74HC244" H 3800 8750 50  0000 L CNN
F 2 "" H 3750 9400 50  0000 C CNN
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
L GND #PWR?
U 1 1 59C6B31F
P 5500 10050
F 0 "#PWR?" H 5500 9800 50  0001 C CNN
F 1 "GND" H 5500 9900 50  0000 C CNN
F 2 "" H 5500 10050 50  0001 C CNN
F 3 "" H 5500 10050 50  0001 C CNN
	1    5500 10050
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR?
U 1 1 59C6B393
P 7850 10050
F 0 "#PWR?" H 7850 9800 50  0001 C CNN
F 1 "GND" H 7850 9900 50  0000 C CNN
F 2 "" H 7850 10050 50  0001 C CNN
F 3 "" H 7850 10050 50  0001 C CNN
	1    7850 10050
	0    -1   -1   0   
$EndComp
$Comp
L R R7
U 1 1 59C6B529
P 5350 10050
F 0 "R7" V 5430 10050 50  0000 C CNN
F 1 "1k" V 5350 10050 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 5280 10050 50  0001 C CNN
F 3 "" H 5350 10050 50  0001 C CNN
	1    5350 10050
	0    1    1    0   
$EndComp
$Comp
L R R8
U 1 1 59C6B916
P 7700 10050
F 0 "R8" V 7780 10050 50  0000 C CNN
F 1 "1k" V 7700 10050 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 7630 10050 50  0001 C CNN
F 3 "" H 7700 10050 50  0001 C CNN
	1    7700 10050
	0    1    1    0   
$EndComp
$Comp
L R R?
U 1 1 59C6CE84
P 3300 10100
F 0 "R?" V 3380 10100 50  0000 C CNN
F 1 "1k" V 3300 10100 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 3230 10100 50  0001 C CNN
F 3 "" H 3300 10100 50  0001 C CNN
	1    3300 10100
	0    1    1    0   
$EndComp
$Comp
L GND #PWR?
U 1 1 59C6CF44
P 3450 10100
F 0 "#PWR?" H 3450 9850 50  0001 C CNN
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
Text GLabel 2550 7000 0    60   Input ~ 0
TI_CRUIN
Text GLabel 3650 5700 2    60   Output ~ 0
TI_A15
Text GLabel 3650 5800 2    60   Output ~ 0
TI_A13
Text GLabel 3650 5900 2    60   Output ~ 0
TI_A11
Text GLabel 2550 5700 0    60   Output ~ 0
TI_A14
Text GLabel 2550 5800 0    60   Output ~ 0
TI_A12
Text GLabel 2550 5900 0    60   Output ~ 0
TI_A10
Text GLabel 3650 6000 2    60   Output ~ 0
TI_A9
Text GLabel 2550 6000 0    60   Output ~ 0
TI_A8
Text GLabel 3650 6100 2    60   Output ~ 0
TI_A7
Text GLabel 2550 6100 0    60   Output ~ 0
TI_A6
Text GLabel 3650 6200 2    60   Output ~ 0
TI_A5
Text GLabel 3650 6300 2    60   Output ~ 0
TI_A3
Text GLabel 3650 6400 2    60   Output ~ 0
TI_A1
Text GLabel 2550 6200 0    60   Output ~ 0
TI_A4
Text GLabel 2550 6300 0    60   Output ~ 0
TI_A2
Text GLabel 2550 6400 0    60   Output ~ 0
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
	12700 6600 13500 6600
Wire Wire Line
	12700 6600 12700 6500
Wire Wire Line
	13500 6600 13500 6500
Connection ~ 13100 6600
Wire Wire Line
	12550 6300 12800 6300
Connection ~ 12700 6300
Wire Wire Line
	13400 6300 13650 6300
Connection ~ 13500 6300
Wire Wire Line
	15100 6200 15200 6200
Wire Wire Line
	15500 6200 15600 6200
Wire Wire Line
	14700 6200 14800 6200
Wire Wire Line
	14400 5900 14500 5900
Wire Wire Line
	14300 6200 14200 6200
Wire Wire Line
	14000 5900 14100 5900
Wire Wire Line
	13750 7750 13750 8150
Connection ~ 13750 7850
Connection ~ 13750 7950
Connection ~ 13750 8050
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
	13750 7750 13600 7750
Wire Wire Line
	5200 9800 5300 9800
Wire Wire Line
	5300 9900 5200 9900
Wire Wire Line
	7550 10050 7550 9800
Wire Wire Line
	7550 9800 7650 9800
Wire Wire Line
	7650 9900 7550 9900
Connection ~ 7550 9900
Wire Wire Line
	5200 9800 5200 10050
Connection ~ 5200 9900
Text GLabel 3650 7000 2    60   Output ~ 0
TI_MEMEN
Text GLabel 3250 9000 0    60   Input ~ 0
TI_CRUCLK
Text GLabel 3250 9100 0    60   Input ~ 0
TI_PH3
Text GLabel 3250 9200 0    60   Input ~ 0
TI_DBIN
Text GLabel 2550 6500 0    60   Output ~ 0
TI_AMB
Text GLabel 2550 6800 0    60   Output ~ 0
TI_CRUCLK
Text GLabel 3650 6800 2    60   Output ~ 0
TI_DBIN
Text GLabel 3650 6700 2    60   Output ~ 0
TI_PH3
Text GLabel 1250 9650 0    60   Input ~ 0
TI_MEMEN
Text GLabel 4250 8900 2    60   Output ~ 0
B_WE
Text GLabel 3250 8900 0    60   Input ~ 0
TI_WE
Text GLabel 3650 6900 2    60   Output ~ 0
TI_WE
$Comp
L 74LS138 U5
U 1 1 59C72E85
P 1850 9300
F 0 "U5" H 1950 9800 50  0000 C CNN
F 1 "74LS138" H 2000 8751 50  0000 C CNN
F 2 "" H 1850 9300 50  0001 C CNN
F 3 "" H 1850 9300 50  0001 C CNN
	1    1850 9300
	1    0    0    -1  
$EndComp
Text GLabel 3650 6500 2    60   Output ~ 0
TI_AMA
Text GLabel 3650 6600 2    60   Output ~ 0
TI_AMC
Text GLabel 1250 8950 0    60   Input ~ 0
TI_AMA
Text GLabel 1250 9150 0    60   Input ~ 0
TI_AMC
Text GLabel 1250 9050 0    60   Input ~ 0
TI_AMB
Text GLabel 3650 4600 2    60   Output ~ 0
TI-AMD
Text GLabel 2550 4700 0    60   Output ~ 0
TI_AME
Text GLabel 1250 9550 0    60   Input ~ 0
TI_AME
Text GLabel 1250 9450 0    60   Input ~ 0
TI-AMD
Wire Wire Line
	3250 9800 3150 9800
Wire Wire Line
	3150 9800 3150 10100
$Comp
L GND #PWR?
U 1 1 59C7685F
P 1850 9750
F 0 "#PWR?" H 1850 9500 50  0001 C CNN
F 1 "GND" H 1850 9600 50  0000 C CNN
F 2 "" H 1850 9750 50  0001 C CNN
F 3 "" H 1850 9750 50  0001 C CNN
	1    1850 9750
	1    0    0    -1  
$EndComp
$Comp
L C_Small C?
U 1 1 59C76A23
P 2000 8550
F 0 "C?" H 2010 8620 50  0000 L CNN
F 1 "0.1uf" H 2010 8470 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 2000 8550 50  0001 C CNN
F 3 "" H 2000 8550 50  0001 C CNN
	1    2000 8550
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 59C76A29
P 1850 8650
F 0 "#PWR?" H 1850 8500 50  0001 C CNN
F 1 "+5V" H 1850 8790 50  0000 C CNN
F 2 "" H 1850 8650 50  0001 C CNN
F 3 "" H 1850 8650 50  0001 C CNN
	1    1850 8650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 59C76A2F
P 2000 8400
F 0 "#PWR?" H 2000 8150 50  0001 C CNN
F 1 "GND" H 2000 8250 50  0000 C CNN
F 2 "" H 2000 8400 50  0001 C CNN
F 3 "" H 2000 8400 50  0001 C CNN
	1    2000 8400
	-1   0    0    1   
$EndComp
Wire Wire Line
	2000 8650 1850 8650
Wire Wire Line
	1850 8650 1850 8850
Wire Wire Line
	2000 8450 2000 8400
Connection ~ 1850 8650
$Comp
L C_Small C?
U 1 1 59C76B96
P 3900 8500
F 0 "C?" H 3910 8570 50  0000 L CNN
F 1 "0.1uf" H 3910 8420 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 3900 8500 50  0001 C CNN
F 3 "" H 3900 8500 50  0001 C CNN
	1    3900 8500
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 59C76B9C
P 3750 8600
F 0 "#PWR?" H 3750 8450 50  0001 C CNN
F 1 "+5V" H 3750 8740 50  0000 C CNN
F 2 "" H 3750 8600 50  0001 C CNN
F 3 "" H 3750 8600 50  0001 C CNN
	1    3750 8600
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 59C76BA2
P 3900 8350
F 0 "#PWR?" H 3900 8100 50  0001 C CNN
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
L C_Small C?
U 1 1 59C76D70
P 5950 8500
F 0 "C?" H 5960 8570 50  0000 L CNN
F 1 "0.1uf" H 5960 8420 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 5950 8500 50  0001 C CNN
F 3 "" H 5950 8500 50  0001 C CNN
	1    5950 8500
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 59C76D76
P 5800 8600
F 0 "#PWR?" H 5800 8450 50  0001 C CNN
F 1 "+5V" H 5800 8740 50  0000 C CNN
F 2 "" H 5800 8600 50  0001 C CNN
F 3 "" H 5800 8600 50  0001 C CNN
	1    5800 8600
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 59C76D7C
P 5950 8350
F 0 "#PWR?" H 5950 8100 50  0001 C CNN
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
L C_Small C?
U 1 1 59C76E70
P 8300 8500
F 0 "C?" H 8310 8570 50  0000 L CNN
F 1 "0.1uf" H 8310 8420 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 8300 8500 50  0001 C CNN
F 3 "" H 8300 8500 50  0001 C CNN
	1    8300 8500
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 59C76E76
P 8150 8600
F 0 "#PWR?" H 8150 8450 50  0001 C CNN
F 1 "+5V" H 8150 8740 50  0000 C CNN
F 2 "" H 8150 8600 50  0001 C CNN
F 3 "" H 8150 8600 50  0001 C CNN
	1    8150 8600
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 59C76E7C
P 8300 8350
F 0 "#PWR?" H 8300 8100 50  0001 C CNN
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
L GND #PWR?
U 1 1 59C76F45
P 8150 10100
F 0 "#PWR?" H 8150 9850 50  0001 C CNN
F 1 "GND" H 8150 9950 50  0000 C CNN
F 2 "" H 8150 10100 50  0001 C CNN
F 3 "" H 8150 10100 50  0001 C CNN
	1    8150 10100
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 59C76FD1
P 5800 10100
F 0 "#PWR?" H 5800 9850 50  0001 C CNN
F 1 "GND" H 5800 9950 50  0000 C CNN
F 2 "" H 5800 10100 50  0001 C CNN
F 3 "" H 5800 10100 50  0001 C CNN
	1    5800 10100
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 59C7705D
P 3750 10100
F 0 "#PWR?" H 3750 9850 50  0001 C CNN
F 1 "GND" H 3750 9950 50  0000 C CNN
F 2 "" H 3750 10100 50  0001 C CNN
F 3 "" H 3750 10100 50  0001 C CNN
	1    3750 10100
	1    0    0    -1  
$EndComp
$EndSCHEMATC
