#!/usr/bin/env python3
# encoding: utf-8

"""This file provides the necessary abstract interface and implementation of a Wallet"""

import logging
from abc import ABC, abstractmethod
from io import BytesIO
from typing import Optional
from uuid import uuid1

import qrcode
from bitcoinlib.wallets import Wallet, WalletKey
from mnemonic import Mnemonic

logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s',
                    level=logging.DEBUG)


class WalletInterface(ABC):
    """Abstract interface provided by a wallet."""

    @abstractmethod
    def get_xpub(self, image: bool = False) -> bytes:
        """
        Get the extended public key.
        If image is true, get the QR code image as a jpg format
        """
        raise NotImplementedError

    @abstractmethod
    def get_address(self, image: bool = False) -> bytes:
        """Get a P2WPKH address to receive payment."""
        raise NotImplementedError

    @abstractmethod
    def balance(self) -> int:
        """Balance Satoshis from UTXO"""
        raise NotImplementedError


class CustomWallet(WalletInterface):
    """Customised implementation of the wallet based on the Blue Wallet Standard."""

    def __init__(self, seed: Optional[str] = None):
        """Implement the wallet using the seed phrase."""
        mnemo: Mnemonic = Mnemonic()
        if seed is None:
            seed = mnemo.generate()  # Generate random seed if not supplied as part of recovery
            logging.debug(msg=f'Note down the random seed initialised as \n {seed}.')
        self.wallet: Wallet = Wallet.create(name=uuid1().hex, keys=seed)
        self.res: WalletKey = self.wallet.public_master()
        logging.info(msg=f'Wallet {self.wallet.name} created.')

    @staticmethod
    def _convert_string_to_qr_(raw_str: str) -> bytes:
        """Convert a string to jpeg QR image byte array."""
        qr: qrcode.main.QRCode = qrcode.main.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                                                    box_size=10, border=4)
        qr.add_data(data=raw_str)
        qr.make(fit=True)
        # noinspection PyUnresolvedReferences
        img: qrcode.image.pil.PilImage = qr.make_image(fill_color="black", back_color="white")
        with BytesIO() as img_byte_arr:
            # noinspection PyArgumentList
            img.save(stream=img_byte_arr, format='JPEG')
            return img_byte_arr.getvalue()

    def get_xpub(self, image: bool = False) -> bytes:
        """
        Get the extended public key.
        If image is true, get the QR code image as a jpg format
        """
        xpub: str = self.res.wif
        return self._convert_string_to_qr_(raw_str=xpub) if image else xpub.encode()

    def get_address(self, image: bool = False) -> bytes:
        """Get a P2WPKH address to receive payment."""
        address: str = self.res.address
        return self._convert_string_to_qr_(raw_str=address) if image else address.encode()

    def balance(self) -> int:
        """Balance Satoshis from UTXO"""
        return self.res.balance(as_string=False)
