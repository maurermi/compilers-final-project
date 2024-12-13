main:
.l0:
	li t0, 1
.l1:
	mv t1, t0
.l2:
	mv t0, t1
.l3:
	mv t1, t2
.l4:
	beq t0, zero, .l5
	j l19
.l5:
	mv t0, t1
.l19:
	mv t0, t1t0, t1, t1
.l6:
	call t0, t0
.l7:
	mv t0, t0
.l8:
	beq t0, zero, .l9
	j l12
.l9:
	li t0, 1
.l12:
	li t0, 0
.l10:
	print t0
.l11:
	j .l15
.l15:
	mv t0, t1
.l13:
	print t0
.l14:
	li t0, 0
.l16:
	li t1, 1
.l17:
	add t0, t0, t1
.l18:
	j .l2
