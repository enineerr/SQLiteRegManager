from modules.obj.reg import Reg
from datetime import datetime


class sReg(Reg):
    def __init__(self, Obj: Reg) -> None:
        super().__init__(Obj.hID, Obj.cID, Obj.ID, Obj.regTime)

    def saveValues(self) -> dict[str, int | None | datetime]:
        return {
            "StudentID": self.hID,
            "CourseID": self.cID,
            "RegistrationTime": self.regTime
        }
