main:
.l0:
	li t1, 2
.l1:
	mv t2, t0
.l2:
	call t1, t1, t2
.l3:
	mv t1, t1
.l4:
	mv t0, t0
.l5:
	mv t1, t1
.l6:
	mul t0, t0, t1
.l7:
	mv a0, t0
	jr ra
