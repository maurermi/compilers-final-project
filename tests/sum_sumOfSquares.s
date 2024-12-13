main:
.l0:
	li t0, 0
.l1:
	mv t0, t0
.l2:
	li t0, 1
.l3:
	mv t2, t0
.l4:
	mv t1, t2
.l5:
	mv t0, s1
.l6:
	beq t0, zero, .l7
	j l15
.l7:
	mv t1, t2
.l15:
	mv t0, t2
.l8:
	mv s1, t2
.l9:
	mul t1, t1, s1
.l10:
	mv t1, t1
.l11:
	mv t0, t0
.l12:
	mv t1, t1
.l13:
	add t0, t0, t1
.l14:
	mv t0, t0
.l16:
	li t1, 1
.l17:
	add t0, t0, t1
.l18:
	j .l4
.l19:
	mv t0, t0
.l20:
	mv a0, t0
	jr ra
