main:
.l0:
	mv t2, t2
.l1:
	li t0, 10
.l2:
	li s1, 0
.l3:
	li t1, 1
.l4:
	li t0, 2
.l5:
	li s2, 1
.l6:
	beq t0, zero, .l7
	j l11
.l7:
	mul t0, s1, t0
.l11:
	mv a0, t1
	jr ra
.l8:
	add t0, t0, t1
.l9:
	add s1, s1, s2
.l10:
	j .l6
