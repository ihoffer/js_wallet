'use strict';
var bitcoin = require('bitcoinjs-lib');
var bip39 = require('bip39');

const DEV = process.argv.indexOf("--debug") !== -1;

// Seed
var mnemonic;
if (process.argv.indexOf("-m") !== -1) {
    const i = process.argv.indexOf("-m") + 1;
    mnemonic = process.argv[i];
} else {
    mnemonic = "tennis strong genre chief viable can parade gift hospital breeze cry relief";
}
console.log("mnemonic: " + mnemonic);
const seed = bip39.mnemonicToSeed(mnemonic);

// Previous hash
const prevHash = "3140eb24b43386f35ba69e3875eb6c93130ac66201d01c58f598defc949a5c2a";

// Amount to transfer
const v = 1;

var oldTx = null;
while(true) {
    var node = bitcoin.HDNode.fromSeedBuffer(seed);

    //Derive m/1 keypair
    var path = "m/1";
    var child = node.derivePath(path);

    const xpub = child.neutered().toBase58();
    const priv = child.toBase58();

    DEV && console.log('xpub: ' + xpub); //ff0488b21e00000000000000000086eaf9dac92bff5a1391bcf396e109dc2499bfc08a550c8d17468a5f8372bceb033e53e808cb2f8c5e9c878fff3582d8257ea4ba6c4ec46cacc4793ea4ed57f06b00000100
    DEV && console.log('priv: ' + priv);

    const addr = child.getAddress();

    DEV && console.log("address: " + addr); //1DsoBCjhgfMrovbKCHtbMTGVi4CFPLbvGh

    var txb = new bitcoin.TransactionBuilder();
    txb.addInput(prevHash, 0);
    txb.addOutput(addr, v);

    txb.sign(0, child);

    const tx = txb.build().toHex();

    DEV && console.log(tx);

    if (oldTx != null && tx !== oldTx) {
        console.log("Something happened");
        console.log("Old tx: " + oldTx);
        console.log("Recent tx: " + tx);
    } else {
        console.log(".");
    }
    oldTx = tx;
}
