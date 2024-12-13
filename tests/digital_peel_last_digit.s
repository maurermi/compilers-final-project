main:
.l0:
	li t2, 10
.l1:
	div t0, t1, t2
.l2:
	mul t0, t0, t2
.l3:
	sub t0, t1, t0
.l4:
	mv a0, t0
	jr ra
