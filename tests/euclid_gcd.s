main:
.l0:
	li t0, 0
.l1:
	mv t2, t0
.l2:
	mv t0, s1
.l3:
	mv t2, t2
.l4:
	sub t0, t0, t2
.l5:
	mv t0, t0
.l6:
	not t0, t0
.l7:
	mv t0, t0
.l8:
	beq t0, zero, .l9
	j l23
.l9:
	mv t0, s1
.l23:
	mv t0, t1
.l10:
	mv t0, t0
.l11:
	mv t1, t1
.l12:
	mv s1, s1
.l13:
	call t1, t1, s1
.l14:
	mv s1, t1
.l15:
	mv t0, t0
.l16:
	mv t1, t0
.l17:
	mv s1, s1
.l18:
	mv t0, t2
.l19:
	sub t0, s1, t0
.l20:
	mv t0, t0
.l21:
	not t0, t0
.l22:
	j .l8
.l24:
	mv a0, t0
	jr ra
