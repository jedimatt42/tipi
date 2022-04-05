# Low Level Testing

on the raspberry pi stop the tipi and tipiwatchdog services:

```
sudo systemctl stop tipi.service
sudo systemctl stop tipiwatchdog.service
```

go to the tipi services folder and enter into the virtual env:

```
cd ~/tipi/services
. ENV/bin/activate
```

Boot your 4A/Geneve and go to MiniMem and enter Easy Bug

Then on the PI start the diagnostic tool:

```
export TIPI_SIG_DELAY=100
python TipiDebug.py
```

It will print out that it is setting some addresses on the TI
to specific values.

It then loops every 5 seconds and prints the values of memory
addresses it can read from the TI.

Check those addresses in EasyBug. If your crubase is >1000:

At the '?' prompt enter the cru command: 'C1000' and press enter.
then enter '1', and '.', the transcript will look like:
(you might want C1100 or whatever crubase your TIPI is set to)

```
?C1000
 C1000  =00  -> 1
 C1001  =01  -> .
```

Now, investigate the values set by the PI test tool:
Enter "M5FF9" and press enter 4 times. Transcript:

```
?M5FF9
 M5FF9  = 5A  ->
 M5FFA  = 00  ->
 M5FFB  = A5  ->
 M5FFC  = 00  ->
```

The tool should be printing on the PI the output of the 
addresses 5FFD and 5FFF, so go down to 5FFD by pressing
enter again, and then set the value to '81', enter again
to skip to 5FFF, and set the value to 'FF'

Transcript in Easy bug will look like:

```
 M5FFD  =00  -> 81
 M5FFE  =00  ->
 M5FFF  =00  -> FF
 M6000  =AA  ->
```

On the PI you should see your 81 and FF values show up.

Likely output on the PI will look like (if it's working)

```
wrote M5FF9: 0x5A, M5FFB: 0xA5
read M5FFD: 0x00, M5FFF: 0x0
...
read M5FFD: 0x81, M5FFF: 0xff
...
```

This is as low as we can go without a signal analyzer.

If you get some muddled values back, you can try 
increasing the value of TIPI_SIG_DELAY and rerun
the script.

