main:
.l0:
	li t0, 1
.l1:
	mv t0, t0
.l2:
	mv s1, t0
.l3:
	mv t1, t1
.l4:
	li t0, 1
.l5:
	sub t0, t1, t0
.l6:
	beq t0, zero, .l7
	j l17
.l7:
	mv s1, t0
.l17:
	j .l2
.l8:
	mv t0, t0
.l9:
	mul t0, s1, t0
.l10:
	mv t1, t1
.l11:
	beq t0, zero, .l12
	j l13
.l12:
	mv t2, t0
.l13:
	mv a0, t2
	jr ra
.l14:
	mv t1, t0
.l15:
	li t0, 1
.l16:
	add t2, t1, t0
.l18:
	li t0, 0
.l19:
	mv a0, t0
	jr ra
