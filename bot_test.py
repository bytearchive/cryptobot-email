#!/usr/bin/env python

import unittest
import bot
import email
import gnupg

class BotTest(unittest.TestCase):

    def setUp(self):
        # test keys
        self.public_key = open('test_key/public.key').read()
        self.private_key = open('test_key/private.key').read()
        # set up test keyring
        self.gpg = gnupg.GPG(homedir="test_bot_keyring")
        self.gpg.import_keys(self.public_key)
        self.gpg.import_keys(self.private_key)
        
        # set up tester
        self.emails = {}
        for filename in ['encrypted_to_wrong_key', 'signed', 'unencrypted_thunderbird', 'encrypted_correctly']: 
            self.emails[filename] = email.message_from_string(open('test_emails/'+filename).read())

    def tearDown(self):
        pass

    def test_encrypted(self):
        msg = bot.OpenPGPMessage(self.emails['encrypted_to_wrong_key'],
                                 gpg=self.gpg)
        self.assertTrue(msg.encrypted)

    def test_unencrypted(self):
        msg = bot.OpenPGPMessage(self.emails['unencrypted_thunderbird'],
                                 gpg=self.gpg)
        self.assertFalse(msg.encrypted)

    def test_signed(self):
        msg = bot.OpenPGPMessage(self.emails['signed'],
                                 gpg=self.gpg)
        self.assertTrue(msg.signed)
        
    def test_unsigned(self):
        # todo finish
        pass

    def test_encrypted_wrong_key(self):
        # tododta fill this out
        pass

    def test_encrypted_correct_key(self):
        result_text = "encrypted text"
        msg = bot.OpenPGPMessage(self.emails['encrypted_correctly'],
                                 gpg=self.gpg)
        self.assertEquals(result_text, msg.decrypted_text.split("quoted-printable")[1].strip())


if __name__ == '__main__':
    unittest.main()
