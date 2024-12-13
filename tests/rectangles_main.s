main:
.l0:
	call t2, t0, t0
.l1:
	call t0, t0, t0
.l2:
	sub t1, t2, t0
.l3:
	beq t0, zero, .l6
	j l4
.l6:
	print t1
.l4:
	li t0, -1
.l5:
	mul t1, t1, t0
