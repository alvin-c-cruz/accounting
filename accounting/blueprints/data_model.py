from accounting import db
import os
import json
from flask import current_app


class DataModel:
    id = db.Column(db.Integer, primary_key=True)

    @staticmethod
    def commit():
        db.session.commit()

    def save(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    def delete_all(self):
        getattr(self, "query").delete()
        db.session.commit()

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

    def export(self, id=None):
        if id:
            data = [getattr(self, "query").get(id)]
        else:
            data = getattr(self, "query").all()

        data_list = []
        columns = self.__table__.columns.keys()
        for obj in data:
            data_list.append(
                { column: getattr(obj, column) for column in columns }
            )

        with current_app.app_context():
            list_files = os.listdir(os.path.join(current_app.instance_path, "temp"))
            for file in list_files:
                os.remove(os.path.join(current_app.instance_path, "temp", file))

            filename = os.path.join(current_app.instance_path, "temp", f"{self.__tablename__}.json")

        with open(filename, "w+") as f:
            json.dump(data_list, f)

        return filename


