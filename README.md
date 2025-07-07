# InteractiveTracker

Install the following dependencies:

```bash
pip3 install -r requirements.txt
```

## Usage

To run the app, execute the following command:

```bash
streamlit run src/streamlit_app.py
```

You also need to have a `csvpath.txt` file in the root directory. This file should contain the path
to a csv file containing student data (e.g. `"students.csv`) in the following format:

```csv
name,frequency_per_week,last_lesson_date,lesson_number_taken_so_far,status,is_online,billing_cycle,note
```

## Example `students.csv`

```csv
name,frequency_per_week,last_lesson_date,lesson_number_taken_so_far,status,is_online,billing_cycle,note
John Doe,2,2023-10-01,5,active,yes,monthly,Out of town next week
Jane Smith,1,2023-10-02,3,inactive,no,yearly,Needs to reschedule
```
