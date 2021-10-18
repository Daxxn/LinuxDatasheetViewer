from uuid import uuid4 as uid, UUID
from models.settings import Settings

#region Tag
class Tag:
   def __init__(self, name: str) -> None:
      self.id: UUID = uid()
      self.name = name

   def serialize(self):
      return self.id.hex

   @staticmethod
   def deserialize(data):
      id = UUID(hex=data['id'])
      tag = Tag(data['name'])
      tag.id = id
      return tag
#endregion

#region TagManager
class TagManager:
   #region Init
   def __init__(self, settings: Settings, tags: list[Tag] = None) -> None:
      self.settings = settings
      self.tags = tags if tags != None else []
   #endregion

   #region Methods
   def add(self, name: str):
      if len(self.tags) > 0:
         for tag in self.tags:
            if tag.name == name:
               return tag
      newTag = Tag(name)
      self.tags.append(newTag)
      return newTag

   def remove(self, tag: Tag):
      if len(self.tags) > 0:
         self.tags.remove(tag)
         return True
      return False

   def find(self, name: str, caseSens: bool = False):
      if len(self.tags) > 0 and name != '':
         if caseSens:
            for tag in self.tags:
               if tag.name == name:
                  return tag
         else:
            for tag in self.tags:
               if tag.name.lower() == name.lower():
                  return tag
      return None

   def filter(self, text: str):
      if text != '':
         if len(self.tags):
            output: list[Tag] = []
            for t in self.tags:
               if t.name.__contains__(text):
                  output.append(t)
            return output
      return None


   def getTags(self):
      return self.tags

   def getTagNames(self):
      output = []
      for t in self.tags:
         output.append(t.name)

   def findTag(self, text: str):
      for tag in self.tags:
         if tag.name.lower() == text.lower():
            return tag

   def serializeAll(self):
      output = []
      for t in self.tags:
         temp = {}
         temp['id'] = t.id.hex
         temp['name'] = t.name
         output.append(temp)
      return output

   @staticmethod
   def deserializeAll(tags: list):
      output = []
      if len(tags) > 0:
         for t in tags:
            output.append(Tag.deserialize(t))
      return output

   @staticmethod
   def load(id: str, name: str):
      tempTag = Tag(name)
      tempTag.id = UUID(hex=id)

   @staticmethod
   def serialize(tags: list):
      output = []
      for t in tags:
         output.append(t.serialize())
      return output

   def deserialize(self, tags: list[str]):
      output = []
      if len(self.tags) > 0:
         for id in tags:
            for tag in self.tags:
               if tag.id.hex == id:
                  output.append(tag)
                  break
      return output
   #endregion
#endregion