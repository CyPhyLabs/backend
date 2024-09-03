# Use the official ContinuumIO miniconda3 image from Docker Hub
FROM continuumio/miniconda3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy the environment.yml file
COPY environment.yml /usr/src/app/

# Create the conda environment
RUN conda env create -f environment.yml

# Activate the environment
RUN echo "source activate t2t_backend" > ~/.bashrc
ENV PATH /opt/conda/envs/t2t_backend/bin:$PATH

# copy entrypoint.sh
COPY entrypoint.sh /usr/src/app/
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Copy the project
COPY . /usr/src/app/

# Install pip dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]