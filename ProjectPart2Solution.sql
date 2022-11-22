DROP TABLE IF EXISTS RecipeIngredient;
DROP TABLE IF EXISTS UnitConversion;
DROP TABLE IF EXISTS Unit;
DROP TABLE IF EXISTS Restrictions;
DROP TABLE IF EXISTS Ingredient;
DROP TABLE IF EXISTS RSVP;
DROP TABLE IF EXISTS EventPicture;
DROP TABLE IF EXISTS Event;
DROP TABLE IF EXISTS GroupMembership;
DROP TABLE IF EXISTS `Group`;
DROP TABLE IF EXISTS Step;
DROP TABLE IF EXISTS RelatedRecipe;
DROP TABLE IF EXISTS ReviewPicture;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS RecipePicture;
DROP TABLE IF EXISTS RecipeTag;
DROP TABLE IF EXISTS Recipe;
DROP TABLE IF EXISTS Person;


CREATE TABLE Person (
    userName VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50),
    fName VARCHAR(50),
    lName VARCHAR(50),
    email VARCHAR(250),
    profile TEXT
);

CREATE TABLE Recipe (
    recipeID INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    numServings INT NOT NULL,
    postedBy VARCHAR(50) NOT NULL,
    FOREIGN KEY (postedBy)
        REFERENCES Person (userName)
);

CREATE TABLE RecipeTag (
    recipeID INT NOT NULL,
    tagText VARCHAR(255) NOT NULL,
    FOREIGN KEY (recipeID)
        REFERENCES Recipe (recipeID),
    PRIMARY KEY (recipeID , tagText)
);

CREATE TABLE RecipePicture (
    recipeID INT NOT NULL,
    pictureURL VARCHAR(255) NOT NULL,
    FOREIGN KEY (recipeID)
        REFERENCES Recipe (recipeID),
    PRIMARY KEY (recipeID , pictureURL)
);

CREATE TABLE Review (
    userName VARCHAR(50),
    recipeID INT NOT NULL,
    revTitle VARCHAR(50),
    revDesc TEXT,
    stars INT,
    PRIMARY KEY (recipeID , userName),
    FOREIGN KEY (userName)
        REFERENCES Person (userName),
    FOREIGN KEY (recipeID)
        REFERENCES Recipe (recipeID)
);

CREATE TABLE ReviewPicture (
    userName VARCHAR(50) NOT NULL,
    recipeID INT NOT NULL,
    pictureURL VARCHAR(255) NOT NULL,
    FOREIGN KEY (userName , recipeID)
        REFERENCES Review (userName , recipeID),
    PRIMARY KEY (userName , recipeID , pictureURL)
);

CREATE TABLE RelatedRecipe (
    recipe1 INT NOT NULL,
    recipe2 INT NOT NULL,
    PRIMARY KEY (recipe1 , recipe2),
    FOREIGN KEY (recipe1)
        REFERENCES Recipe (recipeID),
    FOREIGN KEY (recipe2)
        REFERENCES Recipe (recipeID)
);

CREATE TABLE Step (
    stepNo INT NOT NULL,
    recipeID INT NOT NULL,
    sDesc TEXT NOT NULL,
    PRIMARY KEY (stepNo , recipeID),
    FOREIGN KEY (recipeID)
        REFERENCES Recipe (recipeID)
        ON DELETE CASCADE
);

CREATE TABLE `Group` (
    gName VARCHAR(50) NOT NULL,
    gCreator VARCHAR(50) NOT NULL,
    gDesc TEXT,
    PRIMARY KEY (gName , gCreator),
    FOREIGN KEY (gCreator)
        REFERENCES Person (userName)
        ON DELETE CASCADE
);

CREATE TABLE GroupMembership (
    memberName VARCHAR(50) NOT NULL,
    gName VARCHAR(50) NOT NULL,
    gCreator VARCHAR(50) NOT NULL,
    PRIMARY KEY (memberName , gName , gCreator),
    FOREIGN KEY (memberName)
        REFERENCES Person (userName),
    FOREIGN KEY (gName , gCreator)
        REFERENCES `Group` (gName , gCreator)
);

CREATE TABLE Event (
    eID INT PRIMARY KEY AUTO_INCREMENT,
    eName VARCHAR(255) NOT NULL,
    eDesc TEXT,
    eDate DATETIME NOT NULL,
    gName VARCHAR(50) NOT NULL,
    gCreator VARCHAR(50) NOT NULL,
    FOREIGN KEY (gName , gCreator)
        REFERENCES `Group` (gName , gCreator)
);

CREATE TABLE EventPicture (
    eID INT NOT NULL,
    pictureURL VARCHAR(255) NOT NULL,
    FOREIGN KEY (eID)
        REFERENCES Event (eID),
    PRIMARY KEY (eID , pictureURL)
);

CREATE TABLE RSVP (
    userName VARCHAR(50) NOT NULL,
    eID INT NOT NULL,
    response VARCHAR(1) NOT NULL,
    PRIMARY KEY (userName , eID),
    FOREIGN KEY (userName)
        REFERENCES Person (userName),
    FOREIGN KEY (eID)
        REFERENCES Event (eID)
);

CREATE TABLE Ingredient (
    iName VARCHAR(255) PRIMARY KEY,
    purchaseLink VARCHAR(255)
);

CREATE TABLE Restrictions (
    iName VARCHAR(255) NOT NULL,
    restrictionDesc VARCHAR(255) NOT NULL,
    FOREIGN KEY (iName)
        REFERENCES Ingredient (iName),
    PRIMARY KEY (iName , restrictionDesc)
);

CREATE TABLE Unit (
    unitName VARCHAR(255) PRIMARY KEY
);

CREATE TABLE UnitConversion (
    sourceUnit VARCHAR(255) NOT NULL,
    destinationUnit VARCHAR(255) NOT NULL,
    ratio DECIMAL NOT NULL,
    PRIMARY KEY (sourceUnit , destinationUnit),
    FOREIGN KEY (sourceUnit)
        REFERENCES Unit (unitName),
    FOREIGN KEY (destinationUnit)
        REFERENCES Unit (unitName)
);

CREATE TABLE RecipeIngredient (
    recipeID INT NOT NULL,
    iName VARCHAR(255) NOT NULL,
    unitName VARCHAR(255) NOT NULL,
    amount DECIMAL NOT NULL,
    PRIMARY KEY (recipeID , iName),
    FOREIGN KEY (recipeID)
        REFERENCES Recipe (recipeID),
    FOREIGN KEY (iName)
        REFERENCES Ingredient (iName),
    FOREIGN KEY (unitName)
        REFERENCES Unit (unitName)
);

