main:
.l0:
	mv t2, t0
.l1:
	li t0, 1
.l2:
	mv t1, t0
.l3:
	mv t0, t2
.l4:
	mv t0, t0
.l5:
	mv t2, t0
.l6:
	li t0, 0
.l7:
	beq t0, zero, .l8
	j l16
.l8:
	mv t1, t1
.l16:
	mv t0, t1
.l9:
	mv t2, t0
.l10:
	mul t1, t1, t2
.l11:
	mv t1, t1
.l12:
	mv t0, t0
.l13:
	li t2, 1
.l14:
	sub t0, t0, t2
.l15:
	j .l5
.l17:
	print t0
.l18:
	li t0, 0
