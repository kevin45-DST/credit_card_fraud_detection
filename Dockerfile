# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

FROM python:3.11-slim

WORKDIR /app

ARG ENVIRONMENT=docker

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY config ./config
COPY deployment ./deployment
COPY src/utils ./src/utils
COPY src/ml_pipeline/training_pipeline.py ./src/ml_pipeline/training_pipeline.py
COPY src/ml_pipeline/tracking_pipeline.py ./src/ml_pipeline/tracking_pipeline.py
COPY src/ml_pipeline/logging_pipeline.py ./src/ml_pipeline/logging_pipeline.py
COPY src/ml_toolbox/data_science/data ./src/ml_toolbox/data_science/data
COPY src/ml_toolbox/data_science/preprocessing ./src/ml_toolbox/data_science/preprocessing
COPY src/ml_toolbox/data_science/training/training_manager.py ./src/ml_toolbox/data_science/training/training_manager.py
COPY src/ml_toolbox/data_science/training/training_router.py ./src/ml_toolbox/data_science/training/training_router.py
COPY src/ml_toolbox/data_science/training/training_backend.py ./src/ml_toolbox/data_science/training/training_backend.py
COPY src/ml_toolbox/mlops/tracking/tracking_manager.py ./src/ml_toolbox/mlops/tracking/tracking_manager.py
COPY src/ml_toolbox/mlops/tracking/tracking_backend.py ./src/ml_toolbox/mlops/tracking/tracking_backend.py
COPY src/ml_toolbox/transversal/evaluation/evaluation_manager.py ./src/ml_toolbox/transversal/evaluation/evaluation_manager.py
COPY src/ml_toolbox/transversal/evaluation/evaluation_backend.py ./src/ml_toolbox/transversal/evaluation/evaluation_backend.py
COPY src/ml_toolbox/transversal/logs/log_storage/log_storage_manager.py ./src/ml_toolbox/transversal/logs/log_storage/log_storage_manager.py
COPY src/ml_toolbox/transversal/logs/log_storage/log_storage_backend.py ./src/ml_toolbox/transversal/logs/log_storage/log_storage_backend.py
COPY src/ml_toolbox/transversal/logs/log_collector/log_collector_manager.py ./src/ml_toolbox/transversal/logs/log_collector/log_collector_manager.py
COPY src/ml_toolbox/transversal/persistence/model_persistence_manager.py ./src/ml_toolbox/transversal/persistence/model_persistence_manager.py
COPY src/ml_toolbox/transversal/persistence/model_persistence_backend.py ./src/ml_toolbox/transversal/persistence/model_persistence_backend.py
COPY src/ml_toolbox/transversal/reporting/report_manager.py ./src/ml_toolbox/transversal/reporting/report_manager.py

#implementations
COPY src/ml_toolbox/data_science/training/implementations/scikit_learn_backend.py ./src/ml_toolbox/data_science/training/implementations/scikit_learn_backend.py
COPY src/ml_toolbox/mlops/tracking/implementations/mlflow_backend.py ./src/ml_toolbox/mlops/tracking/implementations/mlflow_backend.py
COPY src/ml_toolbox/transversal/evaluation/implementations/scikit_learn_backend.py ./src/ml_toolbox/transversal/evaluation/implementations/scikit_learn_backend.py
COPY src/ml_toolbox/transversal/logs/log_storage/implementations/elasticsearch_backend.py ./src/ml_toolbox/transversal/logs/log_storage/implementations/elasticsearch_backend.py
COPY src/ml_toolbox/transversal/persistence/implementations/joblib_backend.py ./src/ml_toolbox/transversal/persistence/implementations/joblib_backend.py


RUN echo "Environment=${ENVIRONMENT}" \
    && python deployment/config_resolver.py --environment "${ENVIRONMENT}"

CMD ["python", "main.py"]