# Assembly Notes

## Byte operations

Byte varieties of instructions end in B. They operate on the left byte of a register, or the address specified indirect operands.

## Status register

Impacts behavior of various jump instructions.
C - Compare instruction sets, as do others...  

## Immediate instructions

1st operand is destination, 2nd value

```
LI R0,>0400   ; store >0400 in register 0. 
```

## Indexed addressing

```
MOV @CONST(R1),__	; mov word from CONST + R1 to dst
```

## Auto incrementing

```
MOVB @VDPR,*R4+	; mov byte from ioport VDPR to where R4 points, and increment R4
```

byte operations increment by 1, word operations by 2.

# Operations

## A - Add words

```
	A	R0,R1		; R1 = R1 + R0
	A	@3(R0),R1	; R1 = R1 + R0[3]
```

* Status: Compare sum to >0000







