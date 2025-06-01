
from dotenv import dotenv_values


DEBUG = True

ENV = dotenv_values()

ACCESS_TOKEN = ENV.get("ACCESS_TOKEN")

CSRF_TOKEN: str = ENV["CSRF_TOKEN"]
LI_AT: str = ENV["LI_AT"]

ALT_CSRF_TOKEN: str = ENV["ALT_CSRF_TOKEN"]
ALT_LI_AT: str = ENV["ALT_LI_AT"]