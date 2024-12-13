main:
.l0:
	mv t0, t1
.l1:
	mv t1, t1
.l2:
	mv s1, t2
.l3:
	div s1, t1, s1
.l4:
	mv t1, t2
.l5:
	mul t1, s1, t1
.l6:
	sub t0, t0, t1
.l7:
	mv a0, t0
	jr ra
