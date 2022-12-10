#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import bcrypt

import hashlib

#for uploading photo:
from app import app
#from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


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
        conn.commit()

        


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
            conn.commit()

        
        return render_template('add_steps.html',recipename=recipetitle,nsteps=int(num_steps),nings=int(num_ingredients))
    else:

        return render_template('login.html')


@app.route('/viewrecipes')
def viewrecipes():
    cursor = conn.cursor()
    ins='SELECT * FROM Recipe'
    cursor.execute(ins)
    data = cursor.fetchall()
    print(len(data))
    return render_template('viewrecipe.html',data=data,len=len(data))



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
        print(request.args)
        reviewtitle = request.form['reviewtitle']
        reviewstars = request.form['reviewstars']
        description = request.form['description']
        cursor = conn.cursor()
        ins='INSERT INTO Review(userName,recipeID,revTitle,revDesc,stars) VALUES (%s,%s,%s,%s,%s)'
        cursor.execute(ins,(username,recipeID,reviewtitle,description,int(reviewstars)))
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
    ins='SELECT * FROM Step WHERE recipeID=%s'
    cursor.execute(ins,(recipeID))
    Stepdata = cursor.fetchall()
    ins='SELECT * FROM RecipeTag WHERE recipeID=%s'
    cursor.execute(ins,(recipeID))
    Tagdata = cursor.fetchall()
    ins='SELECT * FROM Review WHERE recipeID=%s'
    cursor.execute(ins,(recipeID))
    ReviewData = cursor.fetchall()


    return render_template('viewonerecipe.html',Recipedata=Recipedata,RecipeIngredientdata=RecipeIngredientdata,Stepdata=Stepdata,Tagdata=Tagdata,recipeID=recipeID,ReviewData=ReviewData)

@app.route('/explore', methods=['GET','POST'])
def exploreRecipes():
    if 'rName' in request.form.keys():
        cursor = conn.cursor()
        recipeName=request.form['rName']
        ins='SELECT * FROM Recipe WHERE title like %s'
        args=['%'+recipeName+'%']
        cursor.execute(ins,args)
    elif 'tags' in request.form.keys():
        cursor = conn.cursor()
        tags=request.form['tags']
        tagsList=tags.split(',')
        stars=request.form['stars']
        tagOp=request.form['tagOperation']
        tagAndStarOp=request.form['tagAndStarOperation']
        print(tags+stars+tagOp+tagAndStarOp)
        ins='SELECT * FROM Recipe JOIN recipetag ON Recipe.recipeID=recipetag.recipeID where tagText IN %s'
        args=[tagsList]
        cursor.execute(ins,args)
    else:
        print("No rName found, returning all recipes")
        cursor = conn.cursor()
        ins='SELECT * FROM Recipe'
        cursor.execute(ins)
    data = cursor.fetchall()
    print(len(data))
    return render_template('explore.html',data=data,len=len(data))


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
