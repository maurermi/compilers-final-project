main:
.l0:
	li t0, 0
.l1:
	li s1, 1
.l2:
	li t0, 2
.l3:
	beq t0, zero, .l4
	j l11
.l4:
	div t2, t1, t0
.l11:
	div t2, t1, t0t2, t1, t0, t1, t0
.l5:
	mul t2, t2, t0
.l6:
	sub t1, t1, t2
.l7:
	beq t1, zero, .l8
	j l10
.l8:
	print t0
.l10:
	j .l3
.l9:
	j .l3
