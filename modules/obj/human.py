class Human:
	def __init__(
			self,
			firstName: str,
			middleName: str,
			lastName: str,
			chosenName: str,
			email: str,
			ID: int | None = None
	) -> None:
		self.firstName = firstName.capitalize()
		self.middleName = middleName.capitalize()
		self.lastName = lastName.capitalize()
		self.chosenName = chosenName.capitalize()
		self.email = email.lower()
		self.ID = ID

	def printInfo(self):
		msg = {
			"First Name": self.firstName,
			"Middle Name": self.middleName,
			"Last Name": self.lastName,
			"Chosen Name": self.chosenName,
			"Email": self.email,
			"ID": self.ID
		}
		# Remove ID if it is empty
		if (self.ID is None):
			msg.pop("ID")
		# Same for middle name
		if (self.middleName == ""):
			msg.pop("Middle Name")

		# return info for printing/use
		return msg
