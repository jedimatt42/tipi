EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "TIPI - TI-99/4A to RPi adapter"
Date "2017-09-11"
Rev "2"
Comp "ti994a.cwfk.net"
Comment1 "github.com/jedimatt42/tipi"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L ti32ksideport:TI32kSideport J1
U 1 1 5917E4FB
P 2100 5250
F 0 "J1" H 2450 6400 60  0000 C CNN
F 1 "TI32kSideport" H 2000 6400 60  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x22_Pitch2.54mm" H 2100 6550 60  0001 C CNN
F 3 "" H 2100 6550 60  0001 C CNN
	1    2100 5250
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR01
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
L tipi-rescue:27C256 U2
U 1 1 5917F7B0
P 2100 2350
F 0 "U2" H 1950 3350 50  0000 C CNN
F 1 "27C256" H 2100 1350 50  0000 C CNN
F 2 "Housings_DIP:DIP-28_W15.24mm_Socket" H 2100 2350 50  0001 C CNN
F 3 "" H 2100 2350 50  0001 C CNN
	1    2100 2350
	1    0    0    -1  
$EndComp
$Comp
L tipi-rescue:74LS245 U3
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
L tipi-rescue:C_Small C6
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
Text GLabel 2850 4500 2    60   BiDi ~ 0
TI_D0
Text GLabel 1350 4400 0    60   BiDi ~ 0
TI_D1
Text GLabel 2850 4400 2    60   BiDi ~ 0
TI_D2
Text GLabel 1350 4300 0    60   BiDi ~ 0
TI_D3
Text GLabel 2850 4600 2    60   BiDi ~ 0
TI_D4
Text GLabel 1350 4500 0    60   BiDi ~ 0
TI_D5
Text GLabel 1350 4600 0    60   BiDi ~ 0
TI_D6
Text GLabel 1350 4700 0    60   BiDi ~ 0
TI_D7
Text GLabel 1350 4900 0    60   Output ~ 0
TI_A1
Text GLabel 1350 5100 0    60   Output ~ 0
TI_WE
Text GLabel 1350 4800 0    60   Output ~ 0
TI_MEMEN
Text GLabel 1350 5300 0    60   Output ~ 0
TI_CRUCLK
Text GLabel 1350 5400 0    60   Output ~ 0
TI_A2
Text GLabel 1350 5500 0    60   Output ~ 0
TI_A9
Text GLabel 1350 5600 0    60   Output ~ 0
TI_A14
Text GLabel 1350 5700 0    60   Output ~ 0
TI_A8
Text GLabel 1350 5900 0    60   Output ~ 0
TI_A3
Text GLabel 1350 6000 0    60   Output ~ 0
TI_A11
Text GLabel 1350 6100 0    60   Output ~ 0
TI_A10
Text GLabel 2850 4800 2    60   Output ~ 0
TI_A0
Text GLabel 2850 4900 2    60   Output ~ 0
TI_A6
$Comp
L power:GND #PWR02
U 1 1 591A49E4
P 2850 5100
F 0 "#PWR02" H 2850 4850 50  0001 C CNN
F 1 "GND" H 2850 4950 50  0000 C CNN
F 2 "" H 2850 5100 50  0001 C CNN
F 3 "" H 2850 5100 50  0001 C CNN
	1    2850 5100
	0    -1   -1   0   
$EndComp
Text GLabel 2850 5400 2    60   Output ~ 0
TI_A15
Text GLabel 2850 5500 2    60   Output ~ 0
TI_A7
Text GLabel 2850 5600 2    60   Output ~ 0
TI_A13
Text GLabel 2850 5800 2    60   Output ~ 0
TI_A12
Text GLabel 2850 6000 2    60   Output ~ 0
TI_A4
Text GLabel 2850 6100 2    60   Output ~ 0
TI_A5
$Comp
L power:+5V #PWR03
U 1 1 591A50F1
P 2700 6300
F 0 "#PWR03" H 2700 6150 50  0001 C CNN
F 1 "+5V" H 2700 6440 50  0000 C CNN
F 2 "" H 2700 6300 50  0001 C CNN
F 3 "" H 2700 6300 50  0001 C CNN
	1    2700 6300
	-1   0    0    1   
$EndComp
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
Text GLabel 4100 3100 0    60   Output ~ 0
R_RESET
Text GLabel 4100 3000 0    60   Input ~ 0
R_DC
Text GLabel 4100 3500 0    60   Input ~ 0
R_RT
Text GLabel 4100 3200 0    60   Output ~ 0
R_DIN
Text GLabel 4100 3400 0    60   Input ~ 0
R_DOUT
Text GLabel 4100 2600 0    60   Input ~ 0
R_CLK
Text GLabel 4100 3300 0    60   Input ~ 0
R_LE
Text GLabel 6500 4000 2    60   Output ~ 0
CRU0
Text GLabel 6500 6300 2    60   Input ~ 0
JTAG_TCK
Text GLabel 6500 6100 2    60   Input ~ 0
JTAG_TDI
Text GLabel 6500 6400 2    60   Output ~ 0
JTAG_TDO
Text GLabel 6500 6200 2    60   Input ~ 0
JTAG_TMS
$Comp
L tipi-rescue:AVR-JTAG-10 JTAG1
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
L power:+3.3V #PWR04
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
L power:GND #PWR05
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
L power:GND #PWR06
U 1 1 591AAD23
P 10350 1350
F 0 "#PWR06" H 10350 1100 50  0001 C CNN
F 1 "GND" H 10350 1200 50  0000 C CNN
F 2 "" H 10350 1350 50  0001 C CNN
F 3 "" H 10350 1350 50  0001 C CNN
	1    10350 1350
	1    0    0    -1  
$EndComp
Text GLabel 4100 5900 0    60   Input ~ 0
TI_A0
Text GLabel 4100 5800 0    60   Input ~ 0
TI_A1
Text GLabel 4100 5500 0    60   Input ~ 0
TI_A2
Text GLabel 6500 3400 2    60   Input ~ 0
TI_A3
Text GLabel 6500 3300 2    60   Input ~ 0
TI_A4
Text GLabel 6500 3100 2    60   Input ~ 0
TI_A5
Text GLabel 4100 5700 0    60   Input ~ 0
TI_A6
Text GLabel 4100 5200 0    60   Input ~ 0
TI_A7
Text GLabel 6500 3700 2    60   Input ~ 0
TI_A8
Text GLabel 4100 5300 0    60   Input ~ 0
TI_A9
Text GLabel 6500 3000 2    60   Input ~ 0
TI_A10
Text GLabel 6500 3200 2    60   Input ~ 0
TI_A11
Text GLabel 6500 3600 2    60   Input ~ 0
TI_A12
Text GLabel 4100 5000 0    60   Input ~ 0
TI_A13
Text GLabel 4100 5100 0    60   Input ~ 0
TI_A14
Text GLabel 4100 5400 0    60   Input ~ 0
TI_A15
Text GLabel 4100 5600 0    60   Input ~ 0
TI_WE
Text GLabel 4100 2800 0    60   Input ~ 0
TI_MEMEN
Text GLabel 6500 3500 2    60   Input ~ 0
TI_DBIN
Text GLabel 4100 3900 0    60   Input ~ 0
TI_CRUCLK
Text GLabel 2850 5900 2    60   Output ~ 0
TI_DBIN
Text GLabel 2850 4700 2    60   Input ~ 0
TI_CRUIN
Text GLabel 1400 1450 0    60   Input ~ 0
TI_A15
Text GLabel 1400 1550 0    60   Input ~ 0
TI_A14
Text GLabel 1400 1650 0    60   Input ~ 0
TI_A13
Text GLabel 1400 1750 0    60   Input ~ 0
TI_A12
Text GLabel 1400 1850 0    60   Input ~ 0
TI_A11
Text GLabel 1400 1950 0    60   Input ~ 0
TI_A10
Text GLabel 1400 2050 0    60   Input ~ 0
TI_A9
Text GLabel 1400 2150 0    60   Input ~ 0
TI_A8
Text GLabel 1400 2350 0    60   Input ~ 0
TI_A6
Text GLabel 1400 2250 0    60   Input ~ 0
TI_A7
Text GLabel 1400 2450 0    60   Input ~ 0
TI_A5
Text GLabel 1400 2550 0    60   Input ~ 0
TI_A4
Text GLabel 1400 2650 0    60   Input ~ 0
TI_A3
Text GLabel 1400 2750 0    60   Input ~ 0
DSR_B0
Text GLabel 1400 2850 0    60   Input ~ 0
DSR_B1
Text GLabel 2800 1450 2    60   3State ~ 0
TP_D0
Text GLabel 2800 1550 2    60   3State ~ 0
TP_D1
Text GLabel 2800 1650 2    60   3State ~ 0
TP_D2
Text GLabel 2800 1750 2    60   3State ~ 0
TP_D3
Text GLabel 2800 1850 2    60   3State ~ 0
TP_D4
Text GLabel 2800 1950 2    60   3State ~ 0
TP_D5
Text GLabel 2800 2050 2    60   3State ~ 0
TP_D6
Text GLabel 2800 2150 2    60   3State ~ 0
TP_D7
Text GLabel 4100 1600 0    60   3State ~ 0
TP_D0
Text GLabel 4100 1700 0    60   3State ~ 0
TP_D1
Text GLabel 4100 1800 0    60   3State ~ 0
TP_D2
Text GLabel 4100 2000 0    60   3State ~ 0
TP_D3
Text GLabel 4100 1900 0    60   3State ~ 0
TP_D4
Text GLabel 4100 2100 0    60   3State ~ 0
TP_D5
Text GLabel 4100 2200 0    60   3State ~ 0
TP_D6
Text GLabel 4100 2300 0    60   3State ~ 0
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
L power:+5V #PWR07
U 1 1 594E090D
P 1050 2950
F 0 "#PWR07" H 1050 2800 50  0001 C CNN
F 1 "+5V" H 1050 3090 50  0000 C CNN
F 2 "" H 1050 2950 50  0001 C CNN
F 3 "" H 1050 2950 50  0001 C CNN
	1    1050 2950
	-1   0    0    1   
$EndComp
Text GLabel 1300 3250 0    60   Input ~ 0
DSR_EN
Text GLabel 6500 4800 2    60   Output ~ 0
DSR_EN
Text GLabel 6500 1600 2    60   Output ~ 0
DB_EN
Text GLabel 4100 4700 0    60   Output ~ 0
DB_DIR
Text GLabel 8850 4800 0    60   Input ~ 0
DB_DIR
Text GLabel 8850 4900 0    60   Input ~ 0
DB_EN
Text GLabel 4100 4400 0    60   Output ~ 0
DSR_B0
Text GLabel 4100 4500 0    60   Output ~ 0
DSR_B1
Text GLabel 4100 2900 0    60   Output ~ 0
TI_CRUIN
$Comp
L tipi-rescue:LM1117-3.3-RESCUE-tipi U4
U 1 1 594EAE75
P 2050 6950
F 0 "U4" H 2150 6700 50  0000 C CNN
F 1 "LM1117-3.3" H 2050 7200 50  0000 C CNN
F 2 "TO_SOT_Packages_SMD:SOT-223" H 2050 6950 50  0001 C CNN
F 3 "" H 2050 6950 50  0001 C CNN
	1    2050 6950
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR08
U 1 1 594EAFBA
P 2050 7250
F 0 "#PWR08" H 2050 7000 50  0001 C CNN
F 1 "GND" H 2050 7100 50  0000 C CNN
F 2 "" H 2050 7250 50  0001 C CNN
F 3 "" H 2050 7250 50  0001 C CNN
	1    2050 7250
	1    0    0    -1  
$EndComp
$Comp
L tipi-rescue:CP1_Small C2
U 1 1 594EB02A
P 2450 7050
F 0 "C2" H 2460 7120 50  0000 L CNN
F 1 "22uf" H 2460 6970 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 2450 7050 50  0001 C CNN
F 3 "" H 2450 7050 50  0001 C CNN
	1    2450 7050
	1    0    0    -1  
$EndComp
$Comp
L tipi-rescue:CP1_Small C1
U 1 1 594EB077
P 1650 7050
F 0 "C1" H 1660 7120 50  0000 L CNN
F 1 "10uf" H 1660 6970 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 1650 7050 50  0001 C CNN
F 3 "" H 1650 7050 50  0001 C CNN
	1    1650 7050
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR09
U 1 1 594EB46B
P 2600 6950
F 0 "#PWR09" H 2600 6800 50  0001 C CNN
F 1 "+3.3V" H 2600 7090 50  0000 C CNN
F 2 "" H 2600 6950 50  0001 C CNN
F 3 "" H 2600 6950 50  0001 C CNN
	1    2600 6950
	0    1    1    0   
$EndComp
$Comp
L power:+5V #PWR010
U 1 1 594EB4B3
P 1500 6950
F 0 "#PWR010" H 1500 6800 50  0001 C CNN
F 1 "+5V" H 1500 7090 50  0000 C CNN
F 2 "" H 1500 6950 50  0001 C CNN
F 3 "" H 1500 6950 50  0001 C CNN
	1    1500 6950
	0    -1   -1   0   
$EndComp
$Comp
L tipi-rescue:LED_ALT D1
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
L tipi-rescue:R R2
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
L power:+5V #PWR011
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
L tipi-rescue:R R1
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
L tipi-rescue:Q_NPN_BCE Q1
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
L power:GND #PWR012
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
CRU0
$Comp
L tipi-rescue:CONN_02X04 CRUBASE1
U 1 1 594FE925
P 7950 6000
F 0 "CRUBASE1" H 7950 6250 50  0000 C CNN
F 1 "CONN_02X04" H 7950 5750 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x04_Pitch2.54mm" H 7950 4800 50  0001 C CNN
F 3 "" H 7950 4800 50  0001 C CNN
	1    7950 6000
	1    0    0    -1  
$EndComp
Text GLabel 8200 5850 2    60   Output ~ 0
CRUB_0
Text GLabel 8200 5950 2    60   Output ~ 0
CRUB_1
Text GLabel 8200 6050 2    60   Output ~ 0
CRUB_2
Text GLabel 8200 6150 2    60   Output ~ 0
CRUB_3
Text GLabel 6500 5600 2    60   Input ~ 0
CRUB_0
Text GLabel 6500 5700 2    60   Input ~ 0
CRUB_1
Text GLabel 6500 5800 2    60   Input ~ 0
CRUB_2
Text GLabel 6500 5900 2    60   Input ~ 0
CRUB_3
Text GLabel 1350 5200 0    60   Output ~ 0
TI_PH3
Text GLabel 4100 4200 0    60   Input ~ 0
TI_PH3
Wire Wire Line
	1350 4300 1500 4300
Wire Wire Line
	1350 4400 1500 4400
Wire Wire Line
	1350 4500 1500 4500
Wire Wire Line
	1350 4600 1500 4600
Wire Wire Line
	1350 4700 1500 4700
Wire Wire Line
	2700 4600 2850 4600
Wire Wire Line
	2700 4500 2850 4500
Wire Wire Line
	2700 4400 2850 4400
Wire Wire Line
	2700 5000 2800 5000
Wire Wire Line
	2800 5000 2800 5100
Wire Wire Line
	2800 5300 2700 5300
Wire Wire Line
	2700 5100 2800 5100
Connection ~ 2800 5100
Wire Wire Line
	2700 5200 2800 5200
Connection ~ 2800 5200
Wire Wire Line
	2700 4800 2850 4800
Wire Wire Line
	2700 4900 2850 4900
Wire Wire Line
	2700 5400 2850 5400
Wire Wire Line
	2700 5500 2850 5500
Wire Wire Line
	2700 5600 2850 5600
Wire Wire Line
	2700 5800 2850 5800
Wire Wire Line
	2700 6000 2850 6000
Wire Wire Line
	2700 6100 2850 6100
Wire Wire Line
	1500 6100 1350 6100
Wire Wire Line
	1500 6000 1350 6000
Wire Wire Line
	1500 5900 1350 5900
Wire Wire Line
	1500 5700 1350 5700
Wire Wire Line
	1500 5600 1350 5600
Wire Wire Line
	1500 5500 1350 5500
Wire Wire Line
	1500 5400 1350 5400
Wire Wire Line
	1500 5300 1350 5300
Wire Wire Line
	1500 5100 1350 5100
Wire Wire Line
	1500 4900 1350 4900
Wire Wire Line
	1500 4800 1350 4800
Wire Wire Line
	9100 950  9350 950 
Wire Wire Line
	9150 1050 9700 1050
Wire Wire Line
	9100 1150 9250 1150
Wire Wire Line
	9100 1350 9150 1350
Wire Wire Line
	9950 1350 10350 1350
Wire Wire Line
	9950 1050 10350 1050
Wire Wire Line
	9950 950  10350 950 
Wire Wire Line
	2700 5900 2850 5900
Wire Wire Line
	2700 4700 2850 4700
Wire Wire Line
	1050 2950 1400 2950
Wire Wire Line
	1400 3150 1400 3250
Wire Wire Line
	1400 3250 1300 3250
Wire Wire Line
	1650 7250 2050 7250
Wire Wire Line
	1650 7250 1650 7150
Wire Wire Line
	2450 7250 2450 7150
Connection ~ 2050 7250
Wire Wire Line
	1500 6950 1650 6950
Connection ~ 1650 6950
Wire Wire Line
	2350 6950 2450 6950
Connection ~ 2450 6950
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
	7700 5750 7700 5850
Connection ~ 7700 5850
Connection ~ 7700 5950
Connection ~ 7700 6050
$Comp
L power:GND #PWR013
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
L tipi-rescue:CONN_02X05 RPi1
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
NoConn ~ 1500 4200
NoConn ~ 2700 4200
NoConn ~ 2700 4300
NoConn ~ 2700 5700
NoConn ~ 2700 6200
NoConn ~ 1500 6300
Wire Wire Line
	1350 5200 1500 5200
NoConn ~ 1500 5800
NoConn ~ 1500 5000
Text GLabel 1350 6200 0    60   Input ~ 0
TI_EXTINT
Wire Wire Line
	1350 6200 1500 6200
Text GLabel 6500 2900 2    60   Output ~ 0
TI_EXTINT
$Comp
L power:+5V #PWR014
U 1 1 59584F63
P 2100 1300
F 0 "#PWR014" H 2100 1150 50  0001 C CNN
F 1 "+5V" H 2100 1440 50  0000 C CNN
F 2 "" H 2100 1300 50  0001 C CNN
F 3 "" H 2100 1300 50  0001 C CNN
	1    2100 1300
	1    0    0    -1  
$EndComp
Wire Wire Line
	2100 1300 2100 1350
$Comp
L power:GND #PWR015
U 1 1 59585050
P 2100 3400
F 0 "#PWR015" H 2100 3150 50  0001 C CNN
F 1 "GND" H 2100 3250 50  0000 C CNN
F 2 "" H 2100 3400 50  0001 C CNN
F 3 "" H 2100 3400 50  0001 C CNN
	1    2100 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	2100 3400 2100 3350
NoConn ~ 9950 1150
NoConn ~ 9950 1250
NoConn ~ 9700 1250
$Comp
L tipi-rescue:C_Small C11
U 1 1 59595B0D
P 2300 1200
F 0 "C11" H 2310 1270 50  0000 L CNN
F 1 "0.1uf" H 2310 1120 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 2300 1200 50  0001 C CNN
F 3 "" H 2300 1200 50  0001 C CNN
	1    2300 1200
	1    0    0    -1  
$EndComp
Wire Wire Line
	2100 1300 2300 1300
Connection ~ 2100 1300
Wire Wire Line
	2300 1100 2300 1000
$Comp
L power:GND #PWR016
U 1 1 59595DCD
P 2300 1000
F 0 "#PWR016" H 2300 750 50  0001 C CNN
F 1 "GND" H 2300 850 50  0000 C CNN
F 2 "" H 2300 1000 50  0001 C CNN
F 3 "" H 2300 1000 50  0001 C CNN
	1    2300 1000
	-1   0    0    1   
$EndComp
$Comp
L tipi-rescue:C_Small C10
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
L power:+5V #PWR017
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
L power:GND #PWR018
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
L power:GND #PWR019
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
L tipi-rescue:R_Small R4
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
L tipi-rescue:R_Small R5
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
L tipi-rescue:R_Small R6
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
L power:+3.3V #PWR020
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
	9150 1850 9350 1850
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
L power:GND #PWR021
U 1 1 596AC072
P 7550 6050
F 0 "#PWR021" H 7550 5800 50  0001 C CNN
F 1 "GND" H 7550 5900 50  0000 C CNN
F 2 "" H 7550 6050 50  0001 C CNN
F 3 "" H 7550 6050 50  0001 C CNN
	1    7550 6050
	1    0    0    -1  
$EndComp
$Comp
L tipi-rescue:C_Small C7
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
L tipi-rescue:C_Small C8
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
L power:+3.3V #PWR022
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
L tipi-rescue:C_Small C9
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
L power:+3.3V #PWR023
U 1 1 596F06D1
P 5900 1100
F 0 "#PWR023" H 5900 950 50  0001 C CNN
F 1 "+3.3V" H 5900 1240 50  0000 C CNN
F 2 "" H 5900 1100 50  0001 C CNN
F 3 "" H 5900 1100 50  0001 C CNN
	1    5900 1100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR024
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
L tipi-rescue:C_Small C5
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
L tipi-rescue:C_Small C4
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
L tipi-rescue:C_Small C3
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
	4900 1100 5000 1100
Connection ~ 5000 1100
Connection ~ 5100 1100
Connection ~ 5400 1100
Connection ~ 5500 1100
Connection ~ 5600 1100
Connection ~ 5700 1100
Wire Wire Line
	3250 7350 3500 7350
Connection ~ 3500 7350
Connection ~ 3750 7350
Connection ~ 4000 7350
Connection ~ 4250 7350
Connection ~ 4500 7350
Connection ~ 4750 7350
Wire Wire Line
	3250 7550 3500 7550
Connection ~ 3500 7550
Connection ~ 3750 7550
Connection ~ 4000 7550
Connection ~ 4250 7550
Connection ~ 4500 7550
Connection ~ 4750 7550
$Comp
L power:GND #PWR025
U 1 1 596F5164
P 5750 6900
F 0 "#PWR025" H 5750 6650 50  0001 C CNN
F 1 "GND" H 5750 6750 50  0000 C CNN
F 2 "" H 5750 6900 50  0001 C CNN
F 3 "" H 5750 6900 50  0001 C CNN
	1    5750 6900
	1    0    0    -1  
$EndComp
Wire Wire Line
	4900 6900 5000 6900
Connection ~ 5000 6900
Connection ~ 5100 6900
Connection ~ 5200 6900
Connection ~ 5300 6900
Connection ~ 5400 6900
Connection ~ 5500 6900
Connection ~ 5600 6900
$Comp
L tipi-rescue:XC95144XL-TQ100 U1
U 1 1 596EEAA9
P 5300 4000
F 0 "U1" H 4450 6650 50  0000 C CNN
F 1 "XC95144XL-TQ100" H 6000 1350 50  0000 C CNN
F 2 "Housings_QFP:TQFP-100_14x14mm_Pitch0.5mm" H 6550 1250 50  0001 C CNN
F 3 "" H 5250 4050 50  0001 C CNN
	1    5300 4000
	1    0    0    -1  
$EndComp
$Comp
L tipi-rescue:TEST_1P T1
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
L tipi-rescue:TEST_1P T2
U 1 1 5975362C
P 6950 5500
F 0 "T2" H 6950 5770 50  0000 C CNN
F 1 "TEST_1P" H 6950 5700 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 7150 5500 50  0001 C CNN
F 3 "" H 7150 5500 50  0001 C CNN
	1    6950 5500
	0    1    1    0   
$EndComp
$Comp
L tipi-rescue:TEST_1P T3
U 1 1 5975393E
P 6950 5400
F 0 "T3" H 6950 5670 50  0000 C CNN
F 1 "TEST_1P" H 6950 5600 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 7150 5400 50  0001 C CNN
F 3 "" H 7150 5400 50  0001 C CNN
	1    6950 5400
	0    1    1    0   
$EndComp
$Comp
L tipi-rescue:TEST_1P T4
U 1 1 597539A7
P 6950 5300
F 0 "T4" H 6950 5570 50  0000 C CNN
F 1 "TEST_1P" H 6950 5500 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 7150 5300 50  0001 C CNN
F 3 "" H 7150 5300 50  0001 C CNN
	1    6950 5300
	0    1    1    0   
$EndComp
$Comp
L tipi-rescue:TEST_1P T5
U 1 1 59753A11
P 6950 5200
F 0 "T5" H 6950 5470 50  0000 C CNN
F 1 "TEST_1P" H 6950 5400 50  0000 C CNN
F 2 "Wire_Pads:SolderWirePad_single_0-8mmDrill" H 7150 5200 50  0001 C CNN
F 3 "" H 7150 5200 50  0001 C CNN
	1    6950 5200
	0    1    1    0   
$EndComp
Wire Wire Line
	6500 5500 6950 5500
Wire Wire Line
	6500 5400 6950 5400
Wire Wire Line
	6500 5300 6950 5300
Wire Wire Line
	6500 5200 6950 5200
$Comp
L tipi-rescue:R R3
U 1 1 599E6C64
P 7550 5900
F 0 "R3" V 7630 5900 50  0000 C CNN
F 1 "1k" V 7550 5900 50  0000 C CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" V 7480 5900 50  0001 C CNN
F 3 "" H 7550 5900 50  0001 C CNN
	1    7550 5900
	1    0    0    -1  
$EndComp
Wire Wire Line
	7700 5750 7550 5750
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
Wire Wire Line
	2800 5100 2800 5200
Wire Wire Line
	2800 5100 2850 5100
Wire Wire Line
	2800 5200 2800 5300
Wire Wire Line
	2050 7250 2450 7250
Wire Wire Line
	1650 6950 1750 6950
Wire Wire Line
	2450 6950 2600 6950
Wire Wire Line
	7700 5850 7700 5950
Wire Wire Line
	7700 5950 7700 6050
Wire Wire Line
	7700 6050 7700 6150
Wire Wire Line
	9550 1850 9700 1850
Wire Wire Line
	9350 1850 9550 1850
Wire Wire Line
	9150 1350 9700 1350
Wire Wire Line
	9250 1150 9700 1150
Wire Wire Line
	9350 950  9700 950 
Wire Wire Line
	5000 1100 5100 1100
Wire Wire Line
	5100 1100 5400 1100
Wire Wire Line
	5400 1100 5500 1100
Wire Wire Line
	5500 1100 5600 1100
Wire Wire Line
	5600 1100 5700 1100
Wire Wire Line
	5700 1100 5900 1100
Wire Wire Line
	3500 7350 3750 7350
Wire Wire Line
	3750 7350 4000 7350
Wire Wire Line
	4000 7350 4250 7350
Wire Wire Line
	4250 7350 4500 7350
Wire Wire Line
	4500 7350 4750 7350
Wire Wire Line
	4750 7350 5000 7350
Wire Wire Line
	3500 7550 3750 7550
Wire Wire Line
	3750 7550 4000 7550
Wire Wire Line
	4000 7550 4250 7550
Wire Wire Line
	4250 7550 4500 7550
Wire Wire Line
	4500 7550 4750 7550
Wire Wire Line
	4750 7550 5000 7550
Wire Wire Line
	5000 6900 5100 6900
Wire Wire Line
	5100 6900 5200 6900
Wire Wire Line
	5200 6900 5300 6900
Wire Wire Line
	5300 6900 5400 6900
Wire Wire Line
	5400 6900 5500 6900
Wire Wire Line
	5500 6900 5600 6900
Wire Wire Line
	5600 6900 5750 6900
$EndSCHEMATC
