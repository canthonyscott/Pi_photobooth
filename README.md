## Quick Start

1. Clone the repo.
2. Install the required packages (virtual environment recommended)
3. Edit the Pi_photobooth/settings.py file and set DEBUG = True
4. Run server using `python manage.py runserver`
5. Navigate to your browser http://127.0.0.1:8000/capture


## Notes
* If you plan to deploy this on a public server makes sure to change the `SECRET_KEY`. This should always remain a secret. I didn't remove it from this repo because this only ever ran locally on my Raspberry Pi.
* Unfortunately because I was making this in a time crunch there are some variables and directories that are hard coded. To get this working full on your raspberry pi you will likely need to edit some locations in the python files. One day I hope to return to this and clean it up to be used more generally. Im thinking docker container.
