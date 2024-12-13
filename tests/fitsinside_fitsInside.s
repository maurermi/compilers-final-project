main:
.l0:
	le s1, t0, t2
.l1:
	le t1, t2, t0
.l2:
	and t1, s1, t1
.l3:
	le t0, t0, t0
.l4:
	le t2, t2, t2
.l5:
	and t0, t0, t2
.l6:
	or t0, t1, t0
.l7:
	mv a0, t0
	jr ra
