main:
.l0:
	li t0, 1
.l1:
	li t2, 1
.l2:
	li s1, 10
.l3:
	li t1, 0
.l4:
	li t2, 1
.l5:
	beq t0, zero, .l6
	j l8
.l6:
	add t1, t1, t2
.l8:
	print t1
.l7:
	j .l5
.l9:
	mv a0, t1
	jr ra
