# SimpleFeedback

Experimental code, based on <https://github.com/acdh-oeaw/django-recogito> and ["Django REST Framework Oversimplified"]([https://www.youtube.com/watch?v=cJveiktaOSQ).

The goals is the following:

## Idea Description

- The user (A) can upload a text in markdown.
- The user (A) receives 2 URLS:
    - easyfeedback.net/\<text-slug>-\<ownertoken>
    - easyfeedback.net/\<text-slug>-\<reviewtoken>
- The user (A) can share the second URL to user (B), user (C) etc.
- User (B) can open easyfeedback.net/\<text-slug>-\<reviewtoken> and
    - read the text,
    - make annotations,
    - enter a name (e.g. "user (B)"),
    - solve a captcha (maybe optional).
    - upload the annotation data as "a review".
- User (C) etc can do the same. They do not see the annotations of other users.
- User (A) can then open easyfeedback.net/\<text-slug>-\<ownertoken> and
    - see that two reviews were uploaded,
    - display each review individually,
    - jointly display selected reviews (e.g. to see where multiple people had comments).
