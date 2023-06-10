# Order-Tracking-Software
Order tracking and receipt prinitng software.

## Development SetUp
In order to run the application you need to pipenv installed. You can install it by running `pip3 install pipenv`

Then run:<br>
`pipenv install -r requirements.txt`
or simply
`pipenv install`

Then migrate the databases using `python3 core/manage.py makemigrations` and `python3 core/manage.py migrate`.

You can run the server with the following command.
`python3 core/manage.py runserver`
