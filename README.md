# GroupProject_Cookzilla

1. Implement application code for Cookzilla as a web-based application using solution from part 2
2. Language: Java or Python?
3. Use prepared statements

Allow a user to:
1. **Search for Recipes**: 
  Users should be able to search for recipes that have a particular tag and/or a given number of stars.
  **We need to add dummy data.**
  
2. **Display Recipe Info**: 
  Given a recipeID (possibly selected from a menu based on a search), display relevant information about the recipe, including the description, the steps in order, etc
  
3. **Login**: 
  The user enters her username and password. Cookzilla will add “salt” to the password, hash it, and check whether the hash of the password matches the stored password for that username. If so, it initiates a session, storing the username and any other relevant data in session variables, then goes to the home page (or provides some mechanism for the user to select her next action.) 
  If the password does not match the stored password for that username (or no such user exists), Cookzilla informs the user that the login failed and does not initiate the session. 
   We will supply Python/Flask code for this. If you’re using a different implementation language, you’ll need to write this yourself. After successful login, the user should see their profile, the recipes they’ve posted and the groups they belong to. 
   
   **The remaining use cases require the user to be logged in.**

4. **Post a Recipe**: 
  Post a recipe and related data (steps, tags, etc)

**Extensions**:

1.

2.

3. 

4.

5. 

6.


**Extensions Options**:
- Log users’ actions and display recipes and/or reviews that they viewed recently
- Post a review
- Post an event for a group that user belongs to
- RSVP to an event that the user belongs to
- More complex searches: ingredients, 
- Search for users with similar taste as the given user (e.g. who have given similar ratings to some kinds of recipes)

- Convert the units in a recipe
- The user can set a preferred unit, and everytime they see the recipe ingredients, they should be able to see it in the previously set unit.

If you want to do any other query apart from the ones suggested above, please check-in with us first by **Dec 6**.
