from models import User, Post, db 
from app import app
db.drop_all()
db.create_all()

u1 = User(first_name="Daniel", last_name="Wardwell")
u2 = User(first_name="Laura", last_name="Eng")
u3 = User(first_name="Shirt", last_name="Thompson", img_url="https://scontent-lax3-1.xx.fbcdn.net/v/t1.0-9/40141600_10157714483878502_2729047710509301760_o.jpg?_nc_cat=110&ccb=2&_nc_sid=09cbfe&_nc_ohc=_prwSZ4yCqMAX_F4inP&_nc_ht=scontent-lax3-1.xx&oh=bb846b41e079cd362bdfea5268da4904&oe=604250F3")

p1 = Post(title="My First Post!", content="This is my first post. it's not very good. okay goodbye", user_id=1)
p2 = Post(title="My Second Post!", content="This is my second post. it's worse okay goodbye", user_id=1)
p3 = Post(title="It burns!", content="I'm in hell. literal hell. you get used to it!", user_id=2)
p4 = Post(title="Stocks", content="Yes, I buy stocks. How do you think I got this lousy t-shirt!", user_id=3)


db.session.add_all([u1,u2,u3])


db.session.commit()

db.session.add_all([p1,p2,p3,p4])

db.session.commit()