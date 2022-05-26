from accounting import db


class DataModel:
    id = db.Column(db.Integer, primary_key=True)

    @staticmethod
    def commit():
        db.session.commit()

    def save(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    def save_and_commit(self):
        self.save()
        self.commit()

    def delete_and_commit(self):
        self.delete()
        self.commit()

    def data(self, form):
        columns = self.__table__.columns.keys()
        for column in columns:
            if column == 'id':
                continue
            setattr(self, column, getattr(form, column).data)
