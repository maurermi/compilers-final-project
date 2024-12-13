main:
.l0:
	mv t2, t1
.l1:
	mv t0, t1
.l2:
	mul t2, t2, t0
.l3:
	li s1, 4
.l4:
	mv t0, t1
.l5:
	mul s1, s1, t0
.l6:
	mv t0, t1
.l7:
	mul t0, s1, t0
.l8:
	sub t0, t2, t0
.l9:
	mv t0, t0
.l10:
	li s1, 2
.l11:
	mv t2, t1
.l12:
	mul t2, s1, t2
.l13:
	mv t2, t2
.l14:
	li s2, 0
.l15:
	mv s1, t1
.l16:
	sub s1, s2, s1
.l17:
	mv s2, t0
.l18:
	call s2, s2
.l19:
	add s1, s1, s2
.l20:
	mv s1, s1
.l21:
	li s2, 0
.l22:
	mv t1, t1
.l23:
	sub t1, s2, t1
.l24:
	mv t0, t0
.l25:
	call t0, t0
.l26:
	sub t0, t1, t0
.l27:
	mv t1, t0
.l28:
	mv s1, s1
.l29:
	mv t0, t2
.l30:
	div t0, s1, t0
.l31:
	print t0
.l32:
	li t0, 0
.l33:
	mv t1, t1
.l34:
	mv t0, t2
.l35:
	div t0, t1, t0
.l36:
	print t0
.l37:
	li t0, 0
