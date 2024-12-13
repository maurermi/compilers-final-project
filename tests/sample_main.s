main:
.l0:
	li t1, 10
.l1:
	li t0, 1
.l2:
	li t2, 1
.l3:
	add s1, t1, t0
.l4:
	li t0, 50
.l5:
	beq t0, zero, .l6
	j l7
.l6:
	j .l11
.l7:
	add s1, s1, t2
.l11:
	add s1, t2, s1
.l8:
	beq t0, zero, .l9
	j l10
.l9:
	j .l11
.l10:
	mul s1, s1, t2
.l12:
	add t0, t2, t2
.l13:
	add t0, s1, t0
.l14:
	add t0, t0, t1
.l15:
	mv a0, t0
	jr ra
