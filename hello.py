from flask import Flask, request, jsonify, abort, redirect, url_for, render_template, send_file
import joblib
import numpy as np
import os
import pandas as pd

app = Flask(__name__)
#загружаем сохраненную модель
knn = joblib.load('knn.pkl') 

@app.route("/") # в кавычках маршрут? по которому выполняется функция
def my_hello_world():
    print(1+2)
    print(1+6/3+100000000)
    #print('hi!')
    return "<h>Hello, my  best friend!</h>"


##добавим переменную
@app.route('/user/<username>') #декоратор для подхода функции к flask'у
def show_user_profile1(username):
    try:
        username = float(username)**2
    except:
        pass
    # show the user profile for that user
    return 'User %s' %username

def mean1(numbers):
    return float(sum(numbers))/len(numbers)

@app.route('/avg/<nums>')
def avg1(nums):
    nums = nums.split(',')
    nums = [float(num) for num in nums]
    nums_mean = mean1(nums)
    print(nums)
    return str(nums_mean)

@app.route('/iris')
def iris1():
    import numpy as np
    #import sklearn
    import sklearn

    from sklearn.datasets import load_iris
    #from sklearn import datasets
    
    iris = load_iris()
    iris_X = iris.data
    iris_y = iris.target
    np.unique(iris_y)
    
    np.random.seed(0)
    indices = np.random.permutation(len(iris_X))
    iris_X_train = iris_X[indices[:-10]]
    iris_y_train = iris_y[indices[:-10]]
    iris_X_test = iris_X[indices[-10:]]
    iris_y_test = iris_y[indices[-10:]]
    #return str(np.unique(iris_y))
    
    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier()
    knn.fit(iris_X_train, iris_y_train)
    KNeighborsClassifier(algorithm='auto',
                         leaf_size=30,
                         metric='minkowski',
                         metric_params=None,
                         n_jobs=1,
                         n_neighbors=5,
                         p=2,
                         weights='uniform')
    predictions = knn.predict(iris_X_test)
    
    return str(predictions), str(np.unique(iris_y))
                      
@app.route('/iris/<param>')
def iris2(param):
    
    '''
    import numpy as np
    #import sklearn
    import sklearn

    from sklearn.datasets import load_iris
    '''
    param = param.split(',')
    param = [float(num) for num in param]
    print(param)
    '''
    iris = load_iris()
    iris_X = iris.data
    iris_y = iris.target
    np.unique(iris_y)
    
    np.random.seed(0)
    indices = np.random.permutation(len(iris_X))
    iris_X_train = iris_X[indices[:-10]]
    iris_y_train = iris_y[indices[:-10]]
    iris_X_test = iris_X[indices[-10:]]
    iris_y_test = iris_y[indices[-10:]]
    #return str(np.unique(iris_y))
    
    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier()
    knn.fit(iris_X_train, iris_y_train)
    
    KNeighborsClassifier(algorithm='auto',
                         leaf_size=30,
                         metric='minkowski',
                         metric_params=None,
                         n_jobs=1,
                         n_neighbors=5,
                         p=2,
                         weights='uniform')
    '''
 
    
    param = np.array(param).reshape(1, -1)
    predictions = knn.predict(param)
    
    return str(predictions)

#  страница на случай ошибки
@app.route('/badrequest400')
def bad_request():
    return abort(400)


# показывает изображения предсказанных ирисов
@app.route('/show_image')
def show_image():
    #return '<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Iris_versicolor_3.jpg" alt="alternatetext">'
    #return '<p><a href="/static/setosa.jpg"> </a><</p>'
    #return '<p><a href="https://commons.wikimedia.org/wiki/File:Iris_versicolor_3.jpg#/media/File:Iris_versicolor_3.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/4/41/Iris_versicolor_3.jpg" alt="Iris versicolor 3.jpg" height="1488" width="1984"></a><br>By No machine-readable author provided. <a href="//commons.wikimedia.org/wiki/User:Dlanglois" title="User:Dlanglois">Dlanglois</a> assumed (based on copyright claims). - No machine-readable source provided. Own work assumed (based on copyright claims)., <a href="http://creativecommons.org/licenses/by-sa/3.0/" title="Creative Commons Attribution-Share Alike 3.0">CC BY-SA 3.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=248095">Link</a></p>'
    #return 'return '<p><a href="/static/setosa.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/4/41/Iris_versicolor_3.jpg" alt="Iris versicolor 3.jpg" height="1488" width="1984"></a><br>By No machine-readable author provided. <a href="//commons.wikimedia.org/wiki/User:Dlanglois" title="User:Dlanglois">Dlanglois</a> assumed (based on copyright claims). - No machine-readable source provided. Own work assumed (based on copyright claims)., <a href="http://creativecommons.org/licenses/by-sa/3.0/" title="Creative Commons Attribution-Share Alike 3.0">CC BY-SA 3.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=248095">Link</a></p>''
    return '<img src="/static/setosa.jpg" alt="User Image">'

#пост-запрос
@app.route('/iris_post',methods=['POST', 'GET'])
def add_message():
    try:
        content = request.get_json() #словарь
        
        param = content['flower'].split(',')
        param = [float(num) for num in param]
        
        param = np.array(param).reshape(1, -1)
        predictions = knn.predict(param)
        
        predictions = {'class':str(predictions[0])}
    except:
        return redirect(url_for('bad_request'))

    return jsonify(predictions) #на POST-запрос возвращаем json-файл

    # web-форма с помощью Flask WTF
    #работа с файлом с помощтю wtf
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired

#загрузка файла
from werkzeug.utils import secure_filename

# секретный ключ для защиты
# иначе появляется ошибка (CSRF)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secrer key"
))

class MyForm(FlaskForm):
    #запрос имени
    name = StringField('name', validators=[DataRequired()])
    #загрузка файла
    file = FileField()
    
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        #после запроса имени
        #return('form_submited')
        #return str(form.name)
        # переход на другую страницу после ввода имени
        #return redirect('/show_image')
        
        # работа с файлом
        f = form.file.data
        
        #загрузка файла
        filename = str(form.name.data)+'.csv'
        #f.save(os.path.join(
            #app.instance_path, 'files', filename
        #    filename
        #))
        #return redirect(url_for('index'))
        
        #работа с csv 
        # чтение из открытого файла f
        df = pd.read_csv(f, header=None)
        print(df.head())
        #предсказание по данным из таблицы
        predict = knn.predict(df)
        print(str(predict))
        
        # сохранение предсказаний в s csv
        result =pd.DataFrame(predict)
        result.to_csv(filename, index=False)
        
        #return('file uploaded'+ '  predictions: ' + str(predict))
        
    
        
        #return(str(form.name))
        
        #возрат файла с результатами
        return send_file(filename,
                        mimetype='text/csv',
                        #attachment_filename=filename,
                        download_name=filename,
                        as_attachment=True)
    return render_template('submit.html', form=form)
                                   
# загрузка файла с POST-запросом
# более простая форма загрузки файла без secret code
# проверяется с помощью Postman
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename+'uploaded')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file uploaded'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
                               