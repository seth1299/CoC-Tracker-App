# CoC-Tracker-App

## Summary

This is a native windows application that uses Python 3.14 with Qt GUI and PyInstaller to allow for easy tracking and managing of sent and received faxes for a medical office setting.

The faxes that are sent and received are known as Coordination-of-Care Requests (CoC Requests).

Currently, all of the information is stored in a Google Sheet (which can be extrapolated as a .csv file).

The overall purpose of this application and tracker is to keep track of sent and received faxes for

## Development setup

The starter application uses [PySide6](https://doc.qt.io/qtforpython-6/) for
the Qt user interface and Python's built-in SQLite support for local storage.

On Windows, run the included setup script. It creates a project-local virtual
environment, installs the dependencies into it, and verifies both packages:

```console
setup.bat
```

Alternatively, create and activate a virtual environment manually, then
install the dependencies:

   ```console
   python -m pip install -r requirements.txt
   ```

Start the application:

   ```console
   .venv\Scripts\python.exe main.py
   ```

The application creates `coc_tracker.db` beside `main.py`. When running a
packaged build, it creates the database beside `CoCTracker.exe`. The generated
database, build output, and Python cache files are excluded from Git.

The initial window includes a small notes list solely to demonstrate writing
to and reading from SQLite. It can be replaced by the final tracker workflow
as the application's data model is developed.

## Windows build

Run `build.bat` from a command prompt after completing `setup.bat`.
PyInstaller places the distributable application in
`dist\CoCTracker\CoCTracker.exe`. The build uses one-directory mode so Qt's
required libraries are distributed with the executable.

`build.bat` deliberately uses `.venv\Scripts\python.exe`, rather than whichever
Python happens to be first on `PATH`. If the environment or required packages
are missing, it exits with instructions to run `setup.bat`.

### HTTP 403 troubleshooting

An HTTP 403 while running `pip install` means that the network proxy or Python
package index rejected the download. It is not caused by PySide6, PyInstaller,
or this application's source code. Try these steps from a normal Windows
Command Prompt:

1. Check whether pip has been pointed at a private index:

   ```console
   py -m pip config debug
   set PIP
   ```

2. If `PIP_INDEX_URL` names an obsolete or unauthorized server, clear it for
   the current prompt and retry against the official index:

   ```console
   set PIP_INDEX_URL=
   py -m pip install --index-url https://pypi.org/simple PySide6 PyInstaller
   ```

3. Check proxy variables with `set | findstr /I proxy`. On a network that does
   not require a proxy, clear stale values with `set HTTP_PROXY=` and
   `set HTTPS_PROXY=`. On a managed network, do not bypass the proxy; ask the
   network administrator to allow `pypi.org` and `files.pythonhosted.org`, or
   obtain the organization's approved index URL and set it with:

   ```console
   py -m pip config set global.index-url https://your-approved-index/simple
   ```

4. If the target computer cannot access a package index, download compatible
   Windows wheels on an internet-connected computer, copy them into a
   `wheelhouse` directory, and install without network access:

   ```console
   py -m pip download --dest wheelhouse -r requirements.txt
   .venv\Scripts\python.exe -m pip install --no-index --find-links=wheelhouse -r requirements.txt
   ```

Do not use `--trusted-host` to work around a 403. That option disables parts of
TLS verification and does not grant permission through a rejecting proxy.

## Entries

As it currently stands as of 6:22 A.M. on 9-30-2026, each entry in the CoC Tracker is the following data structure:

> "Patient ID" (Text type, alphanumeric combination of 3-4 numbers including leading zeroes followed by 2-4 letters), such as "0001MPTS" | "Practice" (Text type, the name of the practice as a whole, such as "Pardee Hospital") | "Doctor" (Text type, the name of the doctor) | "Date Sent" (Date type, the date which the fax was sent) | "ROI Note?" (Boolean type, tracks if a Release of Information Note was created for that fax or not) | "Sent CoC Linked?" (Boolean type, tracks if the sent fax was linked to the patient's chart or not) | "Phone Number" (Text type, alphanumeric, the phone number to contact for medical records for that fax if any issues arise, with the input mask of xxx-xxx-xxxx) | "Fax Number" (Text type, alphanumeric, the fax number that the fax was sent to, with the input mask of xxx-xxx-xxxx) | "Received?" (Boolean type, tracks if we received a fax back in relation to that sent fax or not) | "Received Date" (Date type, tracks the date that we received a fax back in relation to that fax or not, blank if not) | "Reviewed?" (Boolean type, tracks if the fax reply to our sent fax has been reviewed by our medical staff yet or not) | "Linked?" (Boolean type, tracks if the reviewed Coordination of Care has been linked to the patient's chart yet or not) | "Complete?" (Boolean type, tracks if this entry is "Complete" or not, e.g. if there is a received fax that has been reviewed and linked to the patient's chart) | "NN" (Boolean type, stands for "Nurse's Note", only for faxes that we never received back and a Nurse had to put in a note explaining the situation) | "Counselor" (Dropdown that has Text type elements in it, single-choice, the name of the Counselor for the patient) | "Notes" (Text type, for any other loose miscellaneous notes that need to be put in related to the entry)

In the future, this data structure can be modified if there is a better proposed data structure.

Currently, there is no unique fax identification number or anything for each fax. This is because the web service that we use for the faxes does not have unique fax ID numbers, so we cannot have them in turn. This is why the CoC Tracker was created, because on the web service we use, the only way to look for previous faxes was if you knew the date it was sent/received, if you knew the fax number it was sent to, or if you knew the exact very fragile name of the fax that changes frequently as different employees review each fax and change the name of the fax accordingly (things like "in review", "reviewed", etc., making it impossible to accurately keep track of faxes by name). Thus, the Patient ID was used as a "primary key" of sorts, although it is not Unique, as of course, there can be multiple faxes sent for each patient. Ideally, there would be unique IDs for each sent and received fax, but this is currently a large limitation of the web service that we use for our faxes.
