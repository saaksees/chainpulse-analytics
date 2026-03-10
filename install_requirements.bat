@echo off
echo Installing ChainPulse Requirements...
echo.

pip install pandas
pip install numpy
pip install matplotlib
pip install seaborn
pip install scikit-learn
pip install xgboost
pip install imbalanced-learn
pip install prophet
pip install joblib
pip install nltk
pip install wordcloud
pip install squarify
pip install openpyxl
pip install flask
pip install flask-cors
pip install reportlab
pip install statsmodels
pip install lightgbm

echo.
echo Installation complete!
echo.
echo Testing imports...
python -c "import pandas; print('pandas OK')"
python -c "import numpy; print('numpy OK')"
python -c "import matplotlib; print('matplotlib OK')"
python -c "import seaborn; print('seaborn OK')"
python -c "import sklearn; print('scikit-learn OK')"

echo.
echo Ready to run pipeline!
pause