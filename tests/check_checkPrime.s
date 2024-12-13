main:
.l0:
	mv t2, t0
.l1:
	li t1, 1
.l2:
	beq t1, zero, .l3
	j l4
.l3:
	li t0, False
.l4:
	mv a0, t0
	jr ra
.l5:
	li t1, 2
.l6:
	mv t1, t1
.l7:
	mv t1, t1
.l8:
	mv t0, t0
.l9:
	beq t0, zero, .l9
	j l25
.l25:
	add t0, s1, t2
.l10:
	mv t2, t0
.l11:
	mv s1, t1
.l12:
	div t2, t2, s1
.l13:
	mv t2, t2
.l14:
	mv t2, t2
.l15:
	mv t1, t1
.l16:
	mul t1, t2, t1
.l17:
	mv t0, t0
.l18:
	sub t0, t1, t0
.l19:
	mv t0, t0
.l20:
	beq t0, zero, .l20
	j l21
.l21:
	li t0, False
.l22:
	mv a0, t0
	jr ra
.l23:
	mv s1, t1
.l24:
	li t2, 1
.l26:
	j .l7
.l27:
	li t0, True
.l28:
	mv a0, t0
	jr ra
