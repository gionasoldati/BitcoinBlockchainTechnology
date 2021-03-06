#!/usr/bin/env python3

# Copyright (C) 2017-2019 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

import unittest
import os
import json

from btclib.electrum import PRIVATE, bip32_xpub_from_xprv, \
    electrum_entropy_from_mnemonic, electrum_mnemonic_from_raw_entropy, \
    electrum_master_prvkey_from_mnemonic, \
    electrum_master_prvkey_from_raw_entropy


class TestMnemonicDictionaries(unittest.TestCase):
    def test_electrum_wallet(self):
        lang = "en"

        raw_entropy = 0x110aaaa03974d093eda670121023cd0772
        eversion = 'standard'
        mnemonic = electrum_mnemonic_from_raw_entropy(
            raw_entropy, lang, eversion)
        entropy = int(electrum_entropy_from_mnemonic(mnemonic, lang), 2)
        self.assertLess(entropy-raw_entropy, 0xfff)

        passphrase = ''

        xversion = b'\x04\x88\xAD\xE4'
        mprv = electrum_master_prvkey_from_mnemonic(
            mnemonic, passphrase, xversion)
        # TODO: compare with the mprv generated by electrum
        mprv2 = electrum_master_prvkey_from_raw_entropy(
            raw_entropy, passphrase, lang, xversion)
        self.assertEqual(mprv2, mprv)

        # invalid mnemonic version '00'
        mnemonic = "ability awful fetch liberty company spatial panda hat then canal ball cross video"
        self.assertRaises(ValueError, electrum_master_prvkey_from_mnemonic,
                          mnemonic, passphrase, xversion)

    def test_electrum_vectors(self):
        filename = "test_electrum_vectors.json"
        path_to_filename = os.path.join(os.path.dirname(__file__),
                                        "./data/",
                                        filename)
        with open(path_to_filename, 'r') as f:
            test_vectors = json.load(f)
        f.closed

        for test_vector in test_vectors:
            test_mnemonic = test_vector[1]
            passphrase = test_vector[2]
            test_mpub = test_vector[3]
            xversion = PRIVATE[0]
            mprv = electrum_master_prvkey_from_mnemonic(
                test_mnemonic, passphrase, xversion)
            mpub = bip32_xpub_from_xprv(mprv).decode()
            self.assertEqual(mpub, test_mpub)

            lang = "en"
            entropy = int(electrum_entropy_from_mnemonic(
                test_mnemonic, lang), 2)
            version = test_vector[0]
            mnemonic = electrum_mnemonic_from_raw_entropy(
                entropy, lang, version)
            self.assertEqual(mnemonic, test_mnemonic)


if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()
