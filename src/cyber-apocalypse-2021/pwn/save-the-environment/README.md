# Pwn - Save the environment

This challenge is similar to [minefield](../minefield) as we have a write what
where condition and a win function.

Unfortunately we can't just do the same exploit again.

In this challenge you can recycle things in exchange of recycling point, with
at least 10 recycling point we can ask to leak an arbitrary address.

So first thing we need to do is to farm these recycling points.

```python
{{#include attack.py:farm_recycling_fn}}
```

Then we'll leak the libc base address by leaking the content of the got table.

```python
{{#include attack.py:leak_libc_base_fn}}
```

The objective will be to overwrite the stack to return to the win function, the
only problem is we don't know where the stack is. For this we can use the
`environ` inside the libc because by default it points to our stack.

```python
{{#include attack.py:leak_environ_fn}}
```

Now we need to find the offset from `environ` to one of the return address. If
we find it, we can overwrite it to return to anywhere.

Because the environ is at the top of the stack, we need to search to the bottom
(from infinity to zero). And here it is, 36 qword away from environ the return
address of one function.

All we need now is to overwrite this address with the win function.

```python
{{#include attack.py:write_what_where_fn}}

{{#include attack.py:www}}
```

And here's the flag!
