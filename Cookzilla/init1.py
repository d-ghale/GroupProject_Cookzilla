#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import bcrypt
import os
import hashlib

#for uploading photo:
from app import app
#from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])




###Initialize the app from Flask
##app = Flask(__name__)
##app.secret_key = "secret key"
# This sets the configuration to connect to your MySQL database
#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port = 3306,
                       user='root',
                       password='',
                       db='Test',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
## Doma's conn below
# conn = pymysql.connect(host='localhost',
#                        port = 8889,
#                        user='root',
#                        password='root',
#                        db='Test',
#                        charset='utf8mb4',
#                        cursorclass=pymysql.cursors.DictCursor)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


#Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Authenticates the login
# This would be in a login.html file, this makes a POST request to /loginAuth

@app.route('/loginAuth', methods=['GET', 'POST'])

# We can send a query to the database by calling the execute method of cursor. 
# Cursor is just an object that is used to interface with the database. 
# If the query is successful, call fetchone() to get a single data row or fetchall() to get multiple rows.
# If the login is successful, it will redirect to the home page

def loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    #adding the salt to the password and hasing
    salt="Fall2022"
    Copassword = password+salt
    hashed_password = hashlib.md5(Copassword.encode()).hexdigest()

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE username = %s and password = %s'
    cursor.execute(query, (username, hashed_password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    # We want to allow the user to be able to post and see their posts on the front page. 
    # We call fetchall() and pass it into the home.html page.
    cursor.close()
    error = None

    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        return redirect(url_for('home'))
    else:
        #returns an error message to the html page
        # passed in an extra argument to render_template: 
        # error = error. Error corresponds to the error that was passed in by the render_template call.
        # Flask uses jinja templating and we can pass variables from flask to the html page using this. 
        # If there was an error message, we passed it in and the message is displayed. {{}} denotes a variable.
        
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    email=request.form['email']
    bio=request.form['bio']
    salt="Fall2022"
    #You don’t want to store your passwords in your database as plain text, you probably want to hash it

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None

    #adding the salt to the password and hasing

    Copassword = password+salt
    hashed_password = hashlib.md5(Copassword.encode()).hexdigest()
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO Person VALUES(%s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, hashed_password,fname,lname,email,bio))
        conn.commit()
        cursor.close()
        return render_template('index.html')

@app.route('/home')
def home():
    if session.get('username')!=None:

        user = session['username']
        
        # cursor = conn.cursor();
        # query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
        # cursor.execute(query, (user))
        # data = cursor.fetchall()
        # # We want to allow the user to be able to post and see their posts on the front page. 
        # # We call fetchall() and pass it into the home.html page.

        # cursor.close()
        return render_template('home.html', username=user)
    else:
        return render_template('login.html')




#adding a new recipe
@app.route('/addrecipe')
def add_recipe():    
        #need to add tags and description in appropriate palces

    if session.get('username')!=None:
        return render_template('add_recipe.html')



    else:
        return render_template('login.html')
#adding a new group
@app.route('/addgroup')
def add_group():    
    #need to create group in Group table and add creater to groupMembership
    if session.get('username')!=None:
        return render_template('add_group.html')
    else:
        return render_template('login.html')
    
#join a group
@app.route('/joingroup')
def join_group():    
    #need to create group in Group table and add creater to groupMembership
    if session.get('username')!=None:
        return render_template('join_group.html')
    else:
        return render_template('login.html')
    
    #adding a new group
@app.route('/addevent')
def add_event():    
    #need to create group in Group table and add creater to groupMembership
    if session.get('username')!=None:
        return render_template('add_event.html')
    else:
        return render_template('login.html')
    
#join a group
@app.route('/joinevent')
def join_event():    
    #need to create group in Group table and add creater to groupMembership
    if session.get('username')!=None:
        return render_template('join_event.html')
    else:
        return render_template('login.html')
    

def insertingi(iname):
    cursor = conn.cursor()
    ins='SELECT COUNT(1) FROM Ingredient WHERE iName=%s'
    cursor.execute(ins, (iname))
    data = cursor.fetchone()
    if data['COUNT(1)']==0:
        ins='INSERT INTO Ingredient(iName) VALUES(%s)'
        cursor.execute(ins, (iname))
        conn.commit()
    
    #print(data['COUNT(1)'])

def insertunit(unit):
    cursor = conn.cursor()
    ins='SELECT COUNT(1) FROM Unit WHERE unitName=%s'
    cursor.execute(ins, (unit))
    data = cursor.fetchone()
    if data['COUNT(1)']==0:
        ins='INSERT INTO Unit(unitName) VALUES(%s)'
        cursor.execute(ins, (unit))
        conn.commit()


@app.route('/addsteps', methods=['GET','POST'])
def addsteps():
    data=request.form
    steps=data.getlist('step')
    ingredients=data.getlist('ingredient')
    print(steps)
    print(ingredients)
    cursor = conn.cursor()
    recipeID=session['recipeID']
    for ingredient in ingredients:
        things=ingredient.split(" ")
        print(things)
        iname=things[0]
        insertingi(iname)
        unit=things[2]
        amount=int(things[1])

        insertunit(unit)
        
        ins='INSERT INTO RecipeIngredient(recipeID,iName,unitName,amount) VALUES(%s,%s,%s,%s)'
        cursor.execute(ins, (recipeID,iname,unit,amount))
        conn.commit()
    print("ingi done")

    # RecipeIngredient

    # Step
    ins='INSERT INTO Step(stepNo,recipeID,sDesc) VALUES (%s,%s,%s)'
    for i,step in enumerate(steps):
        cursor.execute(ins, (i,recipeID,step))
        conn.commit()

    print("step done")

    

    return render_template('home.html',username=session['username'])


@app.route('/addrecipeprocess', methods=['GET','POST'])
def add_recipe_process():
    if session.get('username')!=None:
        username = session['username']
        recipetitle = request.form['recipetitle']
        num_servings = request.form['num_servings']
        num_steps = request.form['num_steps']
        num_ingredients = request.form['num_ingredients']

        tags = request.form['tags']
        tagslist=tags.split(",")
        cursor = conn.cursor()

        #Creating the Recipe in Recipe Table
        ins = 'INSERT INTO Recipe(title,numServings,postedBy) VALUES(%s, %s, %s)'
        cursor.execute(ins, (recipetitle,num_servings,username))
        #conn.commit()

        


        #Fetching the recipe ID
        ins='SELECT recipeID FROM Recipe WHERE title=%s AND postedBy=%s'
        cursor.execute(ins,(recipetitle,username))

        data = cursor.fetchone()
        print(data)
        recipeID=data["recipeID"]
        session['recipeID'] = recipeID
        #Creating Tags for the Recipe in 

        #RecipeTag
        ins='INSERT INTO RecipeTag(recipeID,tagText) VALUES(%s,%s)'
        for tag in tagslist:
            cursor.execute(ins, (recipeID,tag))
            #conn.commit()


        #Taking care of image

        file = request.files['file']
        filename = secure_filename(file.filename)
        print(filename)
        if filename=="":
            return render_template('add_steps.html',recipename=recipetitle,nsteps=int(num_steps),nings=int(num_ingredients))
        else:

            
            
            ext=filename.split(".")[1]
            filename=str(recipeID)+"."+ext
            file.save(os.path.join(app.config['UPLOAD_FOLDER_RECIPE'], filename))
            q='INSERT INTO RecipePicture(recipeID,pictureURL) VALUES(%s,%s)'
            cursor.execute(q,(recipeID,os.path.join(app.config['UPLOAD_FOLDER_RECIPE'], filename)))
            conn.commit()

        
        return render_template('add_steps.html',recipename=recipetitle,nsteps=int(num_steps),nings=int(num_ingredients))
    else:

        return render_template('login.html')

@app.route('/addgroupprocess', methods=['GET','POST'])
def add_group_process():
    if session.get('username')!=None:
        username = session['username']
        group_name = request.form['group_name']
        group_description = request.form['group_description']
        cursor = conn.cursor()
        #Display message saying group already exists if same creator and same Group name
        ins_check='SELECT * FROM `Group` WHERE gName=%s AND gCreator=%s'
        cursor.execute(ins_check,(group_name, username))
        GroupExist = cursor.fetchone()
        print(GroupExist)
        if GroupExist == None:
            ins='INSERT INTO `Group`(gName, gCreator, gDesc) VALUES(%s,%s,%s)'
            cursor.execute(ins,(group_name,username,group_description))
            q='INSERT INTO GroupMembership( memberName, gName, gCreator) VALUES(%s,%s,%s)'
            cursor.execute(q,(username,group_name,username))
            message_join = "New group created!!!"
            conn.commit()
            return render_template('viewonegroup.html', GCreator = username, GroupName = group_name, GroupDescription=group_description,message_join=message_join)
        else:
            message_join = "You previously created a group with same name, so cannot recreate!!!"
            return render_template('home.html', message_join=message_join)
    else:
        return render_template('login.html')

@app.route('/joingroupprocess', methods=['GET','POST'])
def join_group_process():
    if session.get('username')!=None:
        username = session['username']
        group_name = request.form['group_name']
        group_creator = request.form['group_creator']
        cursor = conn.cursor()
        #Check if such a group exists
        ins_check='SELECT * FROM `Group` WHERE gName=%s AND gCreator=%s'
        cursor.execute(ins_check,(group_name, group_creator))
        GroupExist = cursor.fetchone()
        print(GroupExist)
        if GroupExist == None:
            message_join = f"Please create the group {group_name} first as it doesn't"
            return render_template('home.html', message_join=message_join)
        else: 
            #Check if already part of the group
            ins='SELECT * FROM GroupMembership WHERE gName=%s AND gCreator=%s AND memberName=%s'
            cursor.execute(ins,(group_name, group_creator, username))
            data = cursor.fetchone()
            print(data)
            if data == None:
                q='INSERT INTO GroupMembership(memberName, gName, gCreator) VALUES(%s,%s,%s)'
                cursor.execute(q,(username,group_name,group_creator))
                message_join = "You are now added to the group"
            else:
                message_join = "You were already part of the group"
            #Fetching the info
            ins1='SELECT * FROM `GROUP` WHERE gName=%s AND gCreator=%s'
            cursor.execute(ins1,(group_name, group_creator))
            data = cursor.fetchone()
            print(data)
            group_description=data["gDesc"]
            conn.commit()
            return render_template('viewonegroup.html', GCreator=group_creator, GroupName=group_name, GroupDescription=group_description, message_join=message_join)
    else:
        return render_template('login.html')

import datetime

@app.route('/addeventprocess', methods=['GET','POST'])
def add_event_process():
    if session.get('username')!=None:
        username = session['username']
        event_name = request.form['event_name']
        event_description = request.form['event_description']
        event_date = request.form['event_date']
        event_time = request.form['event_time']
        group_name = request.form['group_name']
        group_creator = request.form['group_creator']
        event_datetime = datetime.datetime.strptime(event_date + " " + event_time, "%Y-%m-%d %H:%M")
        print(event_description)
        cursor = conn.cursor()
        # User has to be part of the group to create an event  
        ins_check='SELECT * FROM GroupMembership WHERE gName=%s AND gCreator=%s AND memberName=%s'
        cursor.execute(ins_check,(group_name, group_creator, username))
        data = cursor.fetchone()
        print(data)
        if data == None:
            message_join = "Sorry you cannot create an event for a group you are not a member of!!!"
            return render_template('home.html', message_join=message_join)
        else:
            print("------")
            q='INSERT INTO Event(eName, eDesc, eDate, gName, gCreator) VALUES(%s,%s,%s,%s,%s)'
            cursor.execute(q,(event_name,event_description,event_datetime, group_name,group_creator))
            message_join = "New event created!!!"

            ## We need to somehow maybe?? grab eID to make that the next part run for this function
            #Fetching the info
            ins1='SELECT * FROM Event WHERE eName=%s AND eDesc=%s AND  eDate=%s AND gName=%s AND gCreator=%s'
            cursor.execute(ins1,(event_name,event_description,event_datetime, group_name,group_creator))
            Eventdata = cursor.fetchall()
            print(Eventdata)

            conn.commit()
            # return render_template('viewoneevent.html', message_join=message_join)
            return render_template('viewoneevent.html', Eventdata=Eventdata, message_join=message_join)
    else:
        return render_template('login.html')

@app.route('/joineventprocess', methods=['GET','POST'])
def join_event_process():
    if session.get('username')!=None:
        username = session['username']
        event_ID = request.form['event_ID']
        event_response = request.form['event_response']
        cursor = conn.cursor()
        
        #Check if event exists
        E_check='SELECT * FROM GroupMembership JOIN Event WHERE eID=%s'
        cursor.execute(E_check,(event_ID))
        E_check_data = cursor.fetchone()
        print(E_check_data)
        if E_check_data == None:
            message_join = "Sorry this event doesn't exist"
            return render_template('viewoneevent.html', message_join=message_join)
        #Check if already part of the group, needs fix!  
        Member_check='SELECT * FROM GroupMembership JOIN Event WHERE eID=%s AND memberName=%s'
        cursor.execute(Member_check,(event_ID, username))
        Member_check_data = cursor.fetchone()
        print(Member_check_data)
        if Member_check_data == None:
            message_join = "Sorry this event is restricted to members only"
            return render_template('viewoneevent.html', message_join=message_join)
        else:
            #check if already RSVPed
            ins_checkRSVP = 'SELECT * FROM RSVP WHERE eID=%s AND userName=%s'
            cursor.execute(ins_checkRSVP,(event_ID, username))
            RSVP_history = cursor.fetchone()
            print(RSVP_history)
            if RSVP_history == None:
                ins='INSERT INTO RSVP(userName, eID, response) VALUES(%s,%s,%s)'
                cursor.execute(ins,(username,event_ID,event_response))
                message_join = "Your response to the event is " + event_response
            else:
                #Update with new respose if already RSVPed
                ins_updateRSVP = 'UPDATE RSVP SET response=%s WHERE eID=%s AND userName=%s'
                cursor.execute(ins_updateRSVP,(event_response,event_ID,username))
                message_join = "Your response to the event is updated as " + event_response
            #Fetching the info
            ins1='SELECT * FROM EVENT WHERE eID=%s'
            cursor.execute(ins1,(event_ID))
            Eventdata = cursor.fetchone()
            print(Eventdata)
            conn.commit()
            return render_template('viewoneevent.html', Eventdata=Eventdata, message_join=message_join)
    else:
        return render_template('login.html')

# def viewrecipes():
#     cursor = conn.cursor()
#     ins='SELECT * FROM Recipe'
#     cursor.execute(ins)
#     data = cursor.fetchall()
#     print(len(data))
#     return render_template('viewrecipe.html',data=data,len=len(data))

@app.route('/addreview', methods=['GET','POST'])
def addreview():
    if session.get('username')!=None:
        print(request.args)
        recipeID= request.args['r']
        return render_template('addreview.html',recipeID=recipeID)
    else:
        return render_template('login.html')


@app.route('/publishreview', methods=['GET','POST'])
def publishreview():
    if session.get('username')!=None:
        username = session['username']
        recipeID= request.args['r']
        cursor = conn.cursor()

        print(request.args)
        qs="SELECT userName from Review WHERE recipeID=%s"
        cursor.execute(qs,(recipeID))
        data = cursor.fetchall()
        if len(data)!=0:
            flash("You can only post once")  
            return render_template('error.html',username=username)

        else:
            print(data,len(data))
            reviewtitle = request.form.get('reviewtitle')
            reviewstars = request.form.get('reviewstars')
            description = request.form.get('description')
            
            file = request.files['file']
            filename = secure_filename(file.filename)
            ins='INSERT INTO Review(userName,recipeID,revTitle,revDesc,stars) VALUES (%s,%s,%s,%s,%s)'
            cursor.execute(ins,(username,recipeID,reviewtitle,description,reviewstars))

            if filename =="":
                conn.commit()
            else:

                ext=filename.split(".")[1]
                filename=recipeID+"_"+username+"."+ext
                file.save(os.path.join(app.config['UPLOAD_FOLDER_REVIEW'], filename))
                
                q='INSERT INTO ReviewPicture(userName,recipeID,pictureURL) VALUES(%s,%s,%s)'
                cursor.execute(q,(username,recipeID,os.path.join(app.config['UPLOAD_FOLDER_REVIEW'], filename)))
            conn.commit()
        


            return render_template('home.html',username=username)
    else:
        return render_template('login.html')




@app.route('/viewonerecipe', methods=['GET','POST'])
def viewonerecipe():
    # recipeID=request.form['recipeID']
    recipeID= request.args['r']
    cursor = conn.cursor()
    ins='SELECT * FROM Recipe WHERE recipeID=%s'
    cursor.execute(ins,(recipeID))
    Recipedata = cursor.fetchall()
    ins='SELECT * FROM RecipeIngredient WHERE recipeID=%s'
    cursor.execute(ins,(recipeID))
    RecipeIngredientdata = cursor.fetchall()
    # RecipeIngredientStr = ' '.join([' '.join([RecipeIngredientdata[i]['amount'], RecipeIngredientdata[i]['unitName'], RecipeIngredientdata[i]['iName']])  for i in range(len(RecipeIngredientdata))])
    RecipeIngredientList = [] 
    for i in range(len(RecipeIngredientdata)):
        RecipeIngredientList.append(" ".join([str(RecipeIngredientdata[i]['amount']), RecipeIngredientdata[i]['unitName'], RecipeIngredientdata[i]['iName']]))
    if len(RecipeIngredientList) > 0 :
        RecipeIngredientStr = ', '.join(RecipeIngredientList)
    else:
        RecipeIngredientStr = 'No ingredients provided'
    ins='SELECT * FROM Step WHERE recipeID=%s'
    cursor.execute(ins,(recipeID))
    Stepdata = cursor.fetchall()
    StepList = []
    for i in range(len(Stepdata)):
        # in database steps starts at 0, so added 1
        StepList.append(". ".join([str(Stepdata[i]['stepNo'] + 1), Stepdata[i]['sDesc']]))
    if len(StepList) > 0 :
        StepStr = '\n'.join(StepList)
    else:
        StepStr = 'No steps provided'
    ins='SELECT tagText FROM RecipeTag WHERE recipeID=%s'
    cursor.execute(ins,(recipeID))
    Tagdata = cursor.fetchall()
    TagList = [Tagdata[i]['tagText'] for i in range(len(Tagdata))]
    if len(TagList) > 0:
        TagStr = ', '.join(TagList)
    else:
        TagStr = 'None provided'
    ins='SELECT * FROM Review WHERE recipeID=%s'
    cursor.execute(ins,(recipeID))
    ReviewData = cursor.fetchall()
    if ReviewData == None :
        NumReviews = 0
    else:
        NumReviews = len(ReviewData)
    ins='SELECT pictureURL FROM RecipePicture WHERE recipeID=%s'
    cursor.execute(ins,(recipeID))
    RecipePicturedata = cursor.fetchall()
    ins='SELECT pictureURL FROM ReviewPicture WHERE recipeID=%s'
    cursor.execute(ins,(recipeID))
    ReviewPicturedata = cursor.fetchall()
    
    if (len(RecipePicturedata) > 0) and (len(ReviewPicturedata) > 0):
        RecipePictureURL = "../" +RecipePicturedata[0]['pictureURL']
        ReviewPictureURL = "../" +ReviewPicturedata[0]['pictureURL']
        print(RecipePictureURL)
        print(RecipePictureURL)
        return render_template('viewonerecipe.html', NumReview=NumReviews, Recipedata=Recipedata,RecipeIngredientdata=RecipeIngredientStr,Stepdata=StepStr,Tagdata=TagStr,recipeID=recipeID,ReviewData=ReviewData,RecipePictureURL=RecipePictureURL, ReviewPictureURL = ReviewPictureURL)
    elif len(RecipePicturedata) > 0:
        RecipePictureURL = "../" +RecipePicturedata[0]['pictureURL']
        print(RecipePictureURL)
        return render_template('viewonerecipe.html', NumReview=NumReviews, Recipedata=Recipedata,RecipeIngredientdata=RecipeIngredientStr,Stepdata=StepStr,Tagdata=TagStr,recipeID=recipeID,ReviewData=ReviewData,RecipePictureURL=RecipePictureURL)
    elif len(RecipePicturedata) > 0:
        ReviewPictureURL = "../" +ReviewPicturedata[0]['pictureURL']
        print(RecipePictureURL)
        return render_template('viewonerecipe.html', NumReview=NumReviews, Recipedata=Recipedata,RecipeIngredientdata=RecipeIngredientStr,Stepdata=StepStr,Tagdata=TagStr,recipeID=recipeID,ReviewData=ReviewData,ReviewPictureURL=ReviewPictureURL)
    else: 
        return render_template('viewonerecipe.html', NumReview=NumReviews, Recipedata=Recipedata,RecipeIngredientdata=RecipeIngredientStr,Stepdata=StepStr,Tagdata=TagStr,recipeID=recipeID,ReviewData=ReviewData)

@app.route('/viewrecipes')
@app.route('/explore', methods=['GET','POST'])
def exploreRecipes():
    keysDict=dict(request.form)
    errorMsg=""
    if keysDict.keys() >= {'tags'} and len(keysDict['tags'])==0:
        del keysDict['tags']
    if keysDict.keys() >= {'stars'} and len(keysDict['stars'])==0:
        del keysDict['stars']
    if 'rName' in keysDict.keys():
        cursor = conn.cursor()
        recipeName=keysDict['rName']
        ins='SELECT * FROM Recipe WHERE title like %s'
        args=['%'+recipeName+'%']
        cursor.execute(ins,args)
    elif keysDict.keys() == {'tags','tagOperation','stars','tagAndStarOperation'}:
        cursor = conn.cursor()
        tags=keysDict['tags']
        tagsList=tags.split(',')
        tagListLen=len(tagsList)
        tagOp=keysDict['tagOperation']
        stars=keysDict['stars']
        tagAndStarOp=keysDict['tagAndStarOperation']
        args=[]
        print(tags+stars+tagOp+tagAndStarOp)
        if(tagOp=='AND' and tagAndStarOp=='AND'):
            ins='SELECT * from Recipe where recipeID IN ((SELECT Recipe.recipeID FROM Recipe JOIN recipetag ON Recipe.recipeID=recipetag.recipeID where tagText IN %s GROUP BY recipetag.recipeID HAVING COUNT(*)=%s) INTERSECT (SELECT recipeID from review where stars > %s))'
            args=[tagsList,str(tagListLen),stars]
        elif(tagOp=='AND' and tagAndStarOp=='OR'):
            ins='SELECT * from Recipe where recipeID IN ((SELECT Recipe.recipeID FROM Recipe JOIN recipetag ON Recipe.recipeID=recipetag.recipeID where tagText IN %s GROUP BY recipetag.recipeID HAVING COUNT(*)=%s) UNION (SELECT recipeID from review where stars > %s))'
            args=[tagsList,str(tagListLen),stars]
        elif(tagOp=='OR' and tagAndStarOp=='AND'):
            ins='SELECT * from Recipe where recipeID IN ((SELECT Recipe.recipeID FROM Recipe JOIN recipetag ON Recipe.recipeID=recipetag.recipeID where tagText IN %s) INTERSECT (SELECT recipeID from review where stars > %s))'
            args=[tagsList,stars]
        elif(tagOp=='OR' and tagAndStarOp=='OR'):
            ins='SELECT * from Recipe where recipeID IN ((SELECT Recipe.recipeID FROM Recipe JOIN recipetag ON Recipe.recipeID=recipetag.recipeID where tagText IN %s) UNION (SELECT recipeID from review where stars > %s))'
            args=[tagsList,stars]
        cursor.execute(ins,args)
    elif keysDict.keys() == {'tags','tagOperation'}:
        cursor = conn.cursor()
        tags=keysDict['tags']
        tagsList=tags.split(',')
        tagListLen=len(tagsList)
        tagOp=keysDict['tagOperation']
        if(tagOp=='AND'):
            ins='SELECT * FROM Recipe JOIN recipetag ON Recipe.recipeID=recipetag.recipeID where tagText IN %s GROUP BY recipetag.recipeID HAVING COUNT(*)=%s'
        if(tagOp=='OR'):
            ins='SELECT * FROM Recipe JOIN recipetag ON Recipe.recipeID=recipetag.recipeID where tagText IN %s'
        args=[tagsList,str(tagListLen)]
        cursor.execute(ins,args)
    elif keysDict.keys() == {'stars'}:
        cursor = conn.cursor()
        stars=keysDict['stars']
        ins='SELECT * FROM Recipe NATURAL JOIN recipetag NATURAL JOIN review where stars >%s GROUP BY recipeId'
        args=[stars]
        cursor.execute(ins,args)
    elif keysDict.keys() >= {'tags'} and not(keysDict.keys() >= {'tagOperation'}):
        if keysDict.keys() >= {'stars'}:
            if not(keysDict.keys() >= {'tagAndStarOperation'}):
                errorMsg="a tag operation choice must be selected if tags are provided and a starAndtag combining operation choice must be selected if stars and tags are provided."
            else:
                errorMsg="a tag operation choice must be selected if tags are provided." 
        else:
            errorMsg="a tag operation choice must be selected if tags are provided."
    elif (keysDict.keys() >= {'tagOperation'} and not(keysDict.keys() >= {'tags'})) or (keysDict.keys() >= {'tagAndStarOperation'} and not(keysDict.keys() >= {'stars'})and not(keysDict.keys() >= {'tags'})):
        if(keysDict.keys() >= {'tagOperation'} and not(keysDict.keys() >= {'tags'})) and (keysDict.keys() >= {'tagAndStarOperation'} and not(keysDict.keys() >= {'stars'}) and not(keysDict.keys() >= {'tags'})):
            errorMsg="tags and stars must be provided if their tag operation and and tag and star combining operations are selected"
        elif (keysDict.keys() >= {'tagOperation'} and not(keysDict.keys() >= {'tags'})):
            errorMsg="tags must be provided if a tag operation is selected"
        elif(keysDict.keys() >= {'tagAndStarOperation'} and not(keysDict.keys() >= {'stars'}) and not(keysDict.keys() >= {'tags'})):
            errorMsg="tags and stars must be provided if a tag And Star combining Operation is selected"
    else:
        print("No rName found, returning all recipes")
        cursor = conn.cursor()
        ins='SELECT * FROM Recipe'
        cursor.execute(ins)
    if(errorMsg!=""):
        return render_template('explore.html',errorMsg=errorMsg)
    data = cursor.fetchall()
    numRows=len(data)
    if(numRows>0):
        return render_template('explore.html',data=data,len=numRows)
    else:
        errorMsg="No recipe found for your search criteria."
        return render_template('explore.html',errorMsg=errorMsg)

@app.route('/findusers', methods=['GET','POST'])
def findUsers():
    keysDict=dict(request.form)
    print(keysDict)
    errorMsg="PAGE NOT IMPLEMENTED"
    return render_template('explore.html',errorMsg=errorMsg)

@app.route('/exploregroup')
def exploregroup():
    cursor = conn.cursor()
    ins='SELECT * FROM `Group`'
    cursor.execute(ins)
    data = cursor.fetchall()
    return render_template('explore_group.html',data=data,len=len(data))

import pandas as pd
import numpy as np

@app.route('/exploreonegroup', methods=['GET','POST'])
def exploreonegroup():
    if session.get('username')!=None:
        username = session['username']
        cursor = conn.cursor()
        group_creator=request.args['r']
        group_name= request.args['name']
        
        ins='SELECT * FROM `Group` WHERE gName=%s AND gCreator=%s'
        cursor.execute(ins,(group_name, group_creator))
        Gdata = cursor.fetchall()
        message_join = "Viewing group"
        group_description = Gdata[0]['gDesc']
        #SHOW group members 
        ins2='SELECT * FROM GroupMembership WHERE gName=%s AND gCreator=%s AND memberName!=%s'
        cursor.execute(ins2,(group_name, group_creator, group_creator))
        Mdata = cursor.fetchall()
        members = ", ".join([Mdata[i]["memberName"] for i in range(len(Mdata))])
        #SHOW events related to the group when No RSVP
        checkEvent='SELECT * FROM Event WHERE gName=%s AND gCreator=%s'
        cursor.execute(checkEvent,(group_name, group_creator))
        Eventdata = cursor.fetchall()

        checkRSVP='SELECT * FROM Event LEFT JOIN RSVP ON Event.eID=RSVP.eID WHERE gName=%s AND gCreator=%s'
        cursor.execute(checkRSVP,(group_name, group_creator))
        RSVPdata = cursor.fetchall()
        print(RSVPdata)
        if len(Eventdata) == 0:
            return render_template('viewonegroup.html', GCreator=group_creator, GroupName=group_name, GroupDescription=group_description,message_join=message_join,members=members)
        else:
            if len(RSVPdata) == 0:
                Eventdf = pd.DataFrame(Eventdata)
                Eventdf["userResponse"] = ""
            else:
                del Eventdata
                Eventdf = pd.DataFrame(RSVPdata)
                print(Eventdf.columns)
                print(Eventdf)
                Eventdf.loc[(Eventdf["response"] == "0"), "response"] = "Not going"
                Eventdf.loc[(Eventdf["response"] == "1"), "response"] = "Going"
                Eventdf.loc[(Eventdf["response"] == "2"), "response"] = "Maybe going"
                Eventdf["response"] = Eventdf["response"].fillna("No Response")
                Eventdf["userResponse"] = Eventdf["userName"]+" "+Eventdf["response"]
                Eventdf["userResponse"] = Eventdf["userResponse"].fillna("No Response")
                Eventdf.drop(columns=["gName","gCreator","userName","response","RSVP.eID"], inplace=True)
                Eventdf['eDate'] = Eventdf['eDate'].dt.strftime('%Y/%d/%m %H:%m')
                print(Eventdf)
            Eventdf2 = pd.DataFrame(Eventdf.groupby(['eID', 'eName', 'eDesc', 'eDate']).agg(tuple).applymap(', '.join).reset_index()).T.to_dict()
            print(Eventdf2)
            return render_template('viewonegroup.html', GCreator=group_creator, GroupName=group_name, GroupDescription=group_description,message_join=message_join,members=members,Eventdf2=Eventdf2)

@app.route('/logout')
# To log out of the application, simply pop ‘username’ from the session store.
# Note that if the user presses the back button on the browser or manually types in
# a path that requires the user to be logged in, bad things will happen. In all the routes
# add a check to see if ‘username’ is in session before doing any other operations.

def logout():
    session.pop('username')
    return redirect('/')
        
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
