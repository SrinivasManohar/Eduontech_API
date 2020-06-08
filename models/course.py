from dataclasses import dataclass, field
import uuid
import re
from typing import Dict
from models.model import Model



@dataclass(eq=False)
class Course(Model):
    collection: str = field(init=False, default="courses")
    name: str
    url_prefix: str
    tag_name: str
    query: Dict
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_name(cls, course_name: str) -> "Course":
        return cls.find_one_by("name", course_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Course":
        url_regex = {"$regex": '^{}'.format(url_prefix)}
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url: str) -> "Course":
        """
        Return a store from a url like "http://www.edureka.com"
        :param url: The item's URL
        :return: a Course
        """
        pattern = re.compile(r"(https?:\/\/.*?\/)")
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)
