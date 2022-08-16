# Hacking an electronic diary

These are the scripts for the e-diary website. Scripts are designed to fix bad marks, remove chastisements and create commendation from teachers.

### How to install

To install these scripts:
1. Install the e-diary website https://github.com/devmanorg/e-diary on your local computer by following the instructions in its repository.
2. Get your own database file somewhere.
3. Start the e-diary website.
4. Copy the `scripts.py` file to a local drive and put it in the root directory of the website (in the same directory as the `manage.py` file).

### How to start

Run cmd, change to the website folder on the command line, then start an interactive Python console to interact with the database:
```
cd {website_folder_on_your_local_disk}
python manage.py shell
```

Make the import of the scripts.py:
```
import scripts
```

### How to edit data of the e-diary

To fix bad marks, run the command:
```
scripts.fix_marks(<schoolkid_name>)
```

To remove all chastisements, run the command:
```
scripts.remove_chastisements(<schoolkid_name>)
```

To add commendation, run the command:
```
scripts.create_commendation(<schoolkid_name>, <subject_title>)
```
Commendation will be added to the last lesson in the specified subject.


### Project Goals

The code is written for educational purposes in the process of learning on the online course on Django ORM for Python developers.