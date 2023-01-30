# GroupProject_Cookzilla
**Group members**: Bharath Sai Reddy Chinthapanti, Doma Ghale and Taha Junaid

1. Implement application code for Cookzilla as a web-based application.
2. Language: Python.
3. Used prepared statements

Allow a user to:
1. Search for Recipes: 

  Users should be able to search for recipes that have a particular tag and/or a given number of stars.
  We implemented that given an input star, we will search for stars strictly greater than the input star.
  
2. Display Recipe Info: **(Doma)**

  Given a recipeID (possibly selected from a menu based on a search), display relevant information about the recipe, including the description, the steps in order, etc.
  We implemented images related to the recipe and review also be displayed. 
  
  
3. Login:

  The user enters her username and password. Cookzilla will add “salt” to the password, hash it, and check whether the hash of the password matches the stored password for that username. If so, it initiates a session, storing the username and any other relevant data in session variables, then goes to the home page. 
   
   *The remaining use cases require the user to be logged in.*


4. Post a Recipe: 

  Post a recipe and related data such as steps and tags.

**Extensions**:

1. Log users’ actions and display recipes and/or reviews that they viewed recently: 

    - Display the 5 most recent viewed recipes. 

2. Post a review:
    - A user cannot post more than one review per recipe, and can post an image with the review.

3. Post an event for a group that user belongs to: **(Doma)**

    - Only members of the group should be able to post an event for that group. 
    - Please specify group name and group creator as multiple groups can have same name with different creator. 

4. RSVP to an event that the user belongs to: **(Doma)**

   - Each event is associated with a group, and only members of the group can RSVP for that event using eID. You can find eID by viewing the group information.  
   - Users can also change their responses by going to RSVP page again. 

5. More complex searches:
    - Users who have given the rating 5 to every Recipe that logged-in user rated 5
    - Recipes with the most popular tags in the last month.
    - Recipes which have not been seen by anyone during the last week.
    - Star User: User who has reviewed every recipe

6. Search for users with similar taste as the given user (e.g. who have given similar ratings to some kinds of recipes):
    - Search for users who gave similar ratings to the logged-in user for recipes with tag, ingredient or receipe name. 

