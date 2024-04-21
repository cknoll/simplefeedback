# SimpleFeedback

Experimental code, based on <https://github.com/acdh-oeaw/django-recogito> and ["Django REST Framework Oversimplified"]([https://www.youtube.com/watch?v=cJveiktaOSQ).

The goals is the following:

## Idea Description

- The user (A) can submit a text in markdown.
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

## Notes for Local Testing

### Manual Testing


- `rm -f db.sqlite3; python manage.py migrate --run-syncdb; python manage.py loaddata base/testdata/fixtures01.json`
- `python manage.py runserver`

Store test-data:
- `python3 manage.py dumpdata | jsonlint -f > tmp.json`

### Unittests

`pytest` (require splinter installed and configured)

### Feedback

Contact me <https://cknoll.github.io/pages/impressum.html>
