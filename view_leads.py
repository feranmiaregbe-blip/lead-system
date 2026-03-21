from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
@app.route("/leads")
def view_leads():
    file = open("leads.txt", "r")
    leads = file.readlines()
    file.close()

    output = "<h2>Saved Leads</h2>"
    output += "<a href='/'>Add New Lead</a><br><br>"

    if len(leads) == 0:
        output += "No leads yet"
    else:
        for lead in leads:
            output += lead + "<br>"

    return output