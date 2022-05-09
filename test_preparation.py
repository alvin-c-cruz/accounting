import os
import shutil


def test_create_empty_database():
    main_file = os.path.join('instance', 'data.db')
    backup_file = os.path.join('instance', 'data_test.db')

    os.remove(main_file)
    shutil.copy(backup_file, main_file)

    assert True
