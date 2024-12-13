main:
.l0:
	mv t0, t0
.l1:
	li t1, 0
.l2:
	li t1, 1
.l3:
	li t2, 2
.l4:
	mv s2, t1
.l5:
	mv mr, t2
.l6:
	mv t1, t1
.l7:
	mul t2, mr, mr
.l8:
	beq t2, zero, .l16
	j l9
.l16:
	beq t0, zero, .l17
	j l18
.l9:
	div t2, t0, mr
.l10:
	mul mr, t2, mr
.l11:
	sub mr, t0, mr
.l12:
	beq s1, zero, .l13
	j l15
.l13:
	add s2, s2, mr
.l15:
	j .l7
.l14:
	add s2, s2, t2
.l17:
	mv t1, t1
.l18:
	print t1
