from flask import Flask,render_template,redirect,request, session,flash
from flask import current_app as app
from flask import Flask
from .models import *
from .database import db
import os

# app = Flask(__name__)



@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        this_user = User.query.filter_by(username=username).first()#lhs is main check part and rhs will change according to input
        if this_user:
            if this_user.password == pwd:
                session['user_id'] = this_user.id
                session['username'] = username
                if this_user.type == "admin":
                    this_user = User.query.first() 
                    subjects=Subject.query.all()
                    return redirect("/admin_dashboard")
                else:
                    quizzes = Quiz.query.all() 
                    return redirect("/user_dashboard")
            else:
                return "password is wrong"
        else:
            return "user does not exist"
    return render_template("login.html")






@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        fullname = request.form.get("fullname")
        qualification = request.form.get("qualification")
        dob =request.form.get("dob")
        this_user = User.query.filter_by(username=username).first()
        if this_user:
            return "user already exists"
        else:
            new_user=User(username=username, password=pwd, fullname=fullname, qualification=qualification, dob=dob)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html")
        



    return render_template('register.html')

@app.route("/add_chapter",methods=["GET","POST"])
def add_chapter():
    if request.method == 'POST':
        this_user = User.query.first() 
        subjects=Subject.query.all()
        name = request.form.get('name')
        description = request.form.get('description')
        subject_id = request.form.get('subject_id')
        
        if not name or not subject_id:
            flash('Chapter name and subject are required', 'error')
            return render_template("admin/add_chapter.html")
              
        new_chapter = Chapter(name=name, description=description, subject_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        chapters = Chapter.query.all()
        subjects = Subject.query.all()
            
            # flash('Chapter added successfully', 'success')
        return redirect("/admin_dashboard")
    
    # chapters = Chapter.query.all()
    # subjects = Subject.query.all()

    return render_template("admin/add_chapter.html")

@app.route("/edit_chapter/<int:chapter_id>", methods=["GET", "POST"])
def edit_chapter(chapter_id):
    # Find the chapter
    chapter = Chapter.query.get_or_404(chapter_id)
    
    if request.method == "POST":
        # Update chapter with form data
        chapter.name = request.form.get('name')
        chapter.description = request.form.get('description')
        chapter.subject_id = request.form.get('subject_id')
        
        # Validate chapter name
        if not chapter.name:
            flash('Chapter name is required', 'error')
            subjects = Subject.query.all()
            return render_template("admin/edit_chapter.html", chapter=chapter, subjects=subjects)
        
        # Check if another chapter has the same name (excluding this one)
        existing_chapter = Chapter.query.filter(
            Chapter.name == chapter.name,
            Chapter.id != chapter_id
        ).first()
        
        if existing_chapter:
            flash('A chapter with this name already exists', 'error')
            subjects = Subject.query.all()
            return render_template("admin/edit_chapter.html", chapter=chapter, subjects=subjects)
        
        # Save changes
        db.session.commit()
        
        # Redirect to admin dashboard with success message
        this_user = User.query.first() 
        subjects = Subject.query.all()
        chapters = Chapter.query.all()
        return redirect("/admin_dashboard")
    
    # GET request - show edit form with chapter data
    subjects = Subject.query.all()
    return render_template("admin/edit_chapter.html", chapter=chapter, subjects=subjects)

@app.route("/delete_chapter/<int:chapter_id>", methods=["GET", "POST"])
def delete_chapter(chapter_id):
    # Find the user
    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    
    
    for quiz in quizzes:
        
        Question.query.filter_by(quiz_id=quiz.id).delete()
        Score.query.filter_by(quiz_id=quiz.id).delete()
    Quiz.query.filter_by(chapter_id=chapter_id).delete()
    
    db.session.delete(chapter)
    db.session.commit()
    this_user = User.query.first() 
    chapters = Chapter.query.all()
    subjects = Subject.query.all()
    
    return redirect("/admin_dashboard")
            
 

@app.route("/add_subject", methods=["GET", "POST"])
def add_subject():
    if request.method == "POST":
        this_user = User.query.first() 
        subjects=Subject.query.all()
        subjectname = request.form.get("name")
        description = request.form.get("description")
        
        # Validate subject name
        if not subjectname:
            flash("Subject name cannot be empty")
            return render_template("admin/add_subject.html")
        
        
        else:
                # Check if subject already exists
            existing_subject = Subject.query.filter_by(name=subjectname).first()
            if existing_subject:
                flash("A subject with this name already exists", "error")
                return render_template("admin/add_subject.html")
                
                # Create new subject
            this_subject = Subject(name=subjectname, description=description)
            db.session.add(this_subject)
            db.session.commit()
            chapters = Chapter.query.all()
            subjects = Subject.query.all()
            
            # flash("Subject added successfully", "success")
            return redirect("/admin_dashboard")
        
        # except Exception as e:
        #     db.session.rollback()
        #     flash(f"Error adding subject: {str(e)}", "error")
        #     app.logger.error(f"Database error: {str(e)}")
        #     return render_template("admin/add_subject.html")
    
    # GET request
    return render_template("admin/add_subject.html")

@app.route("/edit_subject/<int:subject_id>", methods=["GET", "POST"])
def edit_subject(subject_id):
    # Find the subject
    subject = Subject.query.get_or_404(subject_id)
    this_user = User.query.filter_by(type="admin").first()
    
    if request.method == "POST":
        # Update subject with form data
        subject.name = request.form.get('name')
        subject.description = request.form.get('description')
        
        # Validate subject name
        if not subject.name:
            flash('Subject name is required', 'error')
            return render_template("admin/edit_subject.html", subject=subject,this_user=this_user)
        
        # Check if another subject has the same name (excluding this one)
        existing_subject = Subject.query.filter(
            Subject.name == subject.name,
            Subject.id != subject_id
        ).first()
        
        if existing_subject:
            flash('A subject with this name already exists', 'error')
            return render_template("admin/edit_subject.html",this_user=this_user, subject=subject)
        
        # Save changes
        db.session.commit()
        
        # Redirect to admin dashboard
        this_user = User.query.first() 
        subjects = Subject.query.all()
        return redirect("/admin_dashboard")
    
    # GET request - show edit form with subject data
    return render_template("admin/edit_subject.html",this_user=this_user, subject=subject)

@app.route("/delete_subject/<int:subject_id>", methods=["GET", "POST"])
def delete_subject(subject_id):
    # Find the subject
    subject = Subject.query.get_or_404(subject_id)
    
    # Get all chapters associated with this subject
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    
    # For each chapter, delete all quizzes and their questions
    for chapter in chapters:
        # Get all quizzes for this chapter
        quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()
        
        # For each quiz, delete all questions and scores
        for quiz in quizzes:
            # Delete all questions for this quiz
            Question.query.filter_by(quiz_id=quiz.id).delete()
            
            # Delete all scores for this quiz
            Score.query.filter_by(quiz_id=quiz.id).delete()
        
        # Delete all quizzes for this chapter
        Quiz.query.filter_by(chapter_id=chapter.id).delete()
    
    # Delete all chapters for this subject
    Chapter.query.filter_by(subject_id=subject_id).delete()
    
    # Finally, delete the subject itself
    db.session.delete(subject)
    db.session.commit()
    
    # Redirect to admin dashboard
    this_user = User.query.first() 
    subjects = Subject.query.all()
    return redirect("/admin_dashboard")




@app.route("/admin_dashboard",methods=["GET","POST"])
def admin_dashboard():
    this_user = User.query.filter_by(type="admin").first()
    subjects=Subject.query.all()
    chapters = Chapter.query.all()
    return render_template("admin/admin_dashboard.html", this_user=this_user,subjects=subjects,chapters=chapters)


@app.route("/quiz_management",methods=["GET","POST"])
def quiz_management():
    this_user = User.query.filter_by(type="admin").first()
    quizzes = Quiz.query.all()
    chapters = Chapter.query.all()
    questions = Question.query.all() 
    return render_template("admin/quiz_management.html", this_user=this_user,quizzes=quizzes,chapters=chapters,questions=questions)

# @app.route("/logout")
# def logout():
#     session.pop('user_id', None)
#     return redirect("/login")

@app.route("/add_quiz",methods=["GET","POST"])
def add_quiz():
    if request.method == 'POST':
        this_user = User.query.first() 
        quizzes = Quiz.query.all()
        
        chapter_id = request.form.get('chapter_id')
        date_str = request.form.get('date_of_quiz')
        time_duration = request.form.get('time_duration')
        remarks = request.form.get('remarks')
        
        if not chapter_id or not date_str or not time_duration:
            flash('Chapter, date, and duration are required', 'error')
            return render_template("admin/add_quiz.html")
        
        try:
            date_str = dt.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD', 'error')
            return render_template("admin/add_quiz.html")
        
        # Convert duration to integer
        try:
            time_duration = int(time_duration)
            if time_duration <= 0:
                raise ValueError("Duration must be positive")
        except ValueError:
            flash('Duration must be a positive number', 'error')
            return render_template("admin/add_quiz.html")
            
      
            
        new_quiz = Quiz(
            chapter_id=chapter_id,
            date_of_quiz=date_str,
            time_duration=time_duration)
        db.session.add(new_quiz)
        db.session.commit()
        quizzes = Quiz.query.all()
        chapters = Chapter.query.all()
        questions = Question.query.all()
        
        # flash('Quiz added successfully', 'success')
        return redirect("/quiz_management")
        
    quizzes = Quiz.query.all()
    chapters = Chapter.query.all()
    questions = Question.query.all()
    return render_template('admin/add_quiz.html', quizzes=quizzes, chapters=chapters)

@app.route("/edit_quiz/<int:quiz_id>", methods=["GET", "POST"])
def edit_quiz(quiz_id):
    # Find the quiz
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == "POST":
        # Update quiz with form data
        quiz.chapter_id = request.form.get('chapter_id')
        date_str = request.form.get('date_of_quiz')
        quiz.time_duration = request.form.get('time_duration')
        
        # # Validate input
        if not quiz.chapter_id or not date_str or not quiz.time_duration:
            flash('Chapter, date, and duration are required', 'error')
            chapters = Chapter.query.all()
            return render_template("admin/edit_quiz.html",quiz=quiz, chapters=chapters)
        
        # Parse date
        try:
            quiz.date_of_quiz = dt.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD', 'error')
            chapters = Chapter.query.all()
            return render_template("admin/edit_quiz.html", quiz=quiz, chapters=chapters)
        
        # Convert duration to integer
        try:
            quiz.time_duration = int(quiz.time_duration)
            if quiz.time_duration <= 0:
                raise ValueError("Duration must be positive")
        except ValueError:
            flash('Duration must be a positive number', 'error')
            chapters = Chapter.query.all()
            return render_template("admin/edit_quiz.html", quiz=quiz, chapters=chapters)
        
        # Save changes
        db.session.commit()
        
        # Redirect to quiz management page
        this_user = User.query.first()
        quizzes = Quiz.query.all()
        return redirect("/quiz_management")
    
    # GET request - show edit form with quiz data
    chapters = Chapter.query.all()
    return render_template("admin/edit_quiz.html", quiz=quiz, chapters=chapters)

@app.route("/delete_quiz/<int:quiz_id>", methods=["GET", "POST"])
def delete_quiz(quiz_id):
    # Find the quiz
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Delete all questions associated with this quiz
    Question.query.filter_by(quiz_id=quiz_id).delete()
    
    # Delete all scores associated with this quiz
    Score.query.filter_by(quiz_id=quiz_id).delete()
    
    # Delete the quiz itself
    db.session.delete(quiz)
    db.session.commit()
    
    # Redirect back to quiz management page
    this_user = User.query.first()
    quizzes = Quiz.query.all()
    return redirect("/quiz_management")


@app.route("/add_question",methods=["GET","POST"])
def add_question():
    if request.method == 'POST':
        this_user = User.query.first()
        quizzes = Quiz.query.all() 
        questions = Question.query.all()
        quiz_id =request.form.get('quiz_id')
        question_statement = request.form.get('question_statement')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        correct_option = request.form.get('correct_option')
        
        if not quiz_id or not question_statement or not option1 or not option2 or not option3 or not option4 or not correct_option:
            flash('All fields are required', 'error')
            return render_template('admin/add_question.html')
            
        new_question = Question(
            quiz_id=quiz_id,
            question_text=question_statement,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=int(correct_option)
        )
        db.session.add(new_question)
        db.session.commit()
        
        flash('Question added successfully', 'success')
        return redirect('/quiz_management')
        
    # questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return render_template('admin/add_question.html')

@app.route("/edit_question/<int:question_id>", methods=["GET", "POST"])
def edit_question(question_id):
   
    question = Question.query.get_or_404(question_id)
    
    if request.method == "POST":
        # Update question with form data
        question.question_text = request.form.get('question_statement')
        question.option1 = request.form.get('option1')
        question.option2 = request.form.get('option2')
        question.option3 = request.form.get('option3')
        question.option4 = request.form.get('option4')
        question.correct_option = int(request.form.get('correct_option'))
        db.session.commit()
        return redirect("/quiz_management")
        
        # Save changes
        # try:
        #     db.session.commit()
        #     flash('Question updated successfully', 'success')
        #     return redirect("/quiz_management")
        # except Exception as e:
        #     db.session.rollback()
        #     flash(f'Error updating question: {str(e)}', 'error')
    quizzes = Quiz.query.all()  
    return render_template("admin/edit_question.html", question=question)

@app.route("/delete_question/<int:question_id>", methods=["GET", "POST"])
def delete_question(question_id):
    # Verify admin is logged in
    if not session.get('user_id'):
        return redirect("/login")
    
    # Get question to delete
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    
    # Delete the question
    # try:
    #     db.session.delete(question)
    #     db.session.commit()
    #     flash('Question deleted successfully', 'success')
    # except Exception as e:
    #     db.session.rollback()
    #     flash(f'Error deleting question: {str(e)}', 'error')
    
    return redirect("/quiz_management")

@app.route("/summary", methods=["GET"])
def summary():
    # Get the admin user
    this_user = User.query.filter_by(type="admin").first()
    
    # Query to get all scores with related information
    # We need to join multiple tables to get all the required data
    scores_data = db.session.query(
        Score,
        User,
        Quiz,
        Chapter,
        Subject
    ).join(
        User, Score.user_id == User.id
    ).join(
        Quiz, Score.quiz_id == Quiz.id
    ).join(
        Chapter, Quiz.chapter_id == Chapter.id
    ).join(
        Subject, Chapter.subject_id == Subject.id
    ).all()
    
    # Prepare the data for display
    summary_data = []
    for score, user, quiz, chapter, subject in scores_data:
        summary_data.append({
            'score_id': score.id,
            'user_id': user.id,
            'fullname': user.fullname,
            'subject_id': subject.id,
            'chapter_id': chapter.id,
            'quiz_id': quiz.id,
            'date_time': score.attempt_date.strftime('%Y-%m-%d %H:%M') if score.attempt_date else 'N/A',
            'score': score.score
        })
    
    return render_template("admin/summary.html", this_user=this_user, summary_data=summary_data)

@app.route("/user_list")
def user_list():
    this_user = User.query.filter_by(type="admin").first()
    users = User.query.filter_by(type="general").all()  # Only get non-admin users
    return render_template("admin/user_list.html", this_user=this_user, users=users)

@app.route("/delete_user/<int:user_id>", methods=["POST", "GET"])
def delete_user(user_id):
    # Find the user
    user = User.query.get_or_404(user_id)
    
    # Delete associated scores first (optional if you've set up cascade)
    Score.query.filter_by(user_id=user_id).delete()
    
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    
    return redirect("/user_list")

@app.route("/user_score",methods=["GET","POST"])
def user_score():
    username = session.get('username') 
    this_user = User.query.filter_by(username=username).first()
    scores=Score.query.all()
    return render_template("user/user_score.html", this_user=this_user,scores=scores)
    
@app.route("/user_dashboard")
def user_dashboard():
    # Check if user is logged in
    username = session.get('username')
    if not username:
        return redirect("/login")
    
    this_user = User.query.filter_by(username=username).first()
    if not this_user:
        return redirect("/login")
    
    # Get all quizzes to display to the user
    quizzes = Quiz.query.all() 
    chapters = Chapter.query.all()
    return render_template("user/user_dashboard.html", this_user=this_user, quizzes=quizzes, chapters=chapters)


@app.route("/start_quiz/<int:quiz_id>", methods=["GET"])
def start_quiz(quiz_id):
    # Check if user is logged in
    username = session.get('username')
    # if not username:
    #     return redirect("/login")
    
    this_user = User.query.filter_by(username=username).first()
    # if not this_user:
    #     return redirect("/login")
    
    # Get the quiz details
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Get all questions for this quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # If no questions, redirect back with message
    if not questions:
        flash("This quiz has no questions yet!", "warning")
        return redirect("/user_dashboard")
    
    # Calculate end time for the quiz
    start_time = dt.now()
    end_time = start_time + timedelta(minutes=quiz.time_duration)
    session['quiz_start_time'] = start_time.timestamp()
    session['quiz_end_time'] = end_time.timestamp()
    session['current_quiz_id'] = quiz_id
    
    # Return first question
    return render_template("user/start_quiz.html", 
                          quiz=quiz, 
                          questions=questions, 
                          current_question=0, 
                          total_questions=len(questions),
                          user=this_user,
                          time_remaining=quiz.time_duration*60)  # Time in seconds


@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():
    # Get the user ID from session - using user_id is more reliable than username
    user_id = session.get('user_id')
    
    # If no user ID in session, try to get it by username
    # if not user_id and session.get('username'):
    #     # Try to find user by username
    #     username = session.get('username')
    #     this_user = User.query.filter_by(username=username).first()
    #     if this_user:
    #         user_id = this_user.id
    #         # Update session with user_id for future requests
    #         session['user_id'] = user_id
    
    # If still no user_id, redirect to login
    # if not user_id:
    #     flash("Session expired. Please log in again.", "error")
    #     return redirect("/login")
    
    # Get the user from the database
   
    
    # If user not found in database (despite having user_id in session)
    # if not this_user:
    #     flash("User not found. Please log in again.", "error")
    #     session.clear()
    #     return redirect("/login")
    
    # Get quiz_id from session
    quiz_id = session.get('current_quiz_id')
    # if not quiz_id:
    #     flash("Quiz session expired", "danger")
    #     return redirect("/user_dashboard")
    
    # Get the quiz and questions
    quiz = Quiz.query.get(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Calculate score
    score = 0
    for question in questions:
        selected_option = request.form.get(f"question_{question.id}")
        if selected_option and int(selected_option) == question.correct_option:
            score += 1
    
    # Calculate percentage
    percentage = (score / len(questions)) * 100 if questions else 0
    
    this_user = User.query.get(user_id)
    # Save score to database
    new_score = Score(
        user_id=this_user.id,
        quiz_id=quiz_id,
        score=score,
        attempt_date=dt.now()
    )
    db.session.add(new_score)
    db.session.commit()
    
    # Clear quiz session data
    session.pop('quiz_start_time', None)
    session.pop('quiz_end_time', None)
    session.pop('current_quiz_id', None)
    scores=Score.query.all()
    
    # Render results page
    return render_template("user/user_score.html", 
                          score=score, 
                          total=len(questions), 
                          percentage=percentage,
                          this_user=this_user,
                          quiz=quiz,
                          scores=scores)

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Flash a message to inform the user they've been logged out
    # flash('You have been successfully logged out.', 'success')
    # Redirect to the login page
    return redirect("/login")