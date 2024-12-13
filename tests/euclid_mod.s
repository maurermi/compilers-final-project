main:
.l0:
	mv t2, t0
.l1:
	mv t0, t0
.l2:
	mv s1, t1
.l3:
	div s1, t0, s1
.l4:
	mv t0, t1
.l5:
	mul t0, s1, t0
.l6:
	sub t0, t2, t0
.l7:
	mv t0, t0
.l8:
	mv t0, t0
.l9:
	mv a0, t0
	jr ra
