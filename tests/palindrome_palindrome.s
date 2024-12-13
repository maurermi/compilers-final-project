main:
.l0:
	li t1, False
.l1:
	li t1, 0
.l2:
	li t2, 2
.l3:
	li t2, 10
.l4:
	beq t0, zero, .l5
	j l6
.l5:
	j .l19
.l6:
	call t0, t2, t0
.l19:
	mv a0, t1
	jr ra
.l7:
	div t1, t2, t0
.l8:
	div t0, t2, t2
.l9:
	mul t0, t0, t2
.l10:
	sub t0, t2, t0
.l11:
	beq t0, zero, .l12
	j l18
.l12:
	mul t1, t0, t1
.l18:
	j .l19
.l13:
	sub t1, t2, t1
.l14:
	sub t1, t1, t0
.l15:
	div t1, t1, t2
.l16:
	sub t0, t0, t2
.l17:
	j .l19
