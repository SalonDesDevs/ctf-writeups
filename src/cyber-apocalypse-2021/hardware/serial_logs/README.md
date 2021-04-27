# Hw - Serial logs
For this challenge, we have a Saleae Logic project export. Giving the name of the challenge, and the channel 1, we will use the `serial Async` with the default settings:
![dump_img_serial](https://i.imgur.com/olqr2nt.png)

Somes logs appear then in the console:
```
[...more logs...]
[LOG] Connection from 6edec472e9754574d91f460e170b825bacee5f121b73805dffa4f2a5a7d23d7f
[LOG] Connection from 316636cf0500c22f97fa261585b72a48c4625aca7868f0f6ee253937620ac15c
[LOG] Connection from 4b1186d29d6b97f290844407273044e5202ddf8922163077b4a82615fdb22376
[LOG] Connection from 4b1186d29d6b97f290844407273044e5202ddf8922163077b4a82615fdb22376
[LOG] Connection from 4b1186d29d6b97f290844407273044e5202ddf8922163077b4a82615fdb22376
[ERR] Noise detected in channel. Swithcing baud to backup value
```
And after this error, there is garbage on the console output. This last message learn us that the channel baud has been changed from `115200` to some unknown value. After trying some common default values without success, we will try to figure out the baud by analysing the capture.
For this, we first take a charactere than could be found in the damaged communication.
![baud_calculation](https://i.imgur.com/dqrisQa.png)

So the timing for the first bit of communication is `8.48μs`.
We then compute \\(\frac{1}{8.48\times 10^{-6}\\) to find the baud (which is roughly like a frequency)
![baud_deduction](https://i.imgur.com/KuvZhya.png)

We then measure the timing of the next first bits. We found a timing of `13.46μs`. So by trying the same computation that above, we find a baud of `74294`. Trying this setting, the flag appears at the end of the logs. 