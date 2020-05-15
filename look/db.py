import traceback

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from look.model.user import User
from look.model.category import Category
from look.model.board import Board
from look.model.chapter import Chapter
from look.model.subchapter import Subchapter

def init_db():
    print("init_db")
    engine = create_engine('mysql+mysqldb://root:root@localhost:3306/codedu?charset=utf8')

    db_session = sessionmaker(bind=engine)

    User.metadata.create_all(engine)
    Category.metadata.create_all(engine)
    Board.metadata.create_all(engine)
    Chapter.metadata.create_all(engine)
    Subchapter.metadata.create_all(engine)

    return db_session

def insert_dummy_data(db_session):
    print("insert_dummy_data")

    dummy_data = {
        'User' : [
            {
                'username':'ctmanjak',
                'email':'ctmanjak@gmail.com',
                'password':'ctmanjak123!',
            },
            {
                'username':'wjh97',
                'email':'wjh97@naver.com',
                'password':'wjh97123!',
            },
            {
                'username':'kdu1524023',
                'email':'kdu1524023@kduiv.ac.kr',
                'password':'kdu1524023123!',
            },
            {
                'username':'annyeong',
                'email':'annyeong@gmail.com',
                'password':'annyeong123!',
            },
            {
                'username':'ctmanjak2',
                'email':'ctmanjak2@gmail.com',
                'password':'ctmanjak123!',
            },
        ],
        'Category' : [
            {
                'title':'Category1',
                'subtitle':'Category1\'s subtitle',
            },
            {
                'title':'Category2',
                'subtitle':'Category2\'s subtitle',
            },
        ],
        'Board' : [
            {
                'title':'Board1',
                'subtitle':'Board1\'s subtitle',
            },
            {
                'title':'Board2',
                'subtitle':'Board2\'s subtitle',
            },
        ],
        'Chapter' : [{'title':f'Chapter{i+1}'} for i in range(4)],
        'Subchapter' : [{'title':f'Subchapter{i+1}'} for i in range(8)],
    }

    models = {}

    for table in dummy_data:
        models[table] = []
        for data in dummy_data[table]:
            models[table].append(globals()[table](**data))

    progress_dd = [
        [1, 1],
        [1, 2],
        [2, 1],
    ]
    for data in progress_dd:
        models['User'][data[0]-1].learning_progress.append(models['Subchapter'][data[1]-1])

    category_board_dd = [
        [1, 1],
        [1, 2],
        [2, 1],
    ]
    for data in category_board_dd:
        models['Category'][data[0]-1].board.append(models['Board'][data[1]-1])

    board_chapter_dd = [
        [1, 1],
        [1, 2],
        [2, 3],
        [2, 4],
    ]
    for data in board_chapter_dd:
        models['Board'][data[0]-1].chapter.append(models['Chapter'][data[1]-1])

    chapter_subchapter_dd = [
        [1, 1],
        [1, 2],
        [2, 3],
        [2, 4],
        [3, 5],
        [3, 6],
        [4, 7],
        [4, 8],
    ]
    for data in chapter_subchapter_dd:
        models['Chapter'][data[0]-1].subchapter.append(models['Subchapter'][data[1]-1])

    for table in models:
        for model in models[table]:
            db_session.add(model)

    try:
        db_session.commit()
    except:
        traceback.print_exc()
        db_session.rollback()