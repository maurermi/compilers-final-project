main:
.l0:
	li t0, 1
.l1:
	li t0, 2
.l2:
	j .l10
.l10:
	j .l3
.l11:
	j .l3.l3
.l4:
	div t1, t2, t0
.l3:
	beq t0, zero, .l11
	j l4
.l5:
	mul t1, t1, t0
.l6:
	beq t1, zero, .l7
	j l8
.l7:
	j .l10
.l8:
	mul t2, t2, t0
.l9:
	add t2, t2, t0
