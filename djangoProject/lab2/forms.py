from django import forms
from .models import University, Student


class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['full_name', 'short_name', 'creation_date']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'birth_date', 'university', 'enrollment_year']
