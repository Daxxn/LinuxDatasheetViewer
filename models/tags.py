from uuid import uuid4 as uid, UUID

class Tag:
   def __init__(self, name: str) -> None:
      self.id: UUID = uid()
      self.name = name

class TagManager:
   def __init__(self) -> None:
      self.tags: list[Tag] = []

   def add(self, name: str):
      if len(self.tags) > 0:
         for tag in self.tags:
            if tag.name == name:
               return tag
      newTag = Tag(name)
      self.tags.append(newTag)
      return newTag

   def remove(self, name: str):
      if len(self.tags) > 0:
         for tag in self.tags:
            if tag.name == name:
               self.tags.remove(tag)
               return True
      return False