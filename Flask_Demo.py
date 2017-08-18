from flask import Flask, render_template, redirect, url_for, make_response
from flask import flash,session
from wtforms import Form, TextField, validators, PasswordField, BooleanField
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from flask import request
from flask import current_app
from flask_bootstrap import Bootstrap
from HopUp_Database_Code import *
#from JumpUp import JumpUpDB_URL
import simplejson as json
import smtplib
import boto3

from email.mime.text import MIMEText
# from JumpUp import JumpUpDB_URL
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

# from passlib.hash import sha256_crypt
# from psycopg2.extensions import adapt as thwart
from cryptography.fernet import Fernet
from flask import Flask, render_template, redirect, url_for, make_response
from flask import current_app
from flask import flash, session
from flask import request
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash
from wtforms import Form, TextField, validators, PasswordField, BooleanField

from HopUp_Database_Code import *

msg = MIMEText(
    'From: HopUp \n Subject: Project collaboration invitation \n Hello!! Your team mate is inviting you to collaborate and help with their project on hopup',
    'plain', 'utf-8')
msg['Subject'] ='Collaboration Invitation'
msg['From'] = 'Jump Up'
reward_message = MIMEText("The sponsorer has donated the amount and is now eligible for the reward you have created. Please prepate to ship the reward.")
reward_message['Subject'] = 'Sponsorer is now eligible for a reward'
reward_message['From'] = 'Jump Up'
reward_message['To'] = 'Project Creator'

from_addr = 'craftingideas.25@gmail.com'
password = 'SuperUser'
try:
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    s.login(from_addr, password)
except:
    pass

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

#UploadFolder = '/static/'

ctx = app.app_context()
# flask.g.projectTitl=''
# ctx.push()
key = Fernet.generate_key()
f = Fernet(key)
bootstrap = Bootstrap(app)
try:
    create_user_table()
    create_project_table()
    create_reward_table()
    create_personal_info_table()
    create_bank_account_info_table()
    create_project_detailed_info_table()
    create_sponsor_table()
except:
    pass

@app.route('/')
def test():
    return render_template("home.html")


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if request.method == 'GET':
        un = ""
        try:
            un = session['UserName']
            print(un)
            if un != "":
                projects = search_projects_by_username(un)
                return render_template('dashboard.html',projects=projects)
            else:
                return render_template('login.html')
        except:
            projects = view_projects()
            return render_template('dashboard.html',projects=projects)

@app.route('/app_name')
def app_context_learning():
    print(app.url_map)
    return current_app.name

@app.route('/delete_project',methods=['GET','POST'])
def delete_project():
    projectID = request.args.get('projectID')
    print(projectID)
    delete_project_with_id(projectID)
    return render_template('home.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('pwd')
        user_details = validate_user(username)
        if len(user_details) == 0:
            flash("No user registered under this user name")
            return redirect(url_for('register_page'))
        else:
            pwd = user_details[0][1]
            print(pwd)
            password_check = check_password_hash(pwd,password)
            if password_check:
                session['UserName'] = username
                session['Login'] = True
                print("logged in the user")
                return render_template('home.html')
            else:
                print(user_details)
                print(pwd)
                return render_template('login.html')

@app.route('/logout')
def logout():
    session['UserName'] = ""
    session['Login'] = False
    return render_template('login.html')

@app.route('/sign_s3/')
def sign_s3():
    S3_BUCKET = os.environ.get('S3_BUCKET')
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')
    print(file_name)
    print(file_type)
    s3 = boto3.client('s3')
    presigned_post = s3.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key=file_name,
        Fields={"acl": "public-read", "Content-Type": file_type},
        Conditions=[
            {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn=3600
    )
    return json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
    })

@app.route('/register/', methods=["GET", "POST"])
def register_page():
    class FormRegistration(Form):
        username = TextField('Username', [validators.Length(min=4, max=20)])
        email = TextField('Email Address', [validators.Length(min=6, max=50)])
        password = PasswordField('New Password', [
            validators.Length(min=6, max=50),
            validators.Required(),
            validators.EqualTo('confirm', message='Passwords must match')
        ])
        confirm = PasswordField('Repeat Password')
        accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice',
                                  [validators.Required()])

    try:
        form = FormRegistration(request.form)
        if request.method == "POST" and form.validate():
            username = str(form.username.data)
            email = str(form.email.data)
            passw = str(form.password.data)
            password = generate_password_hash(passw)

            c, conn = connections()

            c.execute("Select EXISTS (SELECT * FROM USERS WHERE username = %s)",(username,))
            if c.fetchone()[0]:
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO USERS(UserName, PassWord, EmailId) VALUES (%s, %s, %s)",(username,password,email))
                conn.commit()
                return redirect(url_for('login'))

        return render_template("register.html", form=form)
    except Exception as e:
        return (str(e))


@app.route('/story', methods=['POST', 'GET'])
def story():
    if request.method == 'GET':

        return render_template("story.html")
    elif request.method == 'POST':
        pt = request.cookies.get('projectTitle')
        project_video_link = request.form.get('projectVideoLink')
        project_Detailed_Description = request.form.get('projectDetails')
        pdid = len(view_project_detailed_info()) + 1
        add_project_detailed_info(pdid, pt, project_video_link, project_Detailed_Description)
        return render_template('more_about_you.html')


@app.route('/project_register', methods=['POST', 'GET'])
def project_registration():
    if request.method == 'GET':
        resp = make_response(render_template('register_project.html'))
        resp.set_cookie('UserName', '')
        return resp
    elif request.method == 'POST':
        project_title = request.form.get('project_title')
        project_category = request.form.get('ddl1')
        project_sub_category = request.form.get('ddl2')
        project_country = request.form.get('projectCountry')
        project_image = request.form.get('project_image')
        project_description = request.form.get('project_description')
        project_location = request.form.get('project_location')
        project_fund_duration = request.form.get('fund_duration')
        project_fund_goal = request.form.get('fundGoal')
        dt = str(datetime.now())
        # print(type(project_image))
        # image_str = base64.b64encode(request.files.get('project_image',''))
        projects = search_projects_by_title(project_title)
        if len(projects) >= 1:
            return render_template("register_project.html")
        else:
            next_id = len(view_projects()) + 1
            un = ""
            try:
                un = session['UserName']
            except:
                un = "Guest"
            add_project(next_id, project_title, un, project_category, project_sub_category, project_country,
                        project_image, project_description, project_location, project_fund_duration, project_fund_goal,project_fund_goal,dt)
        resp = make_response(render_template('rewards.html'))
        resp.set_cookie('projectTitle', project_title)
        reward()
        return resp


@app.route('/invite', methods=['POST', 'GET'])
def invite():
    return render_template("invite_collaborator.html")


@app.route('/more_about_you', methods=['POST', 'GET'])
def more_about_you():
    if request.method == 'GET':
        return render_template("more_about_you.html")
    elif request.method == 'POST':
        profile_image = request.form.get('profileimage')
        facebook_url = request.form.get('fbProfile')
        personal_website_url = request.form.get('website')
        personal_location = request.form.get('location')
        github_url = request.form.get('giturl')
        biography = request.form.get('biography')
        next_id = len(view_personal_info()) + 1
        un = ""
        try:
            un = session['UserName']
        except:
            un = "Guest"
        add_personal_info(next_id, un, profile_image, facebook_url, personal_website_url, personal_location, github_url,
                          biography)
        return render_template('bank_details.html')


@app.route('/account_details', methods=['POST', 'GET'])
def account_details():
    if request.method == 'GET':
        return render_template("bank_details.html")
    elif request.method == 'POST':
        contact_email = request.form.get('contactEmail')
        firstName = request.form.get('fn')
        lastName = request.form.get('ln')
        DOB = request.form.get('DOB')
        HomeAddress = request.form.get('homeAddress')
        RoutingNumber = request.form.get('routingNumber')
        bankAccountNumber = request.form.get('BankAccountNumber')
        next_id = len(view_bank_account_info()) + 1
        un = ""
        try:
            un = session['UserName']
        except:
            un = "Guest"
        add_bank_account_info(next_id, un, contact_email, firstName, lastName, DOB, HomeAddress, RoutingNumber,
                              bankAccountNumber)
        #project_details = search_projects_by_title(request.cookies.get('projectTitle'))
        project_details = view_projects()
        return render_template('project_overview.html', projectList=project_details)


@app.route('/send_invite', methods=['POST', 'GET'])
def send_invite():
    to_addr = request.form.get('col_email')
    s.sendmail(from_addr, [to_addr], msg.as_string())
    print("Invitation sent successfully")
    return render_template("rewards.html")

@app.route('/explore',methods=['POST','GET'])
def explore():
    projects = view_projects()
    return render_template('project_overview.html',projectList=projects)


@app.route('/save_reward', methods=['POST', 'GET'])
def save_reward():
    ## Database code to save the rewad details in the reward table
    return redirect(url_for('reward'))


@app.route('/reward', methods=['POST', 'GET'])
def reward():
    if request.method == 'GET':
        print(request.cookies.get('projectTitle'))
        return render_template("rewards.html")
    elif request.method == 'POST':
        reward_title = request.form.get('rewardTitle')
        pledged_amount = request.form.get('pledgedAmount')
        reward_description = request.form.get('rewardDescription')
        expected_delivery_month = request.form.get('month')
        expected_delivery_year = request.form.get('year')
        shippingDetails = request.form.get('shippingDetails')
        reward_limit = request.form.get('rewardLimit')
        print(reward_title)
        un = ""
        try:
            un = session['UserName']
        except:
            un = "Guest"
        pt = request.cookies.get('projectTitle')
        next_id = len(view_rewards()) + 1
        add_reward(next_id, reward_title, pt, un, pledged_amount, reward_description, expected_delivery_month,
                   expected_delivery_year, shippingDetails, reward_limit)
        return render_template('rewards.html')

@app.route('/donate',methods=['POST','GET'])
def donate():
    if request.method == 'GET':
        pid = request.args.get("projectID")
        #print(pid)
        return render_template('donateAmount.html',pid=pid)
    elif request.method == 'POST':
        id = int(request.form.get('projectID'))
        fn = str(request.form.get('fn'))
        ln = str(request.form.get('ln'))
        amount_pledged = int(request.form.get('pledgeAmount'))
        projectTitle = str(request.form.get('projectTitle'))
        print(projectTitle)
        address = str(request.form.get('address'))
        rewards = search_reward_by_project(projectTitle)
        #print("Rewards")
        print(rewards)
        try:
            for reward in rewards:
                amount = int(reward[4])
                print(amount)
                print(amount_pledged)
                if amount_pledged >= amount:
                    project_details = search_projects_by_id(id)
                    creator = project_details[0][2]
                    print(creator)
                    user_details = get_user_details(creator)
                    user_email = str(user_details[0][3])
                    s.sendmail(from_addr,user_email, reward_message.as_string())
        except:
            pass


        if pledge_amount(id,amount_pledged):
            flash("Pledged Successfully")
            sponsors = search_sponsor(fn, ln)
            #print(sponsors)
            if len(sponsors) >= 1:
                previous_project_id = sponsors[0][6]
                #print(type(previous_project_id))
                #print(type(id))
                #print(type(fn))
                #print(type(ln))
                if previous_project_id == id:
                    #print("Yes i am already there")
                    prev_amount = sponsors[0][5]
                    pa = int(prev_amount) + int(amount_pledged)
                    update_sponsor_table(pa,id)
                else:
                    next = len(view_sponsors()) + 1
                    add_sponsor(next,fn,ln,address,amount_pledged,id)
                projects = view_projects()
                return render_template('project_overview.html',projectList=projects)
            else:
                next = len(view_sponsors()) + 1
                add_sponsor(next, fn, ln, address,amount_pledged, id)
                projects = view_projects()
                return render_template('project_overview.html',projectList=projects)
        else:
            flash("Transaction unsuccessful and is rolled back")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404



def validate_project_title(ptitle):
    if not ptitle.isalpha():
        return False
    else:
        return True


def validate_funding_duration(pfunddur):
    if not pfunddur.isdigit():
        return False
    else:
        return True


def validate_fund_goal(pfundgoal):
    if not pfundgoal.isdigit():
        return False
    else:
        return True


if __name__ == "__main__":
    app.run(debug=True)
