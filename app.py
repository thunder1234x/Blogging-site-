from flask import Flask , render_template ,request,redirect,session,json
from bson import json_util
from json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


#custom import from model.py file
from model import Blog_post,app,db,User_details
from data import color_code_generator , data


app.config['SECRET_KEY'] = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'



@app.route('/')
def home_page():
    if 'user'  in session:
        id=User_details.query.filter_by(email=session['user']).first().first_name
        return render_template('index.html',info=[id,True])
        # session['user']=json.dumps(MyEncoder().encode(user_checkin_values()),default=json_util.default)
    else:
        return render_template('index.html',info=['',False])
        


@app.route('/user/<int:id>')
def user_auth_homepage(id):
    if 'user' in session:
        logged_in=True
        id=User_details.query.filter_by(email=session['user']).first().first_name
        return render_template('index.html',info=[id,logged_in])
    else:
        return redirect('/')


@app.route('/posts',methods=['GET','POST'])
def show_post():
    if 'user' in session:
        logged_in_user=User_details.query.filter_by(email=session['user']).first().id
        all_post=Blog_post.query.order_by(Blog_post.time_created).all()
        return render_template('post_show.html',posts=[all_post,User_details,logged_in_user])
    else:
        return render_template('index.html',msg='Log in required!!!!')


@app.route('/blogger/post/<string:id>',methods=['GET','POST'])
def show_my_post(id):
    if 'user' in session:
        user_id=User_details.query.filter_by(email=id).first()
        logged_in_user=user_id.id
        all_post=user_id.post
        return render_template('post_show.html',posts=[all_post,User_details,logged_in_user])
    else:
        return render_template('index.html',msg='Log in required!!!!')


@app.route('/posts/new/<string:mailid>',methods=['GET','POST'])
def user_auth_newpost(mailid):
    user_id=User_details.query.filter_by(email=mailid).first()
    user_name=str(user_id.id)
    return render_template('new_post.html',user_name=user_name)


@app.route('/posts/new',methods=['GET','POST'])
def new_post():
    if 'user' in session:
        if request.method == 'POST':
            post_title=request.form['title']
            post_content=request.form['content']
            post_author=request.form['author']
            new_post =Blog_post(title=post_title,content=post_content,owner=User_details.query.filter_by(id=int(post_author)).first())
            db.session.add(new_post)
            db.session.commit()
            return redirect('/posts')
        else:
            return render_template('new_post.html')
    else:
        return redirect('/blogger/login')


@app.route('/posts/delete/<int:id>',methods=['GET'])
def delete_post(id):
    deleted_post=Blog_post.query.get(id)
    # deleted_post_title=deleted_post.title
    db.session.delete(deleted_post)
    db.session.commit()
    return  redirect('/posts')


@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def update_post(id):
    update_post=Blog_post.query.get(id)
    if request.method == 'POST':
        update_post.title =request.form['title']
        update_post.content=request.form['content']
        update_post.author_id=request.form['author']
        update_post.time_created=datetime.now()
        db.session.commit()
        return redirect('/posts')
    else:
        return  render_template('edit.html',num=[id,update_post])


@app.route('/blogger/login',methods=['GET','POST'])
def log_in():
    all_email=[]
    for item in User_details.query.all():
            all_email.append(item.email)

    if request.method == 'POST':
        if 'user' in session:
            return render_template('login_page.html',msg=['You have already logged in.For Another Login Logout required',all_email])
        else:
            if request.form['email']  in all_email :
                db_info=User_details.query.filter_by(email=request.form['email']).first()
                db_pass=db_info.password
                if db_pass==request.form['password']:
                    session['user']=db_info.email
                    return redirect(f'/user/{db_info.id}')
                else:
                    return render_template('login_page.html',msg=['Password not matching with Email Id',all_email])
            else:
                return render_template('login_page.html',msg=['Email Id does not exists.Please Sign Up!',all_email])

    else:
        return render_template('login_page.html',all_mail=all_email)


@app.route('/blogger/signup',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        email=request.form['email']
        password=request.form['password']
        confirm_password=request.form['comfirm_password']
        
        all_email=[]
        for item in User_details.query.all():
            all_email.append(item.email)
        if email in all_email:
            return render_template('signup_page.html',msg='Email Id already Exists.Please Log-in!')
        else:
            if password==confirm_password:
                new_user=User_details(first_name=first_name, last_name=last_name,email=email,password=password)
                db.session.add(new_user)
                db.session.commit()
                return redirect('/blogger/login')
            else:
                return render_template('signup_page.html',msg='password and Confirm Password does not match')
    else:
        return render_template('signup_page.html')


@app.route('/blogger/dashboard',methods=['GET',])
def user_dashboard():
    if 'user' in session:
        return render_template('dashboard.html',color_code=color_code_generator(5) , data=data)


@app.route('/blogger/logout',methods=['GET',])
def user_logout():
    if 'user' in session:
        session.pop('user')
        return redirect('/')




if __name__ == "__main__":
    app.run(debug=True)