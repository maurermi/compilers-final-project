main:
.l0:
	li t0, 10
.l1:
	li t0, 0
.l2:
	li s1, 1
.l3:
	li t0, 1
.l4:
	beq t2, zero, .l5
	j l10
.l5:
	call t0, t0, t0
.l10:
	sub t0, t0, s1
.l6:
	div t0, t1, t0
.l7:
	beq t0, zero, .l8
	j l9
.l8:
	j .l5
.l9:
	j .l5
.l11:
	call t0, t1, t0
.l12:
	print t0
