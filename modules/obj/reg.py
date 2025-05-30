from datetime import datetime


class Reg:
    def __init__(
            self,
            hID: int | None = None,  # Human ID (Student/Teacher)
            cID: int | None = None,  # Course ID
            ID: int | None = None,  # Registration ID
            regTime: datetime | None = datetime.now()  # Registration Time

    ) -> None:
        self.hID = hID
        self.cID = cID
        self.ID = ID
        self.regTime = regTime

    def storeLookup(self, out):
        self.hID = out.hID
        self.cID = out.cID
        self.ID = out.ID  # This *should* never do anything
        self.regTime = out.regTime
