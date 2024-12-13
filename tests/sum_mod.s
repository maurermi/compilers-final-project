main:
.l0:
	div t1, t0, t0
.l1:
	mul t1, t0, t1
.l2:
	sub t0, t0, t1
.l3:
	mv a0, t0
	jr ra
