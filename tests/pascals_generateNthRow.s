main:
.l0:
	li t1, 1
.l1:
	mv s1, t1
.l2:
	mv t1, s1
.l3:
	print t1
.l4:
	li t1, 0
.l5:
	li t1, 0
.l6:
	mv t1, t1
.l7:
	mv t1, t1
.l8:
	mv t0, t0
.l9:
	beq t0, zero, .l10
	j l31
.l10:
	mv t2, t0
.l31:
	mv t2, t0t2, t0, t0
.l11:
	mv t0, t1
.l12:
	sub t0, t2, t0
.l13:
	mv t0, t0
.l14:
	mv t0, t0
.l15:
	li t2, 1
.l16:
	add t0, t0, t2
.l17:
	mv t0, t0
.l18:
	mv t2, s1
.l19:
	mv t0, t0
.l20:
	mul t0, t2, t0
.l21:
	mv t0, t0
.l22:
	mv t2, t0
.l23:
	print t2
.l24:
	li t2, 0
.l25:
	mv t0, t0
.l26:
	mv s1, t0
.l27:
	mv t0, t1
.l28:
	li t1, 1
.l29:
	add t0, t0, t1
.l30:
	j .l7
