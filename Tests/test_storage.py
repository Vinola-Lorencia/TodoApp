from App.storage import Storage


def test_save_and_load():

    storage = Storage("data/test_tasks.json")

    tasks = [
        {"id":1,"title":"Test Task","completed":False}
    ]

    storage.save_tasks(tasks)

    loaded_tasks = storage.load_tasks()

    assert loaded_tasks == tasks