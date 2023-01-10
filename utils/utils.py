from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from docx import Document


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def make_document(date: str, month: str, year: int, title: str, date_from: str, date_to: str, role: str, gender):
    # date = [(1, 3), (3, 9)]
    # month = [(3, 3), (6, 9)]
    # year = [(5, 3), (9, 9)]
    # title = [(1, 7)]
    # date_from = [(5, 7)]
    # date_to = [(7, 7)]
    # role = [(9, 7)]
    # his_her = [(11, 7), (3, 8)]
    # him_her = [(13, 7), (1, 8)]
    if gender == "male":
        his_her = "his"
        him_her = "him"
    his_her = [(11, 7), (3, 8)]
    him_her = [(13, 7), (1, 8)]
    file = Document("saved.docx")
    paragraphs = file.paragraphs
    for p in range(len(paragraphs)):
        runs = p.runs
        for r in range(len(runs)):
            if r == 1 and p == 3 or r == 3 and p == 9:
                runs[r].clear()
                runs[r].add_text(date)
            elif r == 3 and p == 3 or r == 6 and p == 9:
                runs[r].clear()
                runs[r].add_text(month)
            elif r == 5 and p == 3 or r == 9 and p == 9:
                runs[r].clear()
                runs[r].add_text(str(year))
            elif r == 1 and p == 7:
                runs[r].clear()
                runs[r].add_text(title)
            elif r == 5 and p == 7:
                runs[r].clear()
                runs[r].add_text(date_from)
            elif r == 7 and p == 7:
                runs[r].clear()
                runs[r].add_text(date_to)
            elif r == 9 and p == 7:
                runs[r].clear()
                runs[r].add_text(role)
            elif r == 11 and p == 7 or r == 3 and p == 8:
                runs[r].clear()
                runs[r].add_text(his_her)
            elif r == 13 and p == 7 or r == 1 and p == 8:
                runs[r].clear()
                runs[r].add_text(him_her)
    file.save("output.docx")


    