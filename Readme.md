[![Build and Test](https://github.com/RevelioStartup/revelio-be/actions/workflows/django-build-test.yml/badge.svg)](https://github.com/RevelioStartup/revelio-be/actions/workflows/django-build-test.yml)

### Backend for Revelio App

#### Note: 
- Test coverage for now can be seen at Action --> select the **latest** workflow runs --> select `sonarcloud` Jobs --> open section `Run tests and generate coverage`

#### Note for developers: 
- For development, please add `dev` on every command that **runs** `manage.py` so it will use the Development environment. For example: `python manage.py dev runserver`, `python manage.py dev makemigrations`, `python manage.py dev migrate`.
- While developing, use `python manage.py dev loaddata data_seed_authentication.json` (for example) to load a data seed to development environment database.
- Currently available backend URL: `/try`