# DHW1 – Query Analysis Questions

After you run `run_queries.py`, review your output and answer the questions below in complete sentences.

> **Important:** Your exact answers will be different from your classmates because each student may enter different fake user data.  
> Focus on explaining what your own query results show.

## 1) All Users (`SELECT * FROM users`)
How many total rows (users) are displayed in your output?  
Does this match the number of users you intended to insert?

# ANSWER: 

## 2) Name + Email (`SELECT first_name, last_name, email FROM users`)
What information is shown in this query that is different from Query #1?  

# ANSWER:

## 3) Users from USA (`WHERE country = 'USA'`)
How many users from the USA appear in your results? (The answer can be 0 if none of your users have country 'USA'.)

# ANSWER:

## 4) Total User Count (`COUNT(*)`)
What value did your `total_users` query return?  
How can this query help you check whether your data was inserted correctly?

# ANSWER:

## 5) 3 Most Recent Signups (`ORDER BY signup_date DESC LIMIT 3`)
Which 3 usernames appear as the most recent in **your** output?  

# ANSWER: 

---

> What should be in your zipped folder when you turn it in to Canvas -> create_signup_db.py, run_queries.py, signup_hw.db, and reflection.md