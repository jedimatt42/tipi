# TIPI to Raspberry PI 3 gpio pin assignments

## Key/Legend for TIPI labels

* td0-7 - Data output from TI
* rd0-7 - Data output from RPi ( the TI reads )
* tc0-7 - Control output from TI
* rc0-3 - Control output from RPi

## Pin Mapping

```
 +------+-----+---------+---Pi 3---+---------+-----+------+
 | TIPI | BCM |   Name  | Physical | Name    | BCM | TIPI |
 +------+-----+---------+----++----+---------+-----+------+
 |      |     |    3.3v |  1 || 2  | 5v      |     |      |
 | td0  |   2 |   SDA.1 |  3 || 4  | 5V      |     |      |
 | td1  |   3 |   SCL.1 |  5 || 6  | 0v      |     |      |
 | td2  |   4 | GPIO. 7 |  7 || 8  | TxD     | 14  | tc0  |
 |      |     |      0v |  9 || 10 | RxD     | 15  | tc1  |
 | td3  |  17 | GPIO. 0 | 11 || 12 | GPIO. 1 | 18  | tc2  |
 | td4  |  27 | GPIO. 2 | 13 || 14 | 0v      |     |      |
 | td5  |  22 | GPIO. 3 | 15 || 16 | GPIO. 4 | 23  | tc3  |
 |      |     |    3.3v | 17 || 18 | GPIO. 5 | 24  | tc4  |
 | td6  |  10 |    MOSI | 19 || 20 | 0v      |     |      |
 | td7  |   9 |    MISO | 21 || 22 | GPIO. 6 | 25  | tc5  |
 | rd0  |  11 |    SCLK | 23 || 24 | CE0     | 8   | tc6  |
 |      |     |      0v | 25 || 26 | CE1     | 7   | tc7  |
 | rd1  |   0 |   SDA.0 | 27 || 28 | SCL.0   | 1   | rc0  |
 | rd2  |   5 | GPIO.21 | 29 || 30 | 0v      |     |      |
 | rd3  |   6 | GPIO.22 | 31 || 32 | GPIO.26 | 12  | rc1  |
 | rd4  |  13 | GPIO.23 | 33 || 34 | 0v      |     |      |
 | rd5  |  19 | GPIO.24 | 35 || 36 | GPIO.27 | 16  | rc2  |
 | rd6  |  26 | GPIO.25 | 37 || 38 | GPIO.28 | 20  | rc3  |
 |      |     |      0v | 39 || 40 | GPIO.29 | 21  | rd7  |
 +------+-----+---------+----++----+---------+-----+------+
```

## Notes

All of the pins with BCM numbers have been tested for GPIO input with internal pull-up resister attached. 

All of the pins with BCM numbers have been tested for GPIO output as well.


