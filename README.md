# GroupProject_Cookzilla

1. Implement application code for Cookzilla as a web-based application.
2. Language: Python.
3. Used prepared statements

Allow a user to:
1. **Search for Recipes**: 

  Users should be able to search for recipes that have a particular tag and/or a given number of stars.
  
2. **Display Recipe Info**: 


  Given a recipeID (possibly selected from a menu based on a search), display relevant information about the recipe, including the description, the steps in order, etc
  
  
3. **Login**:


  The user enters her username and password. Cookzilla will add “salt” to the password, hash it, and check whether the hash of the password matches the stored password for that username. If so, it initiates a session, storing the username and any other relevant data in session variables, then goes to the home page. 
   
   **The remaining use cases require the user to be logged in.**


4. **Post a Recipe**: 


  Post a recipe and related data (steps, tags, etc)

**Extensions**:

1. Log users’ actions and display recipes and/or reviews that they viewed recently: 

2. Post a review: 

3. Post an event for a group that user belongs to: 

4. RSVP to an event that the user belongs to:

5. More complex searches:
    - Users who have given the rating 5 to every Recipe that logged-in user rated 5
    - Recipes with the most popular tags in the last month.
    - Recipes which have not been seen by anyone during the last week.
    - Star User: User who has reviewed every recipe

6. Search for users with similar taste as the given user (e.g. who have given similar ratings to some kinds of recipes):


