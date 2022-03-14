from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bitcoinaddress import Wallet
from bitcoinaddress.key.key import Key
from bitcoinaddress import Address, Seed

from .serializers import BTCWalletSerializer


class CustomKey(Key):

    @staticmethod
    def of(obj):
        key = CustomKey()
        if isinstance(obj, Seed):
            key._from_seed(obj)
        else:
            try:
                if len(obj) == 64:
                    key._from_hex(obj)
                    return key
                if len(obj) == 51:
                    key._from_wif(obj)
                    return key
                if len(obj) == 52:
                    pass  # TODO
            except:
                raise Exception("Unsupported format.")
        return key

    def get_params(self, testnet=False):
        if testnet:
            params = (self.hex,
                      self.testnet.wif,
                      self.testnet.wifc)
        else:
            params = (self.hex,
                      self.mainnet.wif,
                      self.mainnet.wifc)
        keys = {'Private Key HEX': params[0], 'Private Key WIF': params[1], 'Private Key WIF compressed': params[2]}
        return keys


class CustomAddress(Address):

    @staticmethod
    def of(key: CustomKey):
        address = CustomAddress(key)
        address.generate()
        return address

    def hi(self):
        pass

    def get_params(self, testnet=False):
        if testnet:
            params = (self.pubkey,
                      self.pubkeyc,
                      self.testnet.pubaddr1,
                      self.testnet.pubaddr1c,
                      self.testnet.pubaddr3,
                      self.testnet.pubaddrtb1_P2WPKH,
                      self.testnet.pubaddrtb1_P2WSH)
        else:
            params = (self.pubkey,
                      self.pubkeyc,
                      self.mainnet.pubaddr1,
                      self.mainnet.pubaddr1c,
                      self.mainnet.pubaddr3,
                      self.mainnet.pubaddrbc1_P2WPKH,
                      self.mainnet.pubaddrbc1_P2WSH)

        address = {
            'Public Key':params[0],
            'Public Key compressed':params[1],
            'Public Address 1':params[2],
            'Public Address 1 compressed':params[3],
            'Public Address 3':params[4],
            'Public Address bc1 P2WPKH':params[5],
            'Public Address bc1 P2WSH':params[6]
            }
        return address


class CustomWallet(Wallet):

    def __init__(self, hash_or_seed=None, testnet=False):
        if hash_or_seed is None: hash_or_seed = Seed()
        self.key = CustomKey.of(hash_or_seed)
        self.final_key = self.key.get_params()
        self.address = CustomAddress.of(self.key)
        self.final_address = self.address.get_params()
        self.testnet = testnet


class BTCWalletAPI(APIView):

    def get(self, request):
        wallet = CustomWallet()
        key = wallet.final_key
        address = wallet.final_address
        data = {'key': key, 'address': address}
        serializer = BTCWalletSerializer(data)
        return Response(serializer.data)
