import asyncio
import sqlite3
from mnemonic import Mnemonic
import bip32utils


mnemon = Mnemonic('english')

async def main():

    conn = sqlite3.connect('wallet.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS wallet
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, words TEXT, xpub TEXT)''')

    i = 1

    while i < 500001:
        words = mnemon.generate(128)
        seed = mnemon.to_seed(words)

        root_key = bip32utils.BIP32Key.fromEntropy(seed)
        path = "m/44'/0'/0'"
        child_key = root_key.ChildKey(44 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN).ChildKey(0 + bip32utils.BIP32_HARDEN)
        xpub = child_key.ExtendedKey(private=False)

        c.execute("INSERT INTO wallet (words, xpub) VALUES (?, ?)", (words, xpub))
        conn.commit()
        i += 1

        print(i)

    conn.close()
    print("Done.......")

if __name__ == '__main__':
    asyncio.run(main())

