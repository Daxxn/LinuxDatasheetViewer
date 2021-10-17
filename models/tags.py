from uuid import uuid4 as uid, UUID
from models.settings import Settings

#region Tag
class Tag:
   def __init__(self, name: str) -> None:
      self.id: UUID = uid()
      self.name = name
#endregion

#region TagManager
class TagManager:
   #region Init
   def __init__(self, settings: Settings) -> None:
      self.settings = settings
      self.tags: list[Tag] = []
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

   def find(self, name: str):
      if len(self.tags) > 0 and name != '':
         for tag in self.tags:
            if tag.name == name:
               return tag
      return None

   def getTags(self):
      return self.tags

   def serializeTags(self):
      pass

   def findTag(self, text: str):
      for tag in self.tags:
         if tag.name.lower() == text.lower():
            return tag
   #endregion
#endregion