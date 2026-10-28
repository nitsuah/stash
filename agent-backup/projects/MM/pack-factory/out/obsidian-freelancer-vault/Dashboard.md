# Dashboard
## Active projects (Dataview)
```dataview
TABLE client, status, due FROM "Projects" WHERE status != "done" SORT due ASC
```
## Clients
```dataview
LIST FROM "Clients"
```
Without Dataview, open the Projects and Clients folders directly.
