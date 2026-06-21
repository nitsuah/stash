# VHS FEEDBACK

## vhs

### nav bar

- the "indicator" that shows the count of items under review shoshould be red not grey.

### capture

- on the "analyze" bar where it stages stored captures. can you move the "analyze and clear" buttons to the left side and order the imagess so that the oldest is the furthest to the right and the newest appears first on the right? this way we can always see the last capture and still see the buttons no matter how many captures we have staged. (and we can also see the progression of the captures as they come in from right to left, and we can also see the oldest capture on the right so we can decide if we want to keep it or not before it gets pushed out of view by newer captures).

### review

- honestly this is working REALLY well now. we'll want to improve the logic and add additional enrichment items and fix items long term and utilize more of the IMDB data to help our AI/llm. but so far pretty good and just needs tuning, but we've given the user the ability to not only improve but also to help the AI with the processing records. so theres definitely some efficiency harmony we can lean into here.

### collect

- the delete "swipe" should be visible so that users know which card they might be swiping and the distance required to swipe/trigger should be a bit bigger/longer to avoid accidental deletes (but the confirm dialog works so that keeps us safe). the left swipe to select works as expected!!! but i think inutitively these options might need to be reversed? so that right swipe is delete and left swipe is select? but we can also just make the delete swipe more visible and easier to trigger to avoid accidental deletes (select sort of highlights it blue, delete should use red accent). (and we can also keep the confirmation dialog for the delete action to prevent accidental deletes, but we already have this in place so that keeps us safe).
- on mobile - the "multi-select" action bar should replace the "wall/fill/etcc" bar at the top when in multi-select mode to avoid confusion and make it clear that we are in a different mode with different actions available and that navigating away or changign the view may affect that. but ideally i just want them to take up less space. (when nothing is selected then the bar shouldnt show up which it currently does very well at that part of the logic - only appear when one or more objects is selected/checkboxed).
- if the multi-select tape is active and the user has 1 tape or more selected these should be used as the scope of the Fix/Check buttons (right now those two just execute for all instead of ALL selected, this will help the user to selectively improve records instead of overwriting correct values or ones the user does not want to execute against. tl;dr makes the buttons scoped to specific records vs all).