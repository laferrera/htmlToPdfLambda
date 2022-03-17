# mostly from here this blog post 
# https://dev.to/bschoeneweis/converting-html-to-a-pdf-using-python-aws-lambda-and-wkhtmltopdf-3mdh
# font resources for lambda: https://github.com/brandonlim-hs/fonts-aws-lambda-layer

from datetime import datetime
import json
import logging
import os
import subprocess
import base64
from typing import Optional

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(event)
    body = json.loads(event['body'])

    try:
        html_string = body['html_string']
    except KeyError:
        html_string = None

    if html_string is None:
        error_message = (
            'Missing "html_string" '
            'from request payload.'
        )
        logger.error(error_message)
        return {
            'status': 400,
            'body': json.dumps(error_message),
        }

    # Now we can check for the option wkhtmltopdf_options and map them to values
    # Again, part of our assumptions are that these are valid
    wkhtmltopdf_options = {}
    if 'wkhtmltopdf_options' in body:
        # Margin is <top> <right> <bottom> <left>
        if 'margin' in body['wkhtmltopdf_options']:
            margins = body['wkhtmltopdf_options']['margin'].split(' ')
            if len(margins) == 4:
                wkhtmltopdf_options['margin-top'] = margins[0]
                wkhtmltopdf_options['margin-right'] = margins[1]
                wkhtmltopdf_options['margin-bottom'] = margins[2]
                wkhtmltopdf_options['margin-left'] = margins[3]

        if 'orientation' in body['wkhtmltopdf_options']:
            wkhtmltopdf_options['orientation'] = 'portrait' \
                if body['wkhtmltopdf_options']['orientation'].lower() not in ['portrait', 'landscape'] \
                else body['wkhtmltopdf_options']['orientation'].lower()

        if 'title' in body['wkhtmltopdf_options']:
            wkhtmltopdf_options['title'] = body['wkhtmltopdf_options']['title']

    # Write the HTML string to a file

    timestamp = str(datetime.now()).replace('.', '').replace(' ', '_')
    local_filename = f'/tmp/{timestamp}-html-string.html'

    # Delete any existing files with that name
    try:
        os.unlink(local_filename)
    except FileNotFoundError:
        pass

    with open(local_filename, 'w') as f:
        f.write(html_string)

    # Now we can create our command string to execute and upload the result to s3
    command = 'wkhtmltopdf  --load-error-handling ignore'  # ignore unecessary errors
    for key, value in wkhtmltopdf_options.items():
        if key == 'title':
            value = f'"{value}"'
        command += ' --{0} {1}'.format(key, value)
    command += ' {0} {1}'.format(local_filename, local_filename.replace('.html', '.pdf'))

    # Important! Remember, we said that we are assuming we're accepting valid HTML
    # this should always be checked to avoid allowing any string to be executed
    # from this command. The reason we use shell=True here is because our title
    # can be multiple words.
    subprocess.run(command, shell=True)
    logger.info('Successfully generated the PDF.')



    pdf_file = open(local_filename.replace('.html', '.pdf'), 'rb')

    return {
        'headers': {"Content-Type": "application/pdf"},
        'statusCode': 200,
        'body': base64.b64encode(pdf_file.read()).decode('utf-8'),
        'isBase64Encoded': True
    }