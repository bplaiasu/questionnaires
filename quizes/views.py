from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Question, Answer, UserDashboard, UserDashboardDetails
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
import uuid
import random


def index(request):
    return render(request, 'quizes/index.html')


def platform(request):
    context = {
        'fixed_footer': True
    }
    return render(request, 'quizes/platform.html', context)


def start_quiz(request):
    return render(request, 'quizes/start-quiz.html')


def preparation(request):
    categories = Category.objects.filter(is_active=True)
    context = {
        'categories': categories
    }
    return render(request, 'quizes/preparation.html', context)


# @login_required(login_url='/accounts/login')
def simulation_a(request):
    categories = Category.objects.filter(is_active=True, simulation_exam_a=True)

    if categories.count() > 0:
        # get all categories questions
        first_categ = categories.first()
        second_categ = categories[1]
        third_categ = categories[2]
        last_categ = categories.last()
        first_categ_questions_ids, second_categ_questions_ids, third_categ_questions_ids, last_categ_questions_ids = [], [], [], []

        # get all categories questions and randomize questions
        first_categ_questions = list(Question.objects.filter(category=first_categ.id))
        first_categ_questions = random.sample(first_categ_questions, len(first_categ_questions))[:first_categ.sim_ex_a_questions]
        second_categ_questions = list(Question.objects.filter(category=second_categ.id))
        second_categ_questions = random.sample(second_categ_questions, len(second_categ_questions))[:second_categ.sim_ex_a_questions]
        third_categ_questions = list(Question.objects.filter(category=third_categ.id))
        third_categ_questions = random.sample(third_categ_questions, len(third_categ_questions))[:third_categ.sim_ex_a_questions]
        last_categ_questions = list(Question.objects.filter(category=last_categ.id))
        last_categ_questions = random.sample(last_categ_questions, len(last_categ_questions))[:last_categ.sim_ex_a_questions]
        
        # save the selected questions into list for each category
        for i in first_categ_questions:
            first_categ_questions_ids.append(i.id)
        for i in second_categ_questions:
            second_categ_questions_ids.append(i.id)
        for i in third_categ_questions:
            third_categ_questions_ids.append(i.id)
        for i in last_categ_questions:
            last_categ_questions_ids.append(i.id)

        # delete the session key already saved
        if 'first_categ_questions_ids' in request.session:
            del request.session['first_categ']
            del request.session['first_categ_questions_ids']
        if 'second_categ_questions_ids' in request.session:
            del request.session['second_categ']
            del request.session['second_categ_questions_ids']
        if 'third_categ_questions_ids' in request.session:
            del request.session['third_categ']
            del request.session['third_categ_questions_ids']
        if 'last_categ_questions_ids' in request.session:
            del request.session['last_categ']
            del request.session['last_categ_questions_ids']
        
        # set session
        request.session['first_categ'] = first_categ.id
        request.session['second_categ'] = second_categ.id
        request.session['third_categ'] = third_categ.id
        request.session['last_categ'] = last_categ.id

        request.session['first_categ_questions_ids'] = first_categ_questions_ids
        request.session['second_categ_questions_ids'] = second_categ_questions_ids
        request.session['third_categ_questions_ids'] = third_categ_questions_ids
        request.session['last_categ_questions_ids'] = last_categ_questions_ids
    
        context = {
            'categories': categories
        }
        return render(request, 'quizes/sim_a.html', context)
    else:
        return render(request, 'quizes/test.html')


@login_required(login_url='/accounts/login')
def sima_start_test(request, category_id=None, question_id=None):
    categories = Category.objects.filter(is_active=True, simulation_exam_a=True).order_by('id')
    
    # get session variables for first category
    first_categ = request.session['first_categ']
    second_categ = request.session['second_categ']
    third_categ = request.session['third_categ']
    last_categ = request.session['last_categ']
    if 'first_categ_questions_ids' in request.session:
        first_categ_questions_ids = request.session['first_categ_questions_ids']
    if 'second_categ_questions_ids' in request.session:
        second_categ_questions_ids = request.session['second_categ_questions_ids']
    if 'third_categ_questions_ids' in request.session:
        third_categ_questions_ids = request.session['third_categ_questions_ids']
    if 'last_categ_questions_ids' in request.session:
        last_categ_questions_ids = request.session['last_categ_questions_ids']
    
    # get only the questions which were selected randomly for each category
    # 1st category
    pk_list = first_categ_questions_ids
    clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(pk_list)])
    ordering = 'CASE %s END' % clauses
    first_categ_questions = Question.objects.filter(pk__in=pk_list).extra(select={'ordering': ordering}, order_by=('ordering',))
    # 2nd category
    pk_list = second_categ_questions_ids
    clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(pk_list)])
    ordering = 'CASE %s END' % clauses
    second_categ_questions = Question.objects.filter(pk__in=pk_list).extra(select={'ordering': ordering}, order_by=('ordering',))
    # 3rd category
    pk_list = third_categ_questions_ids
    clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(pk_list)])
    ordering = 'CASE %s END' % clauses
    third_categ_questions = Question.objects.filter(pk__in=pk_list).extra(select={'ordering': ordering}, order_by=('ordering',))
    # last category
    pk_list = last_categ_questions_ids
    clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(pk_list)])
    ordering = 'CASE %s END' % clauses
    last_categ_questions = Question.objects.filter(pk__in=pk_list).extra(select={'ordering': ordering}, order_by=('ordering',))
    
    # random_selected_questions = first_categ_questions|second_categ_questions
    random_selected_questions = first_categ_questions \
                                    .union(second_categ_questions) \
                                    .union(third_categ_questions) \
                                    .union(last_categ_questions) \
                                    .order_by('category')

    random_selected_questions_ids = []
    for i in random_selected_questions:
        random_selected_questions_ids.append(i.id)
    

    # show 1 question per page.
    paginator = Paginator(random_selected_questions, 1)
    page = request.GET.get('page') if request.GET.get('page') else 1
    questions_per_category_per_page = paginator.get_page(page)

    # get all answers of a question
    if int(page) == int(1):
        first_categ_answers = Answer.objects.filter(question=random_selected_questions.first())
    else:
        first_categ_answers = Answer.objects.filter(question=question_id)

    # get the next question
    if question_id is not None and random_selected_questions_ids.index(question_id) < len(random_selected_questions_ids)-1:
        next_question = random_selected_questions_ids[random_selected_questions_ids.index(question_id)+1]
    else:
        next_question = random_selected_questions_ids[1]

    active_category = first_categ
    next_question_position = random_selected_questions_ids.index(next_question)
    if next_question_position > len(first_categ_questions) + len(second_categ_questions_ids) + len(third_categ_questions):
        active_category = last_categ
    elif next_question_position > len(first_categ_questions) + len(second_categ_questions_ids):
        active_category = third_categ
    elif next_question_position > len(first_categ_questions):
        active_category = second_categ

    context = {
        'categories': categories,
        'first_categ': first_categ,
        'second_categ': second_categ,
        'first_categ_questions': first_categ_questions,
        'first_categ_answers': first_categ_answers,
        'first_category_page_questions': questions_per_category_per_page,
        'next_question': next_question,
        'active_category': active_category
    }

    return render(request, 'quizes/simc_test.html', context)

@login_required(login_url='/accounts/login')
def simulation_b(request):
    return render(request, 'quizes/sim_b.html')


def user_account(request):
    return render(request, 'quizes/user_account.html')


@login_required(login_url='/accounts/login')
def category(request, category_id, question_id=None):
    category = get_object_or_404(Category, pk=category_id)

    # get all questions for category
    questions = Question.objects.filter(category=category_id)
    total_questions = questions.count()
    
    # show 1 question per page.
    paginator = Paginator(questions, 1)
    page = request.GET.get('page') if request.GET.get('page') else 1
    page_questions = paginator.get_page(page)

    # get all answers of a question
    if int(page) == int(1):
        answers = Answer.objects.filter(question=questions.first())
    else:
        answers = Answer.objects.filter(question=question_id)

    context = {
        'category': category,
        'questions': page_questions,
        'total_questions': total_questions,
        'answers': answers
    }
    return render(request, 'quizes/category.html', context)


@login_required(login_url='/accounts/login')
def save_quiz(request):
    # generate survey hash
    survey_hash = uuid.uuid4()

    if request.method == 'POST':
        correct_answers = request.POST['correct_answers']
        incorrect_answers = request.POST['incorrect_answers']

        # check if values already exists - if yes PASS else INSERT
        check_if_exists = UserDashboard.objects.filter(
                correct_answers = request.POST['correct_answers'],
                incorrect_answers = request.POST['incorrect_answers'],
                user = User.objects.filter(username=request.user)[0],
                survey = survey_hash
            ).count()

        if check_if_exists == 0:
            quiz = UserDashboard(
                correct_answers = correct_answers, 
                incorrect_answers = incorrect_answers,
                user = User.objects.filter(username=request.user)[0],
                survey = survey_hash
            )
            quiz.save()
            messages.success(request, 'Datele au fost salvate in DB')
            return redirect('quizes:enter_platform')
        else:
            pass

    return render(request, 'quizes/category.html')


@login_required(login_url='/accounts/login')
def save_quiz_details(request, question_id=None):
    # generate survey hash
    survey_hash = uuid.uuid4()
    messages.info(request, request.POST)

    if request.method == 'POST':
        # save the correct & wrong answers every time question is changed
        correct_answers = request.POST['correct_answers']
        incorrect_answers = request.POST['incorrect_answers']

        # check if survey hash is already saved
        # if exists make an UPDATE otherwise INSERT
        check_if_exists = UserDashboard.objects.filter(
                user = User.objects.filter(username=request.user)[0],
                survey = survey_hash
            ).count()
        messages.info(request, f'exista = {check_if_exists}')
        if check_if_exists:
            # update
            UserDashboard.objects.filter(
                user = User.objects.filter(username=request.user)[0],
                survey = survey_hash
            ).update(
                correct_answers = request.POST['correct_answers'],
                incorrect_answers = request.POST['incorrect_answers']
            )

            # second part is to insert all information about the survey answers
            # get question id
            question = Question.objects.filter(id=question_id)
            q_id = question[0].id           # q_id = question_id
            c_id = question[0].category_id  # c_id = category id

            # obtain the correct answer based on current question
            answer = Answer.objects.filter(question=q_id, correct=True)
            correct_answer = answer[0].id
            user_selected_answer = request.POST[f'answer_question_{q_id}']

            UserDashboardDetails(
                survey_id=survey_hash,
                category_id=c_id,
                question_id=q_id,
                correct_answer=correct_answer,
                user_selected_answer=user_selected_answer
            ).save()
        else:
            # insert
            UserDashboard(
                correct_answers = correct_answers,
                incorrect_answers = incorrect_answers,
                user = User.objects.filter(username=request.user)[0],
                survey = survey_hash
            ).save()

            messages.success(request, 'Datele au fost salvate in DB')

    return render(request, 'quizes/category.html')