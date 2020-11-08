from flask import Flask, render_template, request, jsonify
import smtplib
import query_on_whoosh
import config
import math
#
app=Flask(__name__)
app.config.update(dict(JSONIFY_PRETTYPRINT_REGULAR=True))
#
#@app.route("/")
#def handle_slash():
    #requested_name = request.args.get("name")
    #return render_template("index.html", user_name=requested_name)

#@app.route("/test")
#def handle_tset():
    #input="abc"
    #return test_module.test(input)

@app.route("/query", strict_slashes=False)
def handle_query():
    search_term = request.args.get("q")
    n = int(request.args.get('p'))
    return jsonify(query_on_whoosh.query(search_term, current_page=n))

@app.route("/query_view", strict_slashes=False)
def handle_query_view():
    search_term = request.args.get("q")
    if not search_term:
        search_term=""

    page_index_arg = request.args.get("p")
    if not page_index_arg:
        page_index_arg = "1"
    page_index = int(page_index_arg)
    query_results = query_on_whoosh.query(search_term, current_page = page_index)
    search_results = query_results[0] #return a page of the search results
    results_cnt = int(query_results[1]) # return a total number of the search results
    page_cnt = math.ceil(results_cnt / 10)
    return render_template("query.html", 
                            results = search_results, 
                            page_cnt=page_cnt,
                            search_term = search_term)

@app.route("/about", strict_slashes=False)
def handle_about():
    return render_template("about.html")

@app.route("/success", strict_slashes=False)
def handle_request():
    new_data = request.args.get("new_data")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("juhiipatel.13@gmail.com",config.gmail_password)
    message = 'Subject: {}\n\n{}'.format("Request to add new data", "requestto add:" + new_data)
    server.sendmail("juhiipatel.13@gmail.com", "jpatel18@emich.edu", message)

    return render_template("success.html", new_data=new_data)
