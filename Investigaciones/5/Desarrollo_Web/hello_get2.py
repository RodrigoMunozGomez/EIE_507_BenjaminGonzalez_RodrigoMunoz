#!/usr/bin/env python3
import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()

first_name = form.getvalue('first_name')
last_name = form.getvalue('last_name')
age = form.getvalue('age')

print("Content-Type: text/html;charset=utf-8")
print("Content-type:text/html\r\n")
print("<!DOCTYPE html>")
print("<html lang='en'>")
print("<head>")
print("<title>Hello - get CGI Program</title>")
print("</head>")
print("<body>")
print("<h2>Hello %s %s de edad %s</h2>" % (first_name, last_name, age))
print("</body>")
print("</html>")