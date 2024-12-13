main:
.l0:
	li t1, 10
.l1:
	li t0, 1
.l2:
	li t2, 1
.l3:
	add t0, t1, t0
.l4:
	li t1, 50
.l5:
	gt t0, t0, t2
.l6:
	beq t0, zero, .l7
	j l8
.l7:
	j .l9
.l8:
	add t0, t0, t2
.l9:
	add t0, t2, t0
.l10:
	add t0, t2, t2
.l11:
	mv a0, t0
	jr ra
