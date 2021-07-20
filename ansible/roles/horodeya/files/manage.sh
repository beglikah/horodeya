export DB_HOST='localhost'
export SECRET_KEY='{{secret_key}}'
export AWS_ACCESS_KEY_ID='{{aws_access_key_id}}'
export AWS_SECRET_ACCESS_KEY='{{aws_secret_access_key}}'
export AWS_DEFAULT_REGION='eu-west-1'
export ANYMAIL_WEBHOOK_SECRET='{{anymail_webhook_secret}}'
export SENDGRID_API_KEY='{{sendgrid_api_key}}'
export EPAY_KEY='{{epay_key}}'

export STREAM_API_KEY='{{stream_api_key}}'
export STREAM_API_SECRET='{{stream_api_secret}}'
export DB_PASSWORD='{{db_password}}'
export DB_NAME='{{db_name}}'
export DB_USER='{{db_user}}'

venv/bin/python manage.py $@
