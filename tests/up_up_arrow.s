main:
.l0:
	li t1, 1
.l1:
	mv s1, t2
.l2:
	li t1, 1
.l3:
	beq t0, zero, .l4
	j l9
.l4:
	beq t0, zero, .l5
	j l6
.l9:
	mv a0, s1
	jr ra
.l5:
	j .l8
.l6:
	sub t0, t0, t1
.l8:
	j .l3
.l7:
	call s1, t2, t0, s1
