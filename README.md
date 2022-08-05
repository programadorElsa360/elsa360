# ELSA_backend

<!-- GETTING STARTED -->

### Built With

- [![Django][django]][django-url]
- [![Django REST Framework][django-rest-framework]][django-rest-url]
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

You'll need to have Python installed in your system, it's recommended to set up a Python virtual environment to install the project's dependencies without interfering with your global Python packages.

### Installation

1. Clone the repo

   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```

2. Once your virtual environment is set up, proceed to install the project's dependencies via pip.
   ```sh
   pip install -r requirements.txt
   ```

Before launching the project, please note the location of the .env.example file and create a .env.{stage} file in the same directory, where {stage} is the stage you intend to launch the project in, supported stages are development and production. You can create both .env files if you so desire.

- bash
  ```sh
  cat > .env.development
  ```

To configure the .env file, please check the contents of the .env.example file for the necessary environment variables to be set.

The project comes with 2 settings.py files, for each the development and production stages, it is recommended to use the development settings when launching the project locally, you can choose which settings to use by setting the DJANGO_SETTINGS_MODULE environment variable.

- bash

  ```sh
  export DJANGO_SETTINGS_MODULE=configuration.settings.development
  ```

Remember to set up a local PostgreSQL Database for the project if you're launching it locally.

Finally to launch the project locally just use
  ```sh
  python manage.py runserver
  ```

  <!-- MARKDOWN LINKS & IMAGES -->
  <!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[django]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white
[django-url]: https://www.djangoproject.com/
[django-rest-framework]: https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray
[django-rest-url]: https://www.django-rest-framework.org/
