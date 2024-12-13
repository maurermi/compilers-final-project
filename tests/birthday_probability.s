main:
.l0:
	li t0, 1
.l1:
	mv s1, t0
.l2:
	li t0, 1
.l3:
	mv t2, t0
.l4:
	mv t0, t2
.l5:
	mv t1, t1
.l6:
	beq t0, zero, .l7
	j l23
.l7:
	li t0, 365
.l23:
	li t2, 1
.l8:
	mv s2, t2
.l9:
	fsub t0, t0, s2
.l10:
	mv t0, t0
.l11:
	mv s2, t0
.l12:
	li t0, 365
.l13:
	fdiv t0, s2, t0
.l14:
	mv s2, t0
.l15:
	mv t0, s1
.l16:
	mv s1, s2
.l17:
	fmul t0, t0, s1
.l18:
	mv s1, t0
.l19:
	mv t2, t2
.l20:
	li t0, 1
.l21:
	fadd t0, t2, t0
.l22:
	j .l4
.l24:
	mv t0, s1
.l25:
	li t1, 100
.l26:
	fmul t0, t0, t1
.l27:
	li t1, 100
.l28:
	fdiv t0, t0, t1
.l29:
	fsub t0, t2, t0
.l30:
	mv a0, t0
	jr ra
