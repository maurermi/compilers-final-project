main:
.l0:
	li t0, 0
.l1:
	li s2, 10
.l2:
	li t1, 0
.l3:
	call t2, s1
.l4:
	div s1, s1, s2
.l5:
	add t1, t1, t2
.l6:
	print t1
.l7:
	beq t2, zero, .l11
	j l8
.l11:
	beq t0, zero, .l12
	j l3
.l8:
	call t2, t1
.l9:
	div t1, t1, s2
.l10:
	j .l6
.l12:
	print t1
