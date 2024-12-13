main:
.l0:
	li t2, 0
.l1:
	li t1, 1
.l2:
	beq t2, zero, .l3
	j l4
.l3:
	add t0, t0, t1
.l4:
	mv a0, t0
	jr ra
.l5:
	beq t0, zero, .l5
	j l7
.l7:
	call t0, t2, t1
.l6:
	sub t2, t0, t1
.l8:
	mv a0, t0
	jr ra
.l9:
	sub t2, t0, t1
.l10:
	sub t1, t0, t1
.l11:
	call t0, t0, t1
.l12:
	call t0, t2, t0
.l13:
	mv a0, t0
	jr ra
