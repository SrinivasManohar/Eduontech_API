from dataclasses import dataclass, field
from typing import Dict
import uuid
from models.subject import Subject
from models.model import Model
from libs.mailgun import Mailgun
from models.user import User


@dataclass(eq=False)
class Alert(Model):
    collection: str = field(init=False, default="alerts")
    name: str
    subject_id: str
    price_limit: str
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.subject = Subject.get_by_id(self.subject_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "price_limit": self.price_limit,
            "item_id": self.subject._id,
            "user_email": self.user_email,
        }

    def load_item_price(self) -> float:
        self.subject.load_price()
        return self.subject.price

    def notify_if_price_reached(self) -> None:
        if self.subject.price < self.price_limit:
            print(
                f"Item {self.subject} has reached a price under {self.price_limit}. Latest price: {self.subject.price}."
            )
            Mailgun.send_email(
                email=[self.user_email],
                subject=f"Notification for {self.name}",
                text=f"Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.subject.price}. Go to this address to check your item: {self.subject.url}.",
                html=f'<p>Your alert {self.name} has reached a price under {self.price_limit}.</p><p>The latest price is {self.subject.price}. Check your item out <a href="{self.subject.url}>here</a>.</p>',
            )
