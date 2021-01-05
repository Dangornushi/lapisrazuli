
func(int x, int y):
    add a, x, y
    mov eax, a
    ret

main():
    mov x, 10
    mov y, 2
    msg func(int x, int y)
    mov eax, 0
    ret

call main