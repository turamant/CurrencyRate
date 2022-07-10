from django import forms


class CoinForm(forms.Form):
    bitcoin = forms.BooleanField(required=False) #1
    ripple = forms.BooleanField(required=False)  #2
    cardano = forms.BooleanField(required=False) #3
    ethereum = forms.BooleanField(required=False) #4
    litecoin = forms.BooleanField(required=False) #5
    monero = forms.BooleanField(required=False) #6
    dogecoin = forms.BooleanField(required=False) #7
    tether = forms.BooleanField(required=False) #8
    solana = forms.BooleanField(required=False) #9
    polkadot = forms.BooleanField(required=False) #10


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

