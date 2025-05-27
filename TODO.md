have the database handler make a full backup before opening the database

### student class:
	firstname
	extranames (comma deliminated)
	lastname
	choosenname
	ID
	emergencycontact

### security model:
	main database is locked with a randomly generated password
	admins should each have an encrypted file which is encrypted using a user made password
	the file should contain the encryption key for the database, so multiple admins can login and still access, but dont know the encryption key

### FILTERING/SEARCHING
	ADD ABILIBYT TO SEARCH FOR NAMES
	make main human menu -> search options menu -> which type of name menu -> final func
	make name search not exact by simply using "in" kword

### everything for humans could be refactored to just have a heading instead of individual lines

	Editing Student:
	(1): Edit First name
	(2): Edit First name
	(3): Edit First name
	>>>