from flask import Blueprint, session, render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from sqlalchemy import and_


from models.user import User
from models.questions import Question, UserQuestionHistory, Section
from extensions import db

page_transition_bp = Blueprint(name='page_transition', import_name=__name__,
                               template_folder='templates', static_folder='static')


@page_transition_bp.route('/quiz_entrance')
def quiz_entrance():
    return render_template('questions/quiz_entrance.html')


def query_result_to_list(query_results):
    return [result[0] for result in query_results]


@page_transition_bp.route('/courses')
def course_list():
    query_results = db.session.query(Section.category).distinct().all()
    course_list = query_result_to_list(query_results)
    print(course_list)
    return render_template('page_transition/course_list.html', course_list=course_list)


@page_transition_bp.route('/<course>/chapters')
def chapter_list(course):
    query_results = db.session.query(Section.chapter).filter(
        Section.category == course).distinct().all()
    chapter_list = query_result_to_list(query_results)
    return render_template('page_transition/chapter_list.html', course=course, chapter_list=chapter_list)


@page_transition_bp.route('/<chapter>/units')
def unit_list(chapter):
    query_results = db.session.query(Section.unit).filter(
        Section.chapter == chapter).distinct().all()
    unit_list = query_result_to_list(query_results)
    return render_template('page_transition/unit_list.html', chapter=chapter, unit_list=unit_list)


@page_transition_bp.route('/<unit>/lectures')
def section_list(unit):
    query_results = db.session.query(Section.section_name).filter(
        Section.unit == unit).distinct().all()
    section_list = query_result_to_list(query_results)
    return render_template('page_transition/section_list.html', unit=unit, section_list=section_list)


@page_transition_bp.route('/<section>/quiz_entrance')
def section_quiz_entrance(section):
    return render_template('page_transition/section_quiz_entrance.html', section=section)


@page_transition_bp.route('/question_page', methods=['GET', 'POST'])
def quiz_page():

    # sessionのquestion_id_listをもとにDBからquestionを取得する
    question_index = session['question_index']
    question_id = session['question_id_list'][question_index]
    question = Question.query.get_or_404(question_id)
    session['correct_answer'] = question.correct_answer

    # 回答がPOSTされた時の処理
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        is_correct = (user_answer == session['correct_answer'])
        if session['question_index'] >= session['amount']:
            accuracy = sum(session['user_answers']) / session['amount']
            reset_quiz_session()
            return redirect(url_for('question.result_page'))
        else:
            # record_question_history(question)
            session['question_index'] += 1
            return redirect(url_for('question.quiz_page'))
    return render_template('questions/quiz_page.html', question=question)


@page_transition_bp.route('/qid-<int:question_id>')
def question_detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('questions/question_detail.html', question=question)
