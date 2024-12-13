main:
.l0:
	li t2, 1
.l1:
	li t1, 2
.l2:
	add t2, t2, t0
.l3:
	mul t0, t2, t0
.l4:
	div t0, t0, t1
.l5:
	mv a0, t0
	jr ra
