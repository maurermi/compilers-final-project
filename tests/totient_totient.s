main:
.l0:
	mv t0, mr
.l1:
	li t1, 2
.l2:
	li t2, 1
.l3:
	li s1, 0
.l4:
	mul t1, t1, t1
.l5:
	beq t1, zero, .l6
	j l15
.l6:
	call s2, mr, t1
.l15:
	beq t1, zero, .l16
	j l18
.l7:
	beq s1, zero, .l8
	j l14
.l8:
	call s2, mr, t1
.l14:
	j .l4
.l9:
	beq s1, zero, .l10
	j l12
.l10:
	div s2, mr, t1
.l12:
	div s1, t0, t1
.l11:
	j .l8
.l13:
	sub t0, t0, s1
.l16:
	div s1, t0, mr
.l18:
	mv a0, t0
	jr ra
.l17:
	sub t0, t0, s1
