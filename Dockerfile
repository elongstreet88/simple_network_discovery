FROM python:3.11

# App python requirements
WORKDIR /app
COPY ./app/requirements.txt ./requirements.txt
RUN python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host github.com -r requirements.txt

# Create separate user space
RUN addgroup appgroup
RUN useradd appuser 
RUN adduser appuser appgroup

# Copy app over
COPY ./app ./

# Switch user context
USER appuser

# Startup the app
EXPOSE      8000
ENTRYPOINT  [ "uvicorn" ]
CMD         ["app:app", "--host", "0.0.0.0", "--port", "8000"]