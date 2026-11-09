# Report export

As agreed in draft review 7, we now require authentication and export:read.
We do not claim that these checks make all exports safe.
Exports contain at most 100 rows. Authentication fails before permission checks;
permission checks fail before the row limit check. Output uses UTF-8.
The permission-before-size order avoids exposing report size to unauthorized users.
