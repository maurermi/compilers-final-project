main:
.l0:
	mv t1, s1
.l1:
	beq t2, zero, .l2
	j l3
.l2:
	j .l3
.l3:
	call t0, t1, t0
.l4:
	call t2, t1, s1
.l5:
	li s1, 0
.l6:
	sub t0, t0, s1
.l7:
	sub t2, t2, s1
.l8:
	beq t0, zero, .l9
	j l10
.l9:
	j .l12
.l10:
	li t0, 1
.l12:
	li t0, 1t0, 1
.l11:
	j .l3
