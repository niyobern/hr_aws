from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def make_document():
    date = [(1, 3), (3, 9)]
    month = [(3, 3), (6, 9)]
    year = [(5, 3), (9, 9)]
    title = [(1, 7)]
    date_from = [(5, 7)]
    date_to = [(7, 7)]
    role = [(9, 7)]
    his_her = [(11, 7), (3, 8)]
    him_her = [(13, 7), (1, 8)]
    pass