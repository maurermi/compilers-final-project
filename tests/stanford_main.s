main:
.l0:
	li t2, 0
.l1:
	li s2, 1
.l2:
	li s1, 2
.l3:
	li t1, 3
.l4:
	li t0, 4
.l5:
	add t0, s2, t0
.l6:
	add t1, s1, t1
.l7:
	add t1, s1, t1
.l8:
	beq t2, zero, .l9
	j l10
.l9:
	j .l11
.l10:
	add t0, t0, t1
.l11:
	mv t0, t0
.l12:
	mv a0, t0
	jr ra
