main:
.l0:
	li t2, 10
.l1:
	li t0, 0
.l2:
	div t1, t1, t2
.l3:
	mul t1, t1, t2
.l4:
	sub t0, t1, t0
.l5:
	mv a0, t0
	jr ra
