from accounting import db
import os
import json
from flask import current_app


class DataModel:
    id = db.Column(db.Integer, primary_key=True)

    def data(self, form):
        columns = self.__table__.columns.keys()
        for column in columns:
            if column in ("id", "user_id", "date_modified", "entries"):
                continue
            setattr(self, column, getattr(form, column).data)

    def as_json(self, id=None):
        if id:
            data = [getattr(self, "query").get(id)]
        else:
            data = getattr(self, "query").all()

        data_list = []
        columns = self.__table__.columns.keys()
        for obj in data:
            data_list.append(
                {column: getattr(obj, column) for column in columns}
            )

        return data_list

    def export(self, id=None):
        with current_app.app_context():
            list_files = os.listdir(os.path.join(current_app.instance_path, "temp"))
            for file in list_files:
                os.remove(os.path.join(current_app.instance_path, "temp", file))

            filename = os.path.join(current_app.instance_path, "temp", f"{self.__tablename__}.json")

        with open(filename, "w+") as f:
            json.dump(self.as_json(id), f, indent=4, sort_keys=True, default=str)

        return filename

