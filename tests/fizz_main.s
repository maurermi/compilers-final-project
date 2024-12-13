main:
.l0:
	li t0, 1
.l1:
	mv t1, t0
.l2:
	mv t0, t1
.l3:
	beq t0, zero, .l4
	j l49
.l4:
	mv t0, t1
.l49:
	mv t0, t1t0, t1, t1
.l5:
	li t2, 3
.l6:
	div t0, t0, t2
.l7:
	mv t0, t0
.l8:
	mv t0, t0
.l9:
	li t2, 3
.l10:
	mul t0, t0, t2
.l11:
	mv t2, t1
.l12:
	sub t0, t0, t2
.l13:
	mv s1, t0
.l14:
	mv t0, t1
.l15:
	li t2, 5
.l16:
	div t0, t0, t2
.l17:
	mv t0, t0
.l18:
	mv t0, t0
.l19:
	li t2, 5
.l20:
	mul t0, t0, t2
.l21:
	mv t2, t1
.l22:
	sub t0, t0, t2
.l23:
	mv t2, t0
.l24:
	beq t0, zero, .l25
	j l36
.l25:
	beq t0, zero, .l26
	j l31
.l36:
	beq t0, zero, .l37
	j l42
.l26:
	li s1, 0
.l31:
	li t2, 0
.l27:
	li t0, 1
.l28:
	sub t0, s1, t0
.l29:
	print t0
.l30:
	j .l36
.l32:
	li t0, 2
.l33:
	sub t0, t2, t0
.l34:
	print t0
.l35:
	j .l45
.l45:
	mv t1, t1
.l37:
	li t0, 0
.l42:
	mv t0, t1
.l38:
	li t2, 3
.l39:
	sub t0, t0, t2
.l40:
	print t0
.l41:
	j .l45
.l43:
	print t0
.l44:
	li t0, 0
.l46:
	li t0, 1
.l47:
	add t0, t1, t0
.l48:
	j .l2
