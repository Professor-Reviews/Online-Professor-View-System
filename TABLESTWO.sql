-- tables
-- Table: Administrator
CREATE TABLE Administrator (
    fName char(50)  NOT NULL,
    lName char(50)  NOT NULL,
    adminEmail VARCHAR(100)  NOT NULL,
  
    CONSTRAINT Administrator_pk PRIMARY KEY (adminEmail)
);

-- Table: Feedback
CREATE TABLE Feedback (
	profName CHAR(45) NOT NULL,
    university CHAR(45)	NOT NULL,
    rating INT NOT NULL CHECK(rating >= 0 AND rating <= 5),
    input VARCHAR(500)  NOT NULL,
    reviewID INT AUTO_INCREMENT NOT NULL,
	
    CONSTRAINT Feedback_pk PRIMARY KEY (reviewID)
);
-- Table: Student
CREATE TABLE Student  (
  	fName char(50) NOT NULL,
  	lName char(50) NOT NULL,
  	studentEmail varchar(100) NOT NULL,
    password varchar(100) NOT NULL,
	CONSTRAINT studentEmail_pk  PRIMARY KEY (studentEmail)	
);
-- Table: Professor 
CREATE TABLE Professor (
	fName char NOT NULL,
    lName char NOT NULL,
    profEmail char NOT NULL,
    password varchar(100) NOT NULL,
    CONSTRAINT profEmail_pk PRIMARY KEY (profEmail)
);
    
-- End of file.

