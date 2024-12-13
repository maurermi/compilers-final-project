main:
.l0:
	li t1, 1
.l1:
	li t0, 0
.l2:
	li t0, 1
.l3:
	beq t0, zero, .l4
	j l8
.l4:
	beq t0, zero, .l5
	j l6
.l8:
	mv a0, t1
	jr ra
.l5:
	j .l4
.l6:
	mul t1, t1, t0
.l7:
	j .l4
