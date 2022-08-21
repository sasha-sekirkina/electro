from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(
        label="Тема",
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    email = forms.EmailField(
        label="Адрес электронной почты, на который хотели бы получить ответ",
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'rows': 6}
        )
    )
    content = forms.CharField(
        label="Ваш вопрос/предложение",
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
        )
    )