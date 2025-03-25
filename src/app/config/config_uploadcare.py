import os
from pyuploadcare import Uploadcare

UPLOADCARE_PUBLIC_KEY = os.getenv("UPLOADCARE_PUBLIC_KEY")
UPLOADCARE_SECRET_KEY = os.getenv("UPLOADCARE_SECRET_KEY")

uploadcare = Uploadcare(UPLOADCARE_PUBLIC_KEY, UPLOADCARE_SECRET_KEY)

if not UPLOADCARE_PUBLIC_KEY or not UPLOADCARE_SECRET_KEY:
    raise ValueError("Uploadcare keys are not set!")
