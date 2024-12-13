main:
.l0:
	li t0, 0
.l1:
	beq t0, zero, .l7
	j l2
.l7:
	beq t0, zero, .l7t0, zero, .l7, t0
.l2:
	li t0, 2
.l3:
	call t2, t1, t0
.l4:
	div t0, t1, t0
.l5:
	call t0
.l6:
	print t2
