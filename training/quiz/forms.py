from django import forms
from django.contrib.auth.models import User
from .models import Question
from django.core.exceptions import ValidationError

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        answers = self.instance.answer_set.get.all()
        if answers.count() > 4:
            raise ValidationError
        return cleaned_data
