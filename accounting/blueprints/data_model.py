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

    @property
    def add_route(self):
        class_name = str(self.__class__)[str(self.__class__).rfind('.') + 1: len(str(self.__class__)) - 2].lower()
        return f"{class_name}.add"

    @property
    def edit_route(self):
        class_name = str(self.__class__)[str(self.__class__).rfind('.') + 1: len(str(self.__class__)) - 2].lower()
        return f"{class_name}.edit"

    @property
    def delete_route(self):
        class_name = str(self.__class__)[str(self.__class__).rfind('.') + 1: len(str(self.__class__)) - 2].lower()
        return f"{class_name}.delete"

    @property
    def export_route(self):
        class_name = str(self.__class__)[str(self.__class__).rfind('.') + 1: len(str(self.__class__)) - 2].lower()
        return f"{class_name}.export"

    @property
    def home_route(self):
        class_name = str(self.__class__)[str(self.__class__).rfind('.') + 1: len(str(self.__class__)) - 2].lower()
        return f"{class_name}.home"

    def fields(self):
        data = self.__table__.columns.keys()
        data.remove("id")
        return data

    @property
    def home_html(self):
        class_name = str(self.__class__)[str(self.__class__).rfind('.') + 1: len(str(self.__class__)) - 2].lower()
        return f"{class_name}/home.html"

    @property
    def add_html(self):
        class_name = str(self.__class__)[str(self.__class__).rfind('.') + 1: len(str(self.__class__)) - 2].lower()
        return f"{class_name}/add.html"

    @property
    def edit_html(self):
        class_name = str(self.__class__)[str(self.__class__).rfind('.') + 1: len(str(self.__class__)) - 2].lower()
        return f"{class_name}/edit.html"
