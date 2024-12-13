main:
.l0:
	li t2, 10
.l1:
	li t0, 1
.l2:
	li t1, 1
.l3:
	add t0, t2, t0
.l4:
	li s2, 50
.l5:
	beq s1, zero, .l6
	j l8
.l6:
	j .l11
.l8:
	beq s1, zero, .l9
	j l10
.l11:
	add t0, t1, t0
.l7:
	add t0, t0, t1
.l9:
	j .l11
.l10:
	mul t0, t0, t1
.l12:
	add t1, t1, t1
.l13:
	add t0, t0, t1
.l14:
	add t0, t0, t2
.l15:
	mv a0, t0
	jr ra
