import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

print(f"SECRET_KEY: {env.str('SECRET_KEY')}")
print(f"DEBUG: {env.bool('DEBUG', default=False)}")
print(f"ALLOWED_HOSTS: {env.list('ALLOWED_HOSTS', default=[])}")
