docker start my-mongo
if [ -z "$(docker ps -a -q -f name=my-mongo)" ]; then
    docker run -d -p 27017:27017 --name my-mongo mongo
fi
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload