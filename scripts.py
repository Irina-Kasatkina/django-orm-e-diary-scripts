import random

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Lesson
from datacenter.models import Mark
from datacenter.models import Schoolkid
from datacenter.models import Subject


def create_commendation(schoolkid_name: str, subject_title: str):
    """
    Create a new commendation for the schoolkid
    with the given schoolkid name and subject title.

    Example:
        create_commendation('Васильева Алла', 'Чистописание')
    """

    schoolkid = get_schoolkid(schoolkid_name)
    if not schoolkid:
        return

    lesson = get_last_lesson(schoolkid, subject_title)
    if not lesson:
        return

    texts = [
            'Молодец!', 'Отлично!', 'Хорошо!',
            'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
            'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!',
            'Именно этого я давно ждал от тебя!',
            'Сказано здорово – просто и ясно!',
            'Ты, как всегда, точен!', 'Очень хороший ответ!',
            'Талантливо!', 'Ты сегодня прыгнул выше головы!',
            'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!',
            'Замечательно!', 'Прекрасное начало!', 'Так держать!',
            'Ты на верном пути!', 'Здорово!',
            'Это как раз то, что нужно!', 'Я тобой горжусь!',
            'С каждым разом у тебя получается всё лучше!',
            'Мы с тобой не зря поработали!',
            'Я вижу, как ты стараешься!', 'Ты растешь над собой!',
            'Ты многое сделал, я это вижу!',
            'Теперь у тебя точно все получится!',
    ]
    text = random.choice(texts)
    Commendation.objects.create(
            text=text,
            created=lesson.date,
            schoolkid=schoolkid,
            subject=lesson.subject,
            teacher=lesson.teacher
    )


def fix_marks(schoolkid_name: str):
    """
    Fix all bad marks (< 4) schoolkid to mark 5
    for the schoolkid with the given schoolkid name.

    Example:
        fix_marks('Фролов Иван')
    """

    schoolkid = get_schoolkid(schoolkid_name)
    if not schoolkid:
        return

    good_point, great_point = 4, 5
    Mark.objects.filter(
            schoolkid=schoolkid,
            points__lt=good_point
    ).update(points=great_point)


def get_last_lesson(schoolkid: Schoolkid, subject_title: str) -> Lesson:
    """
    Get from database and return the Subject model object with the latter date
    by the given Schoolkid model object and subject title.
    """

    subject = get_subject(schoolkid, subject_title)
    if not subject:
        return None

    lessons = Lesson.objects.filter(
            subject__title=subject.title,
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter
    ).order_by('-date')
    if not lessons:
        print(f'Уроков по предмету "{subject_title}" пока не было.')
        return None

    return lessons.first()


def get_schoolkid(schoolkid_name: str) -> Schoolkid:
    """
    Get from database and return the Schoolkid model object
    by the given schoolkid name.
    """

    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        return schoolkid
    except ObjectDoesNotExist:
        print(f'Нет школьников, ФИО которых содержит "{schoolkid_name}".')
        print('Проверьте имя на опечатки и запустите снова.')
        return None
    except MultipleObjectsReturned:
        print('Найдено больше одного школьника,',
              f'ФИО которых содержит "{schoolkid_name}".')
        print('Введите фамилию, имя и отчество.')
        return None


def get_subject(schoolkid: Schoolkid, subject_title: str) -> Subject:
    """
    Get from database and return the Subject model object
    by the given Schoolkid model object and subject title.
    """

    try:
        subject = Subject.objects.get(
                title__contains=subject_title,
                year_of_study=schoolkid.year_of_study
        )
        return subject
    except ObjectDoesNotExist:
        print(f'Нет предметов для {schoolkid.year_of_study}-го класса,',
              f'название которых содержит "{subject_title}"')
        print('Проверьте название предмета на опечатки и запустите снова.')
        return None
    except MultipleObjectsReturned:
        print('Найдено больше одного предмета,',
              f'название которых содержит "{subject_title}".\n',
              'Введите более полное название предмета.')
        return None


def remove_chastisements(schoolkid_name):
    """
    Remove all teacher chastisements
    for the schoolkid with the given schoolkid name.

    Example:
        remove_chastisements('Голубев Феофан')
    """

    schoolkid = get_schoolkid(schoolkid_name)
    if schoolkid:
        Chastisement.objects.filter(schoolkid=schoolkid).delete()
