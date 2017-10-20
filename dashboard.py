from flask import Flask,render_template,request
from utils import ConnectJira

#Create an instance of the Flask class
app = Flask(__name__)

@app.route('/dashboard/')
def dashboard():
    "The dashboard page"

   return render_template('dashboard.html')


@app.route('/results/',methods=['GET','POST'])
def results():
    "The results page"
    if request.method == 'POST':
        #Get the keys and values from the form object
        result = request.form
        jira_url = result['jira-url']
        user_name = result['user-name']
        password = result['passwd']
        project = result['project-name']
        no_of_days = result['no-of-days']
        #Create an instance of ConnectJira class
        jira_obj = ConnectJira(server=jira_url,project_name=project,no_of_days=no_of_days,username=user_name,password=password)
        jira_obj.get_description_reporters_data_frame()
        jira_obj.get_comments()

        return render_template('results.html',result=result)


if __name__ == '__main__':
    #run the app
    app.run(host='127.0.0.1',port=5000)