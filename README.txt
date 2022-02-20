This project is composed of 3 folders (data, model and notenooks).
We store the csv data into the data folder. 
The notebook jupyter is available at the notenooks directory. If having any problems with running this notebook, you can find the html output of the notebook in the same folder.
The model folder contains a python script named model.py where we transform the given account and the list of transactions into preprocessed data ready to be predicted. It contains mainly the same preprocessing functions as within the notebook.

The files requirements and requirements-eda contain the packages necessary to this project. 
The lightgbm.pkl is saved from the notebook jupyter and loaded in the app (main.py).
The test_main.py serves to test the predict API. 

The pdf file "Project submission" explains in details the steps to set up the Fast API Framework  and the forecast model. 

To create a virtual environment and load the API please type the follwing:

>python - m venv env
>. .\env\Scripts\activate
>pip install -r requirements.txt
>pip install -r requirements-eda.txt

>jupyter notenook

To run the API server, type the following:
>uvicorn main:app --reload

To test the predict API, run this:
>python test_main.py