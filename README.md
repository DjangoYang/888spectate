# TODO
In the next **60 minutes**, please complete the following tasks.

Do as much as possible within the allotted time.

**Use of supporting pseudo code is acceptable if necessary**.


## 1. Finish the events route
Add logic to each of the endpoints within the events route (application/routes/events.py) to the best of your knowledge.


## 2. When creating an event, the Logos property of the event needs to be populated with logo links associated with the teams participating in the event.

The links are available via a free third party API documented here https://www.thesportsdb.com/free_sports_api
The endpoint is: **www.thesportsdb.com/api/v1/json/3/searchteams.php?t=<QUERY>** (search for team by name) and the relevant key in the response is **strLogo.**.

**Example:**.
Event name: "Arsenal v Leeds";
Requests to the sportsdb service:

**GET www.thesportsdb.com/api/v1/json/3/searchteams.php?t=Arsenal**

and

**GET www.thesportsdb.com/api/v1/json/3/searchteams.php?t=Leeds**

Format of stored data in logos: 

**link_1|link_2**.

If one of the links is not found, use an empty string for the missing link:

**""|link_2 or link_1|""**.

If no link is found at all, store the null value.

**You can assume that a successful response is always correct, so if there are multiple records in the body, always refer to the first one.
If for any reason the system is unable to get a successful response, the failure must be logged (optionally with a reason).**.


## SETUP
To install virtual env, dependencies and run app, execute:
```make setup```

## DEBUGGER
Debugger (debugpy) is installed and listens on port **5678**

