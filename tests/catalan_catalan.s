main:
.l0:
	li t0, 1
.l1:
	li t2, 0
.l2:
	beq t1, zero, .l3
	j l3
.l3:
	mv a0, t0
	jr ra
.l4:
	mv s2, t2
.l5:
	mv s1, t2
.l6:
	sub t1, t1, t0
.l7:
	beq t1, zero, .l7
	j l13
.l13:
	j .l7
.l8:
	sub t2, t1, s1
.l9:
	call t1, s1
.l10:
	call t2, t2
.l11:
	mul t1, t1, t2
.l12:
	add s2, s2, t1
.l14:
	mv a0, s2
	jr ra
