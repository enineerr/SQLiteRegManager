from .human import Human


class Student(Human):
    def __init__(self, Obj: Human) -> None:
        super().__init__(
            Obj.firstName,
            Obj.middleName,
            Obj.lastName,
            Obj.chosenName,
            Obj.email,
            Obj.ID
        )
