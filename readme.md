# Bitcoin Wallet Prototype in JavaScript

This piece of code takes an mnemonic seed as input (or you can run with the default one) and runs in an infinite loop. At every iteration it calculates the key pair from the seed, then creates and signs a transaction of 1 satoshi. In normal mode the output of the code is a single dot after every iteration. In case the current and the previous transaction doesn't match (potentially bitflip), the process prints a notification and the not matching transactions in hex format.

## Requirements

To run the project you should have node.js installed on your computer.

## How to Use

To run the code just type `node wallet.js` in your terminal.

## Options

### Debug mode

In normal mode the code is only printing a dot after every loop iteration. To get more information use the `--debug` flag. For example, `node wallet.js --debug`. In debug mode, the xpriv, xpub and address is printed in every loop iteration.

__NOTE__: even if you are not in debug mode, the key pair and the address is still recalculated at every iteration, so a successful bitflip is likely to alter these calculations.

__TIP__: You might want to redirect the output of the code to a file in debug mode. This way you will have the whole output in a file that you can search, which is usually more comfortable than working with it in terminal. To redirect the output, use the right arrow. For example, `node wallet.js --debug > log.txt`.

### Specify mnemonic seed

The default mnemonic seed is `tennis strong genre chief viable can parade gift hospital breeze cry relief`. You can change this with the -m flag. For example: `node wallet.js -m "your seed"` (__NOTE__: don't forget the quote).

Of course you can combine the 2 flags.

## Useful tools, links

My code is built on the following library: https://github.com/bitcoinjs/bitcoinjs-lib

I used this website to verify the generated transactions. https://coinb.in/#verify

I tested my code against the test vectors found at the bottom of this page. https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki

Other test vectors I found (I didn't use these): https://github.com/trezor/python-mnemonic/blob/master/vectors.json
