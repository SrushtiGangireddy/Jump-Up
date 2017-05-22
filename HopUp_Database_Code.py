import os
import urlparse
import psycopg2
from DatabaseConnection import *
def create_user_table():
    curs=conn.cursor()
    curs.execute(
        "create table if not exists USERS(UserId SERIAL, UserName text,PassWord text, EmailId text)")
    conn.commit()

def validate_user(username):
    curs = conn.cursor()
    curs.execute("select UserName,PassWord from USERS where UserName=%s",(username,))
    users = curs.fetchall()
    return users

def connections():
    c=conn.cursor()
    return c,conn
def create_project_table():
    curs = conn.cursor()
    curs.execute("create table if not exists PROJECT(ProjectID Integer,ProjectTitle text,UserName text,ProjectCategory text,ProjectSubCategory text,ProjectCountry text,ProjectImage text,ProjectDescription text,ProjectLocation text,ProjectFundDuration text,ProjectFundGoal text,Remaining text,StartTime text)")
    conn.commit()

def add_project(pid,ptitle,un,pcat,psubcat,pcountry,pimage,pdesc,ploc,pfunddur,pfundgoal,rem,st):
    curs = conn.cursor()
    curs.execute("insert into PROJECT values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(pid,ptitle,un,pcat,psubcat,pcountry,pimage,pdesc,ploc,pfunddur,pfundgoal,rem,st))
    conn.commit()

def delete_project_with_id(pid):
    curs = conn.cursor()
    curs.execute("delete from PROJECT where ProjectID=%s",(pid,))
    conn.commit()

def view_projects():
    curs = conn.cursor()
    curs.execute("select * from PROJECT")
    rows = curs.fetchall()
    return rows

def pledge_amount(id,amount_pledged):
    curs = conn.cursor()
    curs.execute("select * from PROJECT where ProjectID = %s",(id,))
    project_details = curs.fetchall()
    try:
        remaining_goal = project_details[0][11]
        rem = int(remaining_goal) - int(amount_pledged)
        print(amount_pledged)
        print(rem)
        curs.execute("update PROJECT set Remaining=%s where ProjectID=%s",(rem,id,))
        conn.commit()
        return True
    except:
        pass
        return False

def search_projects_by_title(ptitle):
    curs = conn.cursor()
    curs.execute("select * from PROJECT where ProjectTitle = %s",(ptitle,))
    rows = curs.fetchall()
    return rows

def search_projects_by_username(username):
    curs = conn.cursor()
    curs.execute("select * from PROJECT where UserName = %s",(username,))
    rows = curs.fetchall()
    return rows

def create_reward_table():
    curs = conn.cursor()
    curs.execute("create table if not exists REWARD(RewardID Integer,RewardTitle text,ProjectTitle text,UserName text,PledgedAmount integer,RewardDescription text,ExpectedMonth integer,ExpectedYear integer,ShippingDetails text,RewardLimit integer)")
    conn.commit()

def add_reward(rid,rtitle,ptitle,un,pa,rdesc,expmonth,expyear,shippingDetails,rlimit):
    curs = conn.cursor()
    curs.execute("insert into REWARD values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(rid,rtitle,ptitle,'  ',pa,rdesc,expmonth,expyear,shippingDetails,rlimit))
    conn.commit()

def view_rewards():
    curs = conn.cursor()
    curs.execute("select * from REWARD")
    rows = curs.fetchall()
    return rows

def create_sponsor_table():
    curs = conn.cursor()
    curs.execute("create table if not exists sponsor(SponsorID integer, FirstName text, LastName text,Address text,MobileNumber text,pledgeamount integer,projectTitle text)")
    conn.commit()

def search_reward_by_project(pt):
    curs = conn.cursor()
    curs.execute("select * from REWARD where ProjectTitle=%s",(pt,))
    projects = curs.fetchall()
    return projects

def view_sponsors():
    curs = conn.cursor()
    curs.execute("select * from sponsor")
    sponsors = curs.fetchall()
    return sponsors

def update_sponsor_table(pa,pt):
    curs = conn.cursor()
    curs.execute("update sponsor set pledgeamount = %s where projectTitle = %s",(pa,pt))
    conn.commit()

def add_sponsor(id,fn,ln,address,pa,pt):
    curs = conn.cursor()
    curs.execute("insert into sponsor values(%s,%s,%s,%s,%s,%s)",(id,fn,ln,address,pa,pt,))
    conn.commit()

def search_sponsor(fn,ln):
    curs = conn.cursor()
    curs.execute("select * from sponsor where FirstName = %s and LastName = %s",(fn,ln,))
    details = curs.fetchall()
    return details

def create_personal_info_table():
    curs = conn.cursor()
    curs.execute("create table if not exists PERSONAL_INFO(InfoId integer,UserName text,ProfileImage text,FbUrl text,WebsiteUrl text,Location text,GitUrl text,Biography text)")
    conn.commit()

def add_personal_info(infoid,un,pi,fb,web,loc,git,bio):
    curs = conn.cursor()
    curs.execute("insert into PERSONAL_INFO values(%s,%s,%s,%s,%s,%s,%s,%s)",(infoid,' ',pi,fb,web,loc,git,bio))
    conn.commit()

def view_personal_info():
    curs = conn.cursor()
    curs.execute("select * from PERSONAL_INFO")
    rows = curs.fetchall()
    return rows

def create_bank_account_info_table():
    curs = conn.cursor()
    curs.execute("create table if not exists ACCOUNT(AId integer,UserName text,email text,fn text,ln text,dob text,homeaddress text,routingnumber text,accountnumber text)")
    conn.commit()

def add_bank_account_info(aid,un,email,fn,ln,dob,add,rounum,accnum):
    curs = conn.cursor()
    curs.execute("insert into ACCOUNT values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(aid,' ',email,fn,ln,dob,add,rounum,accnum))
    conn.commit()

def view_bank_account_info():
    curs = conn.cursor()
    curs.execute("select * from ACCOUNT")
    rows = curs.fetchall()
    return rows

def create_project_detailed_info_table():
    curs = conn.cursor()
    curs.execute("create table if not exists PROJECTDETAILS(PDID integer,ProjectTitle text,ProjectVideo text,ProjectDesc text)")
    conn.commit()

def add_project_detailed_info(pdid,pt,pvideo,pdesc):
    curs = conn.cursor()
    curs.execute("insert into PROJECTDETAILS values(%s,%s,%s,%s)",(pdid,pt,pvideo,pdesc))
    conn.commit()

def view_project_detailed_info():
    curs = conn.cursor()
    curs.execute("select * from PROJECTDETAILS")
    rows = curs.fetchall()
    return rows

def search_projects_by_username(un):
    curs = conn.cursor()
    curs.execute("select * from PROJECT where UserName = %s",(un,))
    rows = curs.fetchall()
    return rows

def search_projects_by_id(id):
    curs = conn.cursor()
    curs.execute("select * from PROJECT where ProjectID=%s",(id,))
    rows = curs.fetchall()
    return rows

def get_user_details(un):
    curs = conn.cursor()
    curs.execute("select * from USERS where UserName=%s",(un,))
    rows = curs.fetchall()
    return rows
