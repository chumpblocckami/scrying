pip install -r requirements.deploy.txt

rm -rf dist
python setup.py check
python setup.py sdist

python setup.py bdist_wheel
twine upload dist/*