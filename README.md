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


- `python manage.py migrate --run-syncdb`
- `python manage.py flush`
- `python manage.py loaddata base/testdata/fixtures01.json`
- `rm db.sqlite3; python manage.py migrate --run-syncdb; python manage.py loaddata base/testdata/fixtures01.json`
- `python3 manage.py dumpdata | jsonlint -f > tmp.json`

### Unittests

`pytest`



### Current Challenges

Visualizing annotations:


Idea: two columns; left panel: main text, right panel: current annotation.

left panel: all annotated text-sections (ATS) are highlighted in soft yellow. Sections which are covered by multiple annotations have stronger highlight, clicking on an ATS activates it;

active ATS:
is highlighted with different border color and displayed in the right panel.

right panel: shows metadata (top, small) and comment, offers possibility to copy comment

there are buttons (also activeateable by keys) to select the previous and next annotation. This also solves to access annotations which refer to the same text.

highlighting annotations which refer to the same text: is tricky because of the interaction of outer span and inner span and css selectors


### Current Bugs:

- offsets for comments do not work properly
    - reason: offsets refer to a dom-tree which ignores linebreaks between tags
    - → fixed (all nodes which only consists of newlines are replaced, tested with http://localhost:8000/doc/test-doc3/4225a/o/f8164504fd (md example))
