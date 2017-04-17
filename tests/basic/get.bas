10 INPUT "Hostname: ":HOST$
20 INPUT "Port: ":PORT$
21 CR$ = CHR$(13)
22 LF$ = CHR$(10)
30 OPEN #1:"TIPI.TCP="&HOST$&":"&PORT$,DISPLAY,VARIABLE
40 PRINT #1:"GET / HTTP/1.0";CR$;LF$;
50 PRINT #1:"Accept: text/plain, text/html, text/*";CR$;LF$;
60 PRINT #1:CR$;LF$;
100 INPUT #1:L$
110 PRINT L$;
120 GOTO 100

