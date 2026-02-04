# Use AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11

# Install Playwright dependencies
RUN yum install -y \
    atk \
    cups-libs \
    gtk3 \
    libXcomposite \
    alsa-lib \
    libXcursor \
    libXdamage \
    libXext \
    libXi \
    libXrandr \
    libXScrnSaver \
    libXtst \
    pango \
    at-spi2-atk \
    libXt \
    xorg-x11-server-Xvfb \
    xorg-x11-xauth \
    dbus-glib \
    dbus-glib-devel \
    nss \
    mesa-libgbm

# Copy requirements and install Python dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip3 install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Install Playwright browsers
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy application code
COPY *.py ${LAMBDA_TASK_ROOT}/

# Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]
