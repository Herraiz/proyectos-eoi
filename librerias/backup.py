import zipfile
import os
import statistics as st
import datetime

def welcome():
    print('''
Welcome to the first miniproject of @RoberHerraiz for Libs classes!!

This program will backup all you files with extensions:
- .py
- .ipynb
- .md
. .rst
    ''')

def weekday_picker():

    ''' The weekday_picker function will calculate the week of the day at this moment
    and return the desired name for the zip file, "dayoftheweek.zip"'''

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today_weekday = datetime.date.today().weekday()
    weekday = weekdays[today_weekday]+".zip"
    print(f'The backup will be saved as {weekday}\n')

    return weekday


def backup(weekday):

    ''' This function will make a backup of all the files with a specific extension at the desired path on a .zip file'''

    backup_extensions = [".py", ".ipynb",".md", ".rst"]
    sizes = []

    with zipfile.ZipFile(weekday, 'w') as f: #solo funciona en el directorio del archivo y no es recursivo, hay que usar walk
        for fn in os.listdir(path):
            _, ext = os.path.splitext(fn)
            if ext in backup_extensions:
                sizes.append(os.path.getsize(fn))
                print(f"Saving {fn}")
                f.write(fn)

    print('')
    print(f'A total of {len(sizes)} files with a total size of {sum(sizes)} bytes have been saved.')
    print(f'The average size of the files is {st.mean(sizes)} bytes.')


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    path = "."
    welcome()
    weekday = weekday_picker()
    backup(weekday)
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f'The backup took {duration.seconds} seconds and {duration.microseconds} microseconds.')


        # with zipfile.ZipFile(weekday_picker(), 'w') as f:
        # for t in os.walk(path):
        #     _, _, files = t
        #     for fn in files:
        #         _, ext = os.path.splitext(fn)
        #         if ext in backup_extensions:
        #             sizes.append(os.path.getsize(fn))
        #             print(f"Saving {fn}")
        #             f.write(fn)