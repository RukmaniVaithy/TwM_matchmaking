### Purpose:
TWM Matchmaking is intended to pair mentee and mentor based on preference provided. It eliminates the need to make manual matchmaking which turns cumbersome in case of large turnouts for the event.

Implementation is based on set of pre-defined rules for scenarios defined below.

### Scenarios:

1. **Best First Match**: Mentee's count(first preference) strictly 1.
2. **Ambiguous First Match**: If more than one mentee chose a mentor as 1st choice, chose the mentor's 1st preference.
3. **First Match with HI**: If more than one mentee chose a mentor as 1st choice, but the mentor has not chosen either of the mentee as a first- try 2nd, or Human Intervention.
4. **Second Match**: Repeat Step 1 and 2 for Second Preference.
   - **Best Second Match**: Mentee with no decision on first match, repeat step 1, but for second preference.
   - **Ambiguous Second Match**: 
5. Rest mark as Human Intervention.