# Dependencies

tesseract is installed at "/usr/bin/tesseract"

python -m pip install flask
python -m pip install opencv-python
python -m pip install pytesseract

# Running the app

python app.py

# Notes

The app can be tested by going the URL "localhost:5000" in a browser on the
same machine that the flask development server is running. Uploaded image files
are saved to the "uploads" directory and are not deleted.
