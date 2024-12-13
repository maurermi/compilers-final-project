main:
.l0:
	mv t2, t0
.l1:
	li t0, 0
.l2:
	beq t0, zero, .l3
	j l4
.l3:
	li t1, 1
.l4:
	mv a0, t1
	jr ra
.l5:
	mv t1, t0
.l6:
	mv t2, t0
.l7:
	li t0, 1
.l8:
	sub t0, t2, t0
.l9:
	call t0, t0
.l10:
	mul t0, t1, t0
.l11:
	mv a0, t0
	jr ra
