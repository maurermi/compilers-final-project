main:
.l0:
	mv t2, t1
.l1:
	li s1, 1
.l2:
	beq t2, zero, .l3
	j l4
.l3:
	mv t0, t1
.l4:
	mv a0, t0
	jr ra
.l5:
	mv s2, t1
.l6:
	mv t0, t1
.l7:
	li s1, 2
.l8:
	div t0, t0, s1
.l9:
	call s1, s2, t0
.l10:
	mv s1, s1
.l11:
	mv t0, s1
.l12:
	mv s1, s1
.l13:
	mul t0, t0, s1
.l14:
	mv t0, t0
.l15:
	mv t0, t1
.l16:
	li s1, 2
.l17:
	call s1, t0, s1
.l18:
	li t0, 1
.l19:
	beq t0, zero, .l19
	j l23
.l23:
	j .l25
.l20:
	mv t0, t0
.l21:
	mv t2, t1
.l22:
	mul t2, t0, t2
.l25:
	mv t0, t1
.l24:
	mv t1, t0
.l26:
	mv t0, t0
.l27:
	mv a0, t0
	jr ra
