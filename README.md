# Book writer

## Setup
### Clone the repo
```bash
git clone git@github.com:moinakmalkhan/book-writer.git
cd book-writer
```

### Setup virtual environment
Create a virtual environment using python3
```bash
python3 -m venv venv
```
Activate the virtual environment
```bash
source venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Setup environment variables
Copy the `.env.example` file to `.env` and update the values
```bash
cp .env.example .env
```

### Apply migrations
```bash
python manage.py migrate
```

### Create superuser
```bash
python manage.py createsuperuser
```

### Run the server
```bash
python manage.py runserver
```

### Run tests
```bash
python manage.py test
```
