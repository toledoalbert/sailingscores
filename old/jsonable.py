import json

class jsonable:
   'This is a parent class for all classes that I want to serialize in json'

   def __init__(self):
    self = self

   def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)