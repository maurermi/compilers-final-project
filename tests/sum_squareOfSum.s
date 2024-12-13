main:
.l0:
	li t1, 0
.l1:
	mv t1, t1
.l2:
	li t1, 1
.l3:
	mv t2, t1
.l4:
	mv t2, t2
.l5:
	mv t1, t0
.l6:
	beq t1, zero, .l7
	j l19
.l7:
	mv t1, t1
.l19:
	mv t0, t0
.l8:
	mv s1, t2
.l9:
	add t1, t1, s1
.l10:
	mv t1, t1
.l11:
	mv t1, t2
.l12:
	li t2, 1
.l13:
	add t1, t1, t2
.l14:
	j .l4
.l15:
	mv t0, t1
.l16:
	mv t1, t1
.l17:
	mul t0, t0, t1
.l18:
	mv t0, t0
.l20:
	mv a0, t0
	jr ra
