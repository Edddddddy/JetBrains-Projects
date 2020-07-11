from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine("sqlite:///todo.db?check_same_thread=False")

Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def printTodaysTasks():
    print("Today {} {}:".format(datetime.today().day, datetime.today().strftime("%b")))
    tasks = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    if len(tasks) == 0:
        print("Nothing to do!")
    else:
        for i, v in enumerate(tasks):
            print("{}. {}".format(i + 1, v.task))
    print("")


def add_task(string, date):
    dateList = date.split("-")
    dateObject = datetime(int(dateList[0]), int(dateList[1]), int(dateList[2])).date()
    newTask = Table(task=string, deadline=dateObject)
    session.add(newTask)
    session.commit()


def printAllTasks():
    tasks = session.query(Table).all()
    if len(tasks) == 0:
        print("Nothing to do!")
    else:
        for i, v in enumerate(tasks):
            print("{}. {}. {} {}".format(i + 1, v.task, v.deadline.day, v.deadline.strftime("%b")))
    print("")


def printWeeksTasks():
    currentDay = datetime.today()
    week = list()
    week.append(currentDay)
    for i in range(1, 7):
        week.append(currentDay + timedelta(i))
    for i in week:
        print("{}:".format(i.strftime("%A %d %b")))
        tasks = session.query(Table).filter(Table.deadline == i.date()).all()
        if len(tasks) == 0:
            print("Nothing to do!")
        else:
            for index, v in enumerate(tasks):
                print("{}. {}".format(index + 1, v.task))
        print("")


def printMissedTasks():
    print("Missed tasks:")
    tasks = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
    if len(tasks) == 0:
        print("Nothing is missed!")
    else:
        for i, v in enumerate(tasks):
            print("{}. {}. {}".format(i + 1, v.task, v.deadline.strftime("%d %b")))
    print("")


def deleteTask():
    tasks = session.query(Table).all()
    if len(tasks) == 0:
        print("Nothing to delete")
    else:
        print("Chose the number of the task you want to delete:")
        for i, v in enumerate(tasks):
            print("{}. {}. {} {}".format(i + 1, v.task, v.deadline.day, v.deadline.strftime("%b")))
    taskToDelete = int(input())
    session.delete(tasks[taskToDelete])
    session.commit()
    print("The task has been deleted!")
    print("")


exited = False
while not exited:
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    stdin = int(input())
    print("")
    if stdin == 1:
        printTodaysTasks()
    elif stdin == 2:
        printWeeksTasks()
    elif stdin == 3:
        printAllTasks()
    elif stdin == 4:
        printMissedTasks()
    elif stdin == 5:
        print("Enter task")
        task = input()
        print("Enter deadline")
        deadline = input()
        add_task(task, deadline)
        print("The task has been added!")
        print("")
    elif stdin == 6:
        deleteTask()
    elif stdin == 0:
        exited = True
        break

print("Bye!")
