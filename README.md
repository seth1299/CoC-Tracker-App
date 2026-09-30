# CoC-Tracker-App

## Summary

This is a native windows application that uses Python 3.14 with PyInstaller to allow for easy tracking and managing of sent and received faxes for a medical office setting.

The faxes that are sent and received are known as Coordination-of-Care Requests (CoC Requests).

Currently, all of the information is stored in a Google Sheet (which can be extrapolated as a .csv file).

The overall purpose of this application and tracker is to keep track of sent and received faxes for

## Entries

As it currently stands as of 6:22 A.M. on 9-30-2026, each entry in the CoC Tracker is the following data structure:

> "Patient ID" (Text type, alphanumeric combination of 3-4 numbers including leading zeroes followed by 2-4 letters), such as "0001MPTS" | "Practice" (Text type, the name of the practice as a whole, such as "Pardee Hospital") | "Doctor" (Text type, the name of the doctor) | "Date Sent" (Date type, the date which the fax was sent) | "ROI Note?" (Boolean type, tracks if a Release of Information Note was created for that fax or not) | "Sent CoC Linked?" (Boolean type, tracks if the sent fax was linked to the patient's chart or not) | "Phone Number" (Text type, alphanumeric, the phone number to contact for medical records for that fax if any issues arise, with the input mask of xxx-xxx-xxxx) | "Fax Number" (Text type, alphanumeric, the fax number that the fax was sent to, with the input mask of xxx-xxx-xxxx) | "Received?" (Boolean type, tracks if we received a fax back in relation to that sent fax or not) | "Received Date" (Date type, tracks the date that we received a fax back in relation to that fax or not, blank if not) | "Reviewed?" (Boolean type, tracks if the fax reply to our sent fax has been reviewed by our medical staff yet or not) | "Linked?" (Boolean type, tracks if the reviewed Coordination of Care has been linked to the patient's chart yet or not) | "Complete?" (Boolean type, tracks if this entry is "Complete" or not, e.g. if there is a received fax that has been reviewed and linked to the patient's chart) | "NN" (Boolean type, stands for "Nurse's Note", only for faxes that we never received back and a Nurse had to put in a note explaining the situation) | "Counselor" (Dropdown that has Text type elements in it, single-choice, the name of the Counselor for the patient) | "Notes" (Text type, for any other loose miscellaneous notes that need to be put in related to the entry)

In the future, this data structure can be modified if there is a better proposed data structure.

Currently, there is no unique fax identification number or anything for each fax. This is because the web service that we use for the faxes does not have unique fax ID numbers, so we cannot have them in turn. This is why the CoC Tracker was created, because on the web service we use, the only way to look for previous faxes was if you knew the date it was sent/received, if you knew the fax number it was sent to, or if you knew the exact very fragile name of the fax that changes frequently as different employees review each fax and change the name of the fax accordingly (things like "in review", "reviewed", etc., making it impossible to accurately keep track of faxes by name). Thus, the Patient ID was used as a "primary key" of sorts, although it is not Unique, as of course, there can be multiple faxes sent for each patient. Ideally, there would be unique IDs for each sent and received fax, but this is currently a large limitation of the web service that we use for our faxes.
