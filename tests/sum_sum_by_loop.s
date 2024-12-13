main:
.l0:
	li t1, 1
.l1:
	li t2, 0
.l2:
	li t1, 1
.l3:
	beq t0, zero, .l4
	j l6
.l4:
	add t2, t2, t1
.l6:
	mv a0, t2
	jr ra
.l5:
	j .l3
