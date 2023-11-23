from django.shortcuts import render, get_object_or_404, redirect
from .models import University, Student
from .forms import UniversityForm, StudentForm


def edit_entity(request, pk, entity_class, form_class, on_success_redirect, template, title):
    entity = None
    if pk is not None:
        entity = get_object_or_404(entity_class, pk=pk)

    if request.method == "POST":
        form = form_class(request.POST, instance=entity) if pk else form_class(request.POST)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.save()
            return redirect(on_success_redirect)
    else:
        form = form_class(instance=entity) if pk else form_class()
    return render(request, template, {'form': form, 'title': title})


def university_list(request):
    universities = University.objects.all()
    return render(request, 'university_list.html', {'universities': universities})


def university_edit(request, pk):
    return edit_entity(request, pk, University, UniversityForm,
                       'university_list', 'edit_entity.html', "Редактировать университет")


def university_new(request):
    return edit_entity(request, None, University, UniversityForm,
                       'university_list', 'edit_entity.html', "Создать университет")


def university_delete(request, pk):
    university = get_object_or_404(University, pk=pk)
    university.delete()
    return redirect('university_list')


def student_edit(request, pk):
    return edit_entity(request, pk, Student, StudentForm, 'university_list',
                       'edit_entity.html', 'Редактировать студента')


def student_new(request):
    return edit_entity(request, None, Student, StudentForm, 'university_list',
                       'edit_entity.html', 'Создать студента')


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('university_list')


def student_list(request):
    students = Student.objects.all()
    return render(request, 'students_list.html', {'students': students})
