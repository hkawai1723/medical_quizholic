from flask import Blueprint, session, render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from sqlalchemy import and_


from models.user import User
from models.questions import Question, UserQuestionHistory, Section
from extensions import db

question_bp = Blueprint(name='question', import_name=__name__,
                        template_folder='templates', static_folder='static')


@question_bp.route('/')
def quiz_entrance():
    return render_template('questions/quiz_entrance.html')


class QuizSet(object):
    # def __init__(self, name, amount, question_id_list, randomized=False):
    #     self.name = name
    #     self.amount = amount
    #     self.question_id_list = question_id_list
    #     self.randomized = randomized
    def __init__(self, section, tags=None, done=None, flag=None, randomized=False):
        self.section = section
        # self.tags = tags
        # self.done = done
        # self.flag = flag
        # self.randomized = randomized


@question_bp.route('/<section>/start_quiz')
def section_quiz(section):
    check_section = db.session.query(Section).filter(
        Section.section_name == section).one_or_404()
    quiz_set = QuizSet(section=section)
    start_quiz(quiz_set)

    return redirect(url_for('question.quiz_page', question_index=session['question_index']))


def reset_quiz_session():

    session.pop('question_index', None)
    session.pop('question_id_list', None)
    session.pop('user_answers', None)
    session.pop('amount', None)
    session.pop('title', None)
    session.pop('accuracy', None)


def start_quiz(quiz_set):
    reset_quiz_session()
    try:
        section = db.session.query(Section).filter(
            Section.section_name == quiz_set.section).one_or_404()
        questions = section.questions
        question_id_list = [question.id for question in questions]

    except Exception as e:
        print(e)
        abort(500)

    session['question_index'] = 0
    session['question_id_list'] = question_id_list
    session['user_answers'] = [0] * len(question_id_list)
    session['amount'] = len(question_id_list)
    session['title'] = quiz_set.section
    session['accuracy'] = 0
    if session['amount'] == 0:
        abort(404)

    return redirect(url_for('question.quiz_page', question_index=session['question_index']))


@question_bp.route('/question_page/<int:question_index>', methods=['GET', 'POST'])
def quiz_page(question_index):
    session['question_index'] = question_index
    # 回答がPOSTされた時の処理
    if request.method == 'POST':
        user_answer = int(request.form.get('answer'))
        print(user_answer)
        print(session['correct_answer'])
        
        is_correct = (user_answer == session['correct_answer'])
        session['user_answers'][session['question_index']] = is_correct
        session['accuracy'] = sum(session['user_answers']) / session['amount']
        
        print(session['user_answers'])

        session['question_index'] += 1
        
        if session['question_index'] >= session['amount']:
            accuracy = session['accuracy']
            reset_quiz_session()
            return redirect(url_for('question.result_page', accuracy=accuracy))
        else:
            # record_question_history(question)
            return redirect(url_for('question.quiz_page', question_index=session['question_index']))

    if session['question_index'] >= session['amount']:
        accuracy = sum(session['user_answers']) / session['amount']
        reset_quiz_session()
        return redirect(url_for('question.result_page', accuracy=accuracy))

    # sessionのquestion_id_listをもとにDBからquestionを取得する
    question_index = session['question_index']
    question_id = session['question_id_list'][question_index]
    question = Question.query.get_or_404(question_id)
    session['correct_answer'] = question.correct_answer

    return render_template('questions/quiz_page.html', question=question)


@question_bp.route('/result_page')
def result_page():
    accuracy = request.args.get('accuracy', default=0, type=float)
    accuracy = round(accuracy * 100, 1)
    return render_template('questions/result_page.html', accuracy=accuracy)


def record_question_history(question):
    user_answer = request.form.get('answer')
    is_correct = (user_answer == question.correct_answer)
    user_question_history = UserQuestionHistory(
        user_id=current_user.id, question_id=question.id, is_correct=is_correct)
    db.session.add(user_question_history)
    db.session.commit()


@question_bp.route('/qid-<int:question_id>')
def question_detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('questions/question_detail.html', question=question)
