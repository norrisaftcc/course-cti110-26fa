# MANIFEST: DHW1_start (corrected)

This package replaces the original DHW1_start.zip. Three files changed. One file is new. `run_queries.py` is unchanged.

## Changed files

### create_signup_db.py
| Change | How | Why |
|---|---|---|
| Sample row fixed | The `users` row had 7 values. It now has 8: `'naruto_u'` was added as `username`. `'LoveRamen1'` stays as `password_hash`. | The `INSERT` has 8 placeholders. A 7-value row raised `ProgrammingError: Incorrect number of bindings supplied. The current statement uses 8, and there are 7 supplied.` |
| Column-order comment added | A comment above `users` lists the 8 values in order and says `user_id` is not included. | Students asked if `user_id` is a missing 9th value. It is not. `user_id INTEGER PRIMARY KEY` is assigned by SQLite. The `INSERT` leaves it out on purpose. |
| Hint comments added in STEP 1 | Two NOTE lines: SQLite assigns `user_id`; no comma after the last column. | The starter `CREATE TABLE` ends with `user_id INTEGER PRIMARY KEY,`. A trailing comma before `)` is a syntax error. |

Not changed: the `CREATE TABLE` body. It is still the student's task.

### reflection.md
| Change | How | Why |
|---|---|---|
| Title | `DHW2` changed to `DHW1`. | The assignment is DHW1. |
| File name in the footer | `signup_he.db` changed to `signup_hw.db`. | Typo. The script creates `signup_hw.db`. |
| Question 3 | Added: "The answer can be 0 if none of your users have country 'USA'." | The sample row uses `'JAPAN'`. Query q3 filters on `'USA'`. Students with no USA users saw 0 rows and did not know if it was an error. |

### Folder name
`DHW2_start/` is now `DHW1_start/`. Why: the assignment is DHW1.

## Unchanged
- `run_queries.py`. The five queries are correct as written.

## Not in this package (fix in Canvas)
- The Canvas page checklist heading says "DHW2 Checklist". It should say DHW1.
- The Canvas page says to name the folder `DHW1_LastnameFirstname`. The folder here is `DHW1_start`. This is correct. Students rename it.

## Verification
- Starter as shipped: fails with `OperationalError` (trailing comma). This is expected. Students fix it in STEP 1.
- With a completed `CREATE TABLE` (8 columns after `user_id`) and the corrected sample row: runs without errors. The output row is `(1, 'Naruto', 'Uzamaki', 'ramen@example.com', 'naruto_u', 'LoveRamen1', '2026-06-01', 'JAPAN', 16)`.
- With the original 7-value row: fails with the `ProgrammingError` above.
