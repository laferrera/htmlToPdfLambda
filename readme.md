
this is the Lambda Function ARN
arn:aws:lambda:us-east-1:557236342652:function:convertHtmlToPdf

here's a link to the editor for Jason's Personal AWS Acct Lambda Function
https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/htmlToPdfPython?tab=code


original medium article
https://medium.com/1mgofficial/pdf-generation-with-aws-lambda-627b8dd07c77


resources for fonts
https://github.com/brandonlim-hs/fonts-aws-lambda-layer

resources for wkhtmltopdf binary
https://wkhtmltopdf.org/downloads.html#stable

you can try things out locally by installing wkhtmltopdf locally
`brew install wkhtmltopdf`
and then 
`wkhtmltopdf test.html output.pdf`

but to hit my lambda function you'll just need to do a JSON post

this works!
curl -X POST https://4o2gpjutlg.execute-api.us-east-1.amazonaws.com/default/htmlToPdfPython -H 'Content-Type: application/json' -d '{"html_string" : "<html>hello,world</html>"}' > test.pdf

this works with an image
curl -X POST https://4o2gpjutlg.execute-api.us-east-1.amazonaws.com/default/htmlToPdfPython -H 'Content-Type: application/json' -d '{"html_string" : "<html><head><body><p>hello, world</p><img src=\"https://image.roku.com/developer_channels/prod/c0dda8886e121608052fb46c4cbfd3568880a1917c4cfbea8de48c82cef3c3a1.png\" style=\"width: 290px; height: 218px\"></body><html>"}' > test.pdf
