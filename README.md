This is the label checker used in the validation process of [Customlabel.nl](https://customlabel.nl/). The reason for using this extra check is because we create outlines of the generated barcodes. However, creating these outlines causes some barcodes to break i.e. unable to be scanned. Therefore, this little python scripts is written to detect these broken barcodes
 
## Getting Started

Install from [oschwartz10612](https://github.com/oschwartz10612) the latest release of [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/)

Place this folder somewhere easy to find on your device.

Afterwards create `local.py` in the root directory and make the global variable

```python
PATH_TO_POPPLER = r"LOCATION TO POPPLER"
# For instance
PATH_TO_POPPLER = r"C:\poppler-22.04.0\Library\bin"
```

Now Poppler is installed, we can install all the packages by running the following snippet in your terminal:

```bash
pip install -r requirements.txt
```

That's it, now you can run `labelchecker.py`.