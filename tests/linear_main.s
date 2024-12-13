main:
.l0:
	li t1, 10
.l1:
	li t2, 1
.l2:
	li s1, 1
.l3:
	add t0, t1, t2
.l4:
	li t1, 50
.l5:
	gt t1, t0, s1
.l6:
	mv t0, s1
.l7:
	gt s1, t0, s1
.l8:
	sub t2, t0, s1
.l9:
	mul t1, t0, s1
.l10:
	add s1, s1, t0
.l11:
	add t1, s1, s1
.l12:
	add t0, s1, t0
.l13:
	add t0, t0, t0
.l14:
	mv a0, t0
	jr ra
