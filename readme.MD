create a new conda env with version 3.9 (conda_env_name)
conda activate conda_env_name or just open a new terminal
conda install -y -c conda-forge --file requirements.txt

(if the above code does not work, follow the below 3 steps)
- conda install flask
- conda install -c conda-forge flask-sqlalchemy
- conda install -c conda-forge flask-login

run seed.py to populate the db and start the project by running the run.py file
