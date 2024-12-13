main:
.l0:
	li t0, 1
.l1:
	mul mr, t2, t2
.l2:
	mv mr, t0
.l3:
	mv s2, t0
.l4:
	mul t1, mr, mr
.l5:
	mul s1, s2, s2
.l6:
	add t1, t1, s1
.l7:
	beq t1, zero, .l8
	j l9
.l8:
	print s2, mr
.l9:
	add s2, s2, t0
.l10:
	beq t1, zero, .l11
	j l4
.l11:
	add mr, mr, t0
.l12:
	beq t1, zero, .l13
	j l3
