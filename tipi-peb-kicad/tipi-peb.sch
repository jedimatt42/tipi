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
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "TIPI PEB - TI-99/4A to RPi adapter"
Date "2017-09-17"
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
P 9250 2950
F 0 "#PWR01" H 9250 2700 50  0001 C CNN
F 1 "GND" H 9250 2800 50  0000 C CNN
F 2 "" H 9250 2950 50  0001 C CNN
F 3 "" H 9250 2950 50  0001 C CNN
	1    9250 2950
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
P 9550 4400
F 0 "U3" H 9650 4975 50  0000 L BNN
F 1 "74HCT245" H 9600 3825 50  0000 L TNN
F 2 "SMD_Packages:SSOP-20" H 9550 4400 50  0001 C CNN
F 3 "" H 9550 4400 50  0001 C CNN
	1    9550 4400
	1    0    0    -1  
$EndComp
$Comp
L C_Small C6
U 1 1 5917FDFE
P 4000 7450
F 0 "C6" H 4010 7520 50  0000 L CNN
F 1 "0.1uf" H 4010 7370 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 4000 7450 50  0001 C CNN
F 3 "" H 4000 7450 50  0001 C CNN
	1    4000 7450
	1    0    0    -1  
$EndComp
Text GLabel 10250 4200 2    60   BiDi ~ 0
TI_D0
Text GLabel 10250 4100 2    60   BiDi ~ 0
TI_D1
Text GLabel 10250 4000 2    60   BiDi ~ 0
TI_D2
Text GLabel 10250 3900 2    60   BiDi ~ 0
TI_D3
Text GLabel 10250 4400 2    60   BiDi ~ 0
TI_D4
Text GLabel 10250 4300 2    60   BiDi ~ 0
TI_D5
Text GLabel 10250 4500 2    60   BiDi ~ 0
TI_D6
Text GLabel 10250 4600 2    60   BiDi ~ 0
TI_D7
Text GLabel 9400 2650 0    60   Output ~ 0
R_LE
Text GLabel 9400 2450 0    60   Output ~ 0
R_CLK
Text GLabel 9900 2650 2    60   Output ~ 0
R_DOUT
Text GLabel 9900 2750 2    60   Input ~ 0
R_DIN
Text GLabel 9400 2550 0    60   Output ~ 0
R_RT
Text GLabel 9900 2850 2    60   Output ~ 0
R_DC
Text GLabel 9400 2750 0    60   Input ~ 0
R_RESET
Text GLabel 4550 2650 0    60   Output ~ 0
R_RESET
Text GLabel 4550 2550 0    60   Input ~ 0
R_DC
Text GLabel 4550 3050 0    60   Input ~ 0
R_RT
Text GLabel 4550 2750 0    60   Output ~ 0
R_DIN
Text GLabel 4550 2950 0    60   Input ~ 0
R_DOUT
Text GLabel 4550 2150 0    60   Input ~ 0
R_CLK
Text GLabel 4550 2850 0    60   Input ~ 0
R_LE
Text GLabel 6950 3550 2    60   Output ~ 0
LED0
Text GLabel 6950 5850 2    60   Input ~ 0
JTAG_TCK
Text GLabel 6950 5650 2    60   Input ~ 0
JTAG_TDI
Text GLabel 6950 5950 2    60   Output ~ 0
JTAG_TDO
Text GLabel 6950 5750 2    60   Input ~ 0
JTAG_TMS
$Comp
L AVR-JTAG-10 JTAG1
U 1 1 591AA716
P 9900 1150
F 0 "JTAG1" H 9730 1480 50  0000 C CNN
F 1 "AVR-JTAG-10" H 9560 820 50  0000 L BNN
F 2 "Connect:IDC_Header_Straight_10pins" V 9330 1170 50  0001 C CNN
F 3 "" H 9900 1150 50  0001 C CNN
	1    9900 1150
	1    0    0    -1  
$EndComp
Text GLabel 9100 950  0    60   Output ~ 0
JTAG_TCK
Text GLabel 9150 1050 0    60   Input ~ 0
JTAG_TDO
Text GLabel 9100 1150 0    60   Output ~ 0
JTAG_TMS
Text GLabel 9100 1350 0    60   Output ~ 0
JTAG_TDI
$Comp
L +3.3V #PWR04
U 1 1 591AACD3
P 10350 1050
F 0 "#PWR04" H 10350 900 50  0001 C CNN
F 1 "+3.3V" H 10350 1190 50  0000 C CNN
F 2 "" H 10350 1050 50  0001 C CNN
F 3 "" H 10350 1050 50  0001 C CNN
	1    10350 1050
	0    1    1    0   
$EndComp
$Comp
L GND #PWR05
U 1 1 591AACFB
P 10350 950
F 0 "#PWR05" H 10350 700 50  0001 C CNN
F 1 "GND" H 10350 800 50  0000 C CNN
F 2 "" H 10350 950 50  0001 C CNN
F 3 "" H 10350 950 50  0001 C CNN
	1    10350 950 
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR06
U 1 1 591AAD23
P 10350 1350
F 0 "#PWR06" H 10350 1100 50  0001 C CNN
F 1 "GND" H 10350 1200 50  0000 C CNN
F 2 "" H 10350 1350 50  0001 C CNN
F 3 "" H 10350 1350 50  0001 C CNN
	1    10350 1350
	1    0    0    -1  
$EndComp
Text GLabel 4550 5450 0    60   Input ~ 0
B_A0
Text GLabel 4550 5350 0    60   Input ~ 0
B_A1
Text GLabel 4550 5050 0    60   Input ~ 0
B_A2
Text GLabel 6950 2950 2    60   Input ~ 0
B_A3
Text GLabel 6950 2850 2    60   Input ~ 0
B_A4
Text GLabel 6950 2650 2    60   Input ~ 0
B_A5
Text GLabel 4550 5250 0    60   Input ~ 0
B_A6
Text GLabel 4550 4750 0    60   Input ~ 0
B_A7
Text GLabel 6950 3250 2    60   Input ~ 0
B_A8
Text GLabel 4550 4850 0    60   Input ~ 0
B_A9
Text GLabel 6950 2550 2    60   Input ~ 0
B_A10
Text GLabel 6950 2750 2    60   Input ~ 0
B_A11
Text GLabel 6950 3150 2    60   Input ~ 0
B_A12
Text GLabel 4550 4550 0    60   Input ~ 0
B_A13
Text GLabel 4550 4650 0    60   Input ~ 0
B_A14
Text GLabel 4550 4950 0    60   Input ~ 0
B_A15
Text GLabel 4550 5150 0    60   Input ~ 0
B_WE
Text GLabel 4550 2350 0    60   Input ~ 0
B_MEMEN
Text GLabel 6950 3050 2    60   Input ~ 0
B_DBIN
Text GLabel 4550 3450 0    60   Input ~ 0
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
Text GLabel 4550 1150 0    60   3State ~ 0
TP_D0
Text GLabel 4550 1250 0    60   3State ~ 0
TP_D1
Text GLabel 4550 1350 0    60   3State ~ 0
TP_D2
Text GLabel 4550 1550 0    60   3State ~ 0
TP_D3
Text GLabel 4550 1450 0    60   3State ~ 0
TP_D4
Text GLabel 4550 1650 0    60   3State ~ 0
TP_D5
Text GLabel 4550 1750 0    60   3State ~ 0
TP_D6
Text GLabel 4550 1850 0    60   3State ~ 0
TP_D7
Text GLabel 8850 4600 0    60   3State ~ 0
TP_D0
Text GLabel 8850 4500 0    60   3State ~ 0
TP_D1
Text GLabel 8850 4300 0    60   3State ~ 0
TP_D2
Text GLabel 8850 4400 0    60   3State ~ 0
TP_D3
Text GLabel 8850 3900 0    60   3State ~ 0
TP_D4
Text GLabel 8850 4000 0    60   3State ~ 0
TP_D5
Text GLabel 8850 4100 0    60   3State ~ 0
TP_D6
Text GLabel 8850 4200 0    60   3State ~ 0
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
Text GLabel 6950 4350 2    60   Output ~ 0
DSR_EN
Text GLabel 6950 1150 2    60   Output ~ 0
DB_EN
Text GLabel 4550 4250 0    60   Output ~ 0
DB_DIR
Text GLabel 8850 4800 0    60   Input ~ 0
DB_DIR
Text GLabel 8850 4900 0    60   Input ~ 0
DB_EN
Text GLabel 4550 3950 0    60   Output ~ 0
DSR_B0
Text GLabel 4550 4050 0    60   Output ~ 0
DSR_B1
Text GLabel 4550 2450 0    60   Output ~ 0
B_CRUIN
$Comp
L LM1117-3.3 U4
U 1 1 594EAE75
P 8350 5950
F 0 "U4" H 8450 5700 50  0000 C CNN
F 1 "LM1117-3.3" H 8350 6200 50  0000 C CNN
F 2 "TO_SOT_Packages_SMD:SOT-223" H 8350 5950 50  0001 C CNN
F 3 "" H 8350 5950 50  0001 C CNN
	1    8350 5950
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR08
U 1 1 594EAFBA
P 8350 6250
F 0 "#PWR08" H 8350 6000 50  0001 C CNN
F 1 "GND" H 8350 6100 50  0000 C CNN
F 2 "" H 8350 6250 50  0001 C CNN
F 3 "" H 8350 6250 50  0001 C CNN
	1    8350 6250
	1    0    0    -1  
$EndComp
$Comp
L CP1_Small C2
U 1 1 594EB02A
P 8750 6050
F 0 "C2" H 8760 6120 50  0000 L CNN
F 1 "22uf" H 8760 5970 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 8750 6050 50  0001 C CNN
F 3 "" H 8750 6050 50  0001 C CNN
	1    8750 6050
	1    0    0    -1  
$EndComp
$Comp
L CP1_Small C1
U 1 1 594EB077
P 7950 6050
F 0 "C1" H 7960 6120 50  0000 L CNN
F 1 "10uf" H 7960 5970 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 7950 6050 50  0001 C CNN
F 3 "" H 7950 6050 50  0001 C CNN
	1    7950 6050
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR09
U 1 1 594EB46B
P 8900 5950
F 0 "#PWR09" H 8900 5800 50  0001 C CNN
F 1 "+3.3V" H 8900 6090 50  0000 C CNN
F 2 "" H 8900 5950 50  0001 C CNN
F 3 "" H 8900 5950 50  0001 C CNN
	1    8900 5950
	0    1    1    0   
$EndComp
$Comp
L +5V #PWR010
U 1 1 594EB4B3
P 7800 5950
F 0 "#PWR010" H 7800 5800 50  0001 C CNN
F 1 "+5V" H 7800 6090 50  0000 C CNN
F 2 "" H 7800 5950 50  0001 C CNN
F 3 "" H 7800 5950 50  0001 C CNN
	1    7800 5950
	0    -1   -1   0   
$EndComp
$Comp
L LED_ALT D1
U 1 1 594FDAB3
P 10200 5850
F 0 "D1" H 10200 5950 50  0000 C CNN
F 1 "LED_ALT" H 10200 5750 50  0000 C CNN
F 2 "LEDs:LED_D3.0mm" H 10200 5850 50  0001 C CNN
F 3 "" H 10200 5850 50  0001 C CNN
	1    10200 5850
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 594FDB4A
P 10600 5850
F 0 "R2" V 10680 5850 50  0000 C CNN
F 1 "330" V 10600 5850 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 10530 5850 50  0001 C CNN
F 3 "" H 10600 5850 50  0001 C CNN
	1    10600 5850
	0    1    1    0   
$EndComp
$Comp
L +5V #PWR011
U 1 1 594FDBD5
P 10850 5850
F 0 "#PWR011" H 10850 5700 50  0001 C CNN
F 1 "+5V" H 10850 5990 50  0000 C CNN
F 2 "" H 10850 5850 50  0001 C CNN
F 3 "" H 10850 5850 50  0001 C CNN
	1    10850 5850
	-1   0    0    1   
$EndComp
$Comp
L R R1
U 1 1 594FDDEA
P 9500 5550
F 0 "R1" V 9580 5550 50  0000 C CNN
F 1 "1k" V 9500 5550 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 9430 5550 50  0001 C CNN
F 3 "" H 9500 5550 50  0001 C CNN
	1    9500 5550
	0    1    1    0   
$EndComp
$Comp
L Q_NPN_BCE Q1
U 1 1 594FDE57
P 9750 5750
F 0 "Q1" H 9950 5800 50  0000 L CNN
F 1 "Q_NPN_BCE" H 9950 5700 50  0000 L CNN
F 2 "TO_SOT_Packages_SMD:SOT-23" H 9950 5850 50  0001 C CNN
F 3 "" H 9750 5750 50  0001 C CNN
	1    9750 5750
	0    1    1    0   
$EndComp
$Comp
L GND #PWR012
U 1 1 594FDF4A
P 9450 5850
F 0 "#PWR012" H 9450 5600 50  0001 C CNN
F 1 "GND" H 9450 5700 50  0000 C CNN
F 2 "" H 9450 5850 50  0001 C CNN
F 3 "" H 9450 5850 50  0001 C CNN
	1    9450 5850
	1    0    0    -1  
$EndComp
Text GLabel 9250 5550 0    60   Input ~ 0
LED0
$Comp
L CONN_02X04 CRUBASE1
U 1 1 594FE925
P 6000 7450
F 0 "CRUBASE1" H 6000 7700 50  0000 C CNN
F 1 "CONN_02X04" H 6000 7200 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x04_Pitch2.54mm" H 6000 6250 50  0001 C CNN
F 3 "" H 6000 6250 50  0001 C CNN
	1    6000 7450
	1    0    0    -1  
$EndComp
Text GLabel 6250 7300 2    60   Output ~ 0
CRUB_0
Text GLabel 6250 7400 2    60   Output ~ 0
CRUB_1
Text GLabel 6250 7500 2    60   Output ~ 0
CRUB_2
Text GLabel 6250 7600 2    60   Output ~ 0
CRUB_3
Text GLabel 6950 5150 2    60   Input ~ 0
CRUB_0
Text GLabel 6950 5250 2    60   Input ~ 0
CRUB_1
Text GLabel 6950 5350 2    60   Input ~ 0
CRUB_2
Text GLabel 6950 5450 2    60   Input ~ 0
CRUB_3
Text GLabel 4550 3750 0    60   Input ~ 0
B_PH3
Wire Wire Line
	9100 950  9700 950 
Wire Wire Line
	9150 1050 9700 1050
Wire Wire Line
	9100 1150 9700 1150
Wire Wire Line
	9100 1350 9700 1350
Wire Wire Line
	9950 1350 10350 1350
Wire Wire Line
	9950 1050 10350 1050
Wire Wire Line
	9950 950  10350 950 
Wire Wire Line
	1000 2700 1350 2700
Wire Wire Line
	1350 2900 1350 3000
Wire Wire Line
	1350 3000 1250 3000
Wire Wire Line
	7950 6250 8750 6250
Wire Wire Line
	7950 6250 7950 6150
Wire Wire Line
	8750 6250 8750 6150
Connection ~ 8350 6250
Wire Wire Line
	7800 5950 8050 5950
Connection ~ 7950 5950
Wire Wire Line
	8650 5950 8900 5950
Connection ~ 8750 5950
Wire Wire Line
	10350 5850 10450 5850
Wire Wire Line
	10750 5850 10850 5850
Wire Wire Line
	9950 5850 10050 5850
Wire Wire Line
	9650 5550 9750 5550
Wire Wire Line
	9550 5850 9450 5850
Wire Wire Line
	9250 5550 9350 5550
Wire Wire Line
	5750 7200 5750 7600
Connection ~ 5750 7300
Connection ~ 5750 7400
Connection ~ 5750 7500
$Comp
L GND #PWR013
U 1 1 594FF989
P 10350 2550
F 0 "#PWR013" H 10350 2300 50  0001 C CNN
F 1 "GND" H 10350 2400 50  0000 C CNN
F 2 "" H 10350 2550 50  0001 C CNN
F 3 "" H 10350 2550 50  0001 C CNN
	1    10350 2550
	-1   0    0    1   
$EndComp
$Comp
L CONN_02X05 RPi1
U 1 1 594FFC97
P 9650 2650
F 0 "RPi1" H 9650 2950 50  0000 C CNN
F 1 "RPI_CONN_02X05" H 9650 2350 50  0000 C CNN
F 2 "Connect:IDC_Header_Straight_10pins" H 9650 1450 50  0001 C CNN
F 3 "" H 9650 1450 50  0001 C CNN
	1    9650 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	9250 2950 9250 2850
Wire Wire Line
	9250 2850 9400 2850
Wire Wire Line
	9900 2550 10350 2550
Text GLabel 6950 2450 2    60   Output ~ 0
B_EXTINT
$Comp
L +5V #PWR014
U 1 1 59584F63
P 2050 1050
F 0 "#PWR014" H 2050 900 50  0001 C CNN
F 1 "+5V" H 2050 1190 50  0000 C CNN
F 2 "" H 2050 1050 50  0001 C CNN
F 3 "" H 2050 1050 50  0001 C CNN
	1    2050 1050
	1    0    0    -1  
$EndComp
Wire Wire Line
	2050 1050 2050 1100
$Comp
L GND #PWR015
U 1 1 59585050
P 2050 3150
F 0 "#PWR015" H 2050 2900 50  0001 C CNN
F 1 "GND" H 2050 3000 50  0000 C CNN
F 2 "" H 2050 3150 50  0001 C CNN
F 3 "" H 2050 3150 50  0001 C CNN
	1    2050 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	2050 3150 2050 3100
NoConn ~ 9950 1150
NoConn ~ 9950 1250
NoConn ~ 9700 1250
$Comp
L C_Small C11
U 1 1 59595B0D
P 2250 950
F 0 "C11" H 2260 1020 50  0000 L CNN
F 1 "0.1uf" H 2260 870 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 2250 950 50  0001 C CNN
F 3 "" H 2250 950 50  0001 C CNN
	1    2250 950 
	1    0    0    -1  
$EndComp
Wire Wire Line
	2050 1050 2250 1050
Connection ~ 2050 1050
Wire Wire Line
	2250 850  2250 750 
$Comp
L GND #PWR016
U 1 1 59595DCD
P 2250 750
F 0 "#PWR016" H 2250 500 50  0001 C CNN
F 1 "GND" H 2250 600 50  0000 C CNN
F 2 "" H 2250 750 50  0001 C CNN
F 3 "" H 2250 750 50  0001 C CNN
	1    2250 750 
	-1   0    0    1   
$EndComp
$Comp
L C_Small C10
U 1 1 595963F1
P 9700 3550
F 0 "C10" H 9710 3620 50  0000 L CNN
F 1 "0.1uf" H 9710 3470 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 9700 3550 50  0001 C CNN
F 3 "" H 9700 3550 50  0001 C CNN
	1    9700 3550
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR017
U 1 1 5959655E
P 9550 3650
F 0 "#PWR017" H 9550 3500 50  0001 C CNN
F 1 "+5V" H 9550 3790 50  0000 C CNN
F 2 "" H 9550 3650 50  0001 C CNN
F 3 "" H 9550 3650 50  0001 C CNN
	1    9550 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	9700 3650 9550 3650
Wire Wire Line
	9550 3650 9550 3850
$Comp
L GND #PWR018
U 1 1 59596997
P 9550 5050
F 0 "#PWR018" H 9550 4800 50  0001 C CNN
F 1 "GND" H 9550 4900 50  0000 C CNN
F 2 "" H 9550 5050 50  0001 C CNN
F 3 "" H 9550 5050 50  0001 C CNN
	1    9550 5050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR019
U 1 1 59596B4F
P 9700 3400
F 0 "#PWR019" H 9700 3150 50  0001 C CNN
F 1 "GND" H 9700 3250 50  0000 C CNN
F 2 "" H 9700 3400 50  0001 C CNN
F 3 "" H 9700 3400 50  0001 C CNN
	1    9700 3400
	-1   0    0    1   
$EndComp
Wire Wire Line
	9700 3450 9700 3400
Wire Wire Line
	9550 5050 9550 4950
Connection ~ 9550 3650
$Comp
L R_Small R4
U 1 1 59612E43
P 9150 1700
F 0 "R4" H 9180 1720 50  0000 L CNN
F 1 "10k" H 9180 1660 50  0000 L CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" H 9150 1700 50  0001 C CNN
F 3 "" H 9150 1700 50  0001 C CNN
	1    9150 1700
	1    0    0    -1  
$EndComp
$Comp
L R_Small R5
U 1 1 59612F26
P 9350 1700
F 0 "R5" H 9380 1720 50  0000 L CNN
F 1 "10k" H 9380 1660 50  0000 L CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" H 9350 1700 50  0001 C CNN
F 3 "" H 9350 1700 50  0001 C CNN
	1    9350 1700
	1    0    0    -1  
$EndComp
$Comp
L R_Small R6
U 1 1 59612F85
P 9550 1700
F 0 "R6" H 9580 1720 50  0000 L CNN
F 1 "10k" H 9580 1660 50  0000 L CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" H 9550 1700 50  0001 C CNN
F 3 "" H 9550 1700 50  0001 C CNN
	1    9550 1700
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR020
U 1 1 59613684
P 9700 1850
F 0 "#PWR020" H 9700 1700 50  0001 C CNN
F 1 "+3.3V" H 9700 1990 50  0000 C CNN
F 2 "" H 9700 1850 50  0001 C CNN
F 3 "" H 9700 1850 50  0001 C CNN
	1    9700 1850
	0    1    1    0   
$EndComp
Wire Wire Line
	9150 1850 9700 1850
Wire Wire Line
	9550 1850 9550 1800
Wire Wire Line
	9350 1850 9350 1800
Connection ~ 9550 1850
Wire Wire Line
	9150 1850 9150 1800
Connection ~ 9350 1850
Wire Wire Line
	9150 1600 9150 1350
Connection ~ 9150 1350
Wire Wire Line
	9350 1600 9250 1600
Wire Wire Line
	9250 1600 9250 1150
Connection ~ 9250 1150
Wire Wire Line
	9550 1600 9450 1600
Wire Wire Line
	9450 1600 9450 1500
Wire Wire Line
	9450 1500 9350 1500
Wire Wire Line
	9350 1500 9350 950 
Connection ~ 9350 950 
$Comp
L GND #PWR021
U 1 1 596AC072
P 5600 7500
F 0 "#PWR021" H 5600 7250 50  0001 C CNN
F 1 "GND" H 5600 7350 50  0000 C CNN
F 2 "" H 5600 7500 50  0001 C CNN
F 3 "" H 5600 7500 50  0001 C CNN
	1    5600 7500
	1    0    0    -1  
$EndComp
$Comp
L C_Small C7
U 1 1 596F064F
P 4250 7450
F 0 "C7" H 4260 7520 50  0000 L CNN
F 1 "0.1uf" H 4260 7370 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 4250 7450 50  0001 C CNN
F 3 "" H 4250 7450 50  0001 C CNN
	1    4250 7450
	1    0    0    -1  
$EndComp
$Comp
L C_Small C8
U 1 1 596F06B9
P 4500 7450
F 0 "C8" H 4510 7520 50  0000 L CNN
F 1 "0.1uf" H 4510 7370 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 4500 7450 50  0001 C CNN
F 3 "" H 4500 7450 50  0001 C CNN
	1    4500 7450
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR022
U 1 1 596F06BF
P 5000 7350
F 0 "#PWR022" H 5000 7200 50  0001 C CNN
F 1 "+3.3V" H 5000 7490 50  0000 C CNN
F 2 "" H 5000 7350 50  0001 C CNN
F 3 "" H 5000 7350 50  0001 C CNN
	1    5000 7350
	1    0    0    -1  
$EndComp
$Comp
L C_Small C9
U 1 1 596F06CB
P 4750 7450
F 0 "C9" H 4760 7520 50  0000 L CNN
F 1 "0.1uf" H 4760 7370 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 4750 7450 50  0001 C CNN
F 3 "" H 4750 7450 50  0001 C CNN
	1    4750 7450
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR023
U 1 1 596F06D1
P 6350 650
F 0 "#PWR023" H 6350 500 50  0001 C CNN
F 1 "+3.3V" H 6350 790 50  0000 C CNN
F 2 "" H 6350 650 50  0001 C CNN
F 3 "" H 6350 650 50  0001 C CNN
	1    6350 650 
	0    1    1    0   
$EndComp
$Comp
L GND #PWR024
U 1 1 596F06D7
P 5000 7550
F 0 "#PWR024" H 5000 7300 50  0001 C CNN
F 1 "GND" H 5000 7400 50  0000 C CNN
F 2 "" H 5000 7550 50  0001 C CNN
F 3 "" H 5000 7550 50  0001 C CNN
	1    5000 7550
	1    0    0    -1  
$EndComp
$Comp
L C_Small C5
U 1 1 596F0DF9
P 3750 7450
F 0 "C5" H 3760 7520 50  0000 L CNN
F 1 "0.1uf" H 3760 7370 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 3750 7450 50  0001 C CNN
F 3 "" H 3750 7450 50  0001 C CNN
	1    3750 7450
	1    0    0    -1  
$EndComp
$Comp
L C_Small C4
U 1 1 596F0E6D
P 3500 7450
F 0 "C4" H 3510 7520 50  0000 L CNN
F 1 "0.1uf" H 3510 7370 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 3500 7450 50  0001 C CNN
F 3 "" H 3500 7450 50  0001 C CNN
	1    3500 7450
	1    0    0    -1  
$EndComp
$Comp
L C_Small C3
U 1 1 596F0E7F
P 3250 7450
F 0 "C3" H 3260 7520 50  0000 L CNN
F 1 "0.1uf" H 3260 7370 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 3250 7450 50  0001 C CNN
F 3 "" H 3250 7450 50  0001 C CNN
	1    3250 7450
	1    0    0    -1  
$EndComp
Wire Wire Line
	5350 650  6350 650 
Connection ~ 5450 650 
Connection ~ 5550 650 
Connection ~ 5850 650 
Connection ~ 5950 650 
Connection ~ 6050 650 
Connection ~ 6150 650 
Wire Wire Line
	3250 7350 5000 7350
Connection ~ 3500 7350
Connection ~ 3750 7350
Connection ~ 4000 7350
Connection ~ 4250 7350
Connection ~ 4500 7350
Connection ~ 4750 7350
Wire Wire Line
	3250 7550 5000 7550
Connection ~ 3500 7550
Connection ~ 3750 7550
Connection ~ 4000 7550
Connection ~ 4250 7550
Connection ~ 4500 7550
Connection ~ 4750 7550
$Comp
L GND #PWR025
U 1 1 596F5164
P 6200 6450
F 0 "#PWR025" H 6200 6200 50  0001 C CNN
F 1 "GND" H 6200 6300 50  0000 C CNN
F 2 "" H 6200 6450 50  0001 C CNN
F 3 "" H 6200 6450 50  0001 C CNN
	1    6200 6450
	1    0    0    -1  
$EndComp
Wire Wire Line
	5350 6450 6200 6450
Connection ~ 5450 6450
Connection ~ 5550 6450
Connection ~ 5650 6450
Connection ~ 5750 6450
Connection ~ 5850 6450
Connection ~ 5950 6450
Connection ~ 6050 6450
$Comp
L XC95144XL-TQ100 U1
U 1 1 596EEAA9
P 5750 3550
F 0 "U1" H 4900 6200 50  0000 C CNN
F 1 "XC95144XL-TQ100" H 6450 900 50  0000 C CNN
F 2 "Housings_QFP:TQFP-100_14x14mm_Pitch0.5mm" H 7000 800 50  0001 C CNN
F 3 "" H 5700 3600 50  0001 C CNN
	1    5750 3550
	1    0    0    -1  
$EndComp
$Comp
L TEST_1P T1
U 1 1 597515DC
P 9900 2450
F 0 "T1" H 9900 2720 50  0000 C CNN
F 1 "TEST_1P" H 9900 2650 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 10100 2450 50  0001 C CNN
F 3 "" H 10100 2450 50  0001 C CNN
	1    9900 2450
	1    0    0    -1  
$EndComp
$Comp
L TEST_1P T2
U 1 1 5975362C
P 7400 5050
F 0 "T2" H 7400 5320 50  0000 C CNN
F 1 "TEST_1P" H 7400 5250 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 7600 5050 50  0001 C CNN
F 3 "" H 7600 5050 50  0001 C CNN
	1    7400 5050
	0    1    1    0   
$EndComp
$Comp
L TEST_1P T3
U 1 1 5975393E
P 7400 4950
F 0 "T3" H 7400 5220 50  0000 C CNN
F 1 "TEST_1P" H 7400 5150 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 7600 4950 50  0001 C CNN
F 3 "" H 7600 4950 50  0001 C CNN
	1    7400 4950
	0    1    1    0   
$EndComp
$Comp
L TEST_1P T4
U 1 1 597539A7
P 7400 4850
F 0 "T4" H 7400 5120 50  0000 C CNN
F 1 "TEST_1P" H 7400 5050 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 7600 4850 50  0001 C CNN
F 3 "" H 7600 4850 50  0001 C CNN
	1    7400 4850
	0    1    1    0   
$EndComp
$Comp
L TEST_1P T5
U 1 1 59753A11
P 7400 4750
F 0 "T5" H 7400 5020 50  0000 C CNN
F 1 "TEST_1P" H 7400 4950 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 7600 4750 50  0001 C CNN
F 3 "" H 7600 4750 50  0001 C CNN
	1    7400 4750
	0    1    1    0   
$EndComp
Wire Wire Line
	6950 5050 7400 5050
Wire Wire Line
	6950 4950 7400 4950
Wire Wire Line
	6950 4850 7400 4850
Wire Wire Line
	6950 4750 7400 4750
$Comp
L R R3
U 1 1 599E6C64
P 5600 7350
F 0 "R3" V 5680 7350 50  0000 C CNN
F 1 "1k" V 5600 7350 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 5530 7350 50  0001 C CNN
F 3 "" H 5600 7350 50  0001 C CNN
	1    5600 7350
	1    0    0    -1  
$EndComp
Wire Wire Line
	5750 7200 5600 7200
Text Notes 8550 2800 0    60   ~ 0
GPIO_26
Text Notes 8550 2700 0    60   ~ 0
GPIO_19
Text Notes 8550 2600 0    60   ~ 0
GPIO_13
Text Notes 8550 2500 0    60   ~ 0
GPIO_6
Text Notes 10500 2500 0    60   ~ 0
GPIO_12
Text Notes 10350 2700 0    60   ~ 0
GPIO_16
Text Notes 10350 2800 0    60   ~ 0
GPIO_20
Text Notes 10350 2900 0    60   ~ 0
GPIO_21
$Comp
L TiPEBEdge E1
U 1 1 59BEF870
P 2050 5300
F 0 "E1" H 1750 6850 60  0000 C CNN
F 1 "TiPEBEdge" V 2050 5300 60  0000 C CNN
F 2 "" H 2050 6850 60  0001 C CNN
F 3 "" H 2050 6850 60  0001 C CNN
	1    2050 5300
	1    0    0    -1  
$EndComp
$EndSCHEMATC
