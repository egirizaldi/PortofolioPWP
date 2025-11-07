from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os

# --- KONFIGURASI TAMBAHAN ---
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# -----------------------------

app = Flask(__name__)
app.secret_key = "!@#$%"
app.config["UPLOAD_FOLDER"] = 'static/upload'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'portofolio'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()

    # Ambil skill
    cur.execute("SELECT * FROM skills")
    skills = cur.fetchall()

    # Ambil project
    cur.execute("SELECT * FROM projects")
    projects = cur.fetchall()

    
    cur.execute("SELECT name, bio, photo FROM users LIMIT 1")
    user = cur.fetchone()

    cur.close()

    return render_template(
        'index.html',
        skills=skills,
        projects=projects,
        user=user  
    )
@app.route('/login',methods =['GET','POST'])
def login():
    if request.method == 'POST' and 'inpUsername' in request.form and 'inpPass' in request.form:
        username = request.form['inpUsername']
        password = request.form['inpPass']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users where username = %s and password = %s", (username, password)) 

        result = cur.fetchone()
    
        if result:
            session['is_logged_in'] = True
            session['username'] = result[1]

            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Username atau password salah.')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('is_logged_in',None) 
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'is_logged_in' in session and session['is_logged_in']:
        cur = mysql.connection.cursor()

        
        cur.execute("SELECT * FROM users WHERE username=%s", [session['username']])
        user = cur.fetchone()

        
        cur.execute("SELECT * FROM skills")
        skills = cur.fetchall()

        
        cur.execute("SELECT * FROM projects")
        projects = cur.fetchall()

        cur.close()

        return render_template(
            "dashboard.html",
            username=session['username'],
            user=user,           # ⬅ kirim data user ke dashboard.html
            skills=skills,
            projects=projects
        )
    else:
        return redirect(url_for("login"))
@app.route('/api/bio', methods=['POST'])
def update_bio():
    if 'is_logged_in' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    name = request.form.get("name")
    bio = request.form.get("bio")
    photo = request.files.get("photo")

    username = session.get("username")

    if not name or not bio:
        return jsonify({"error": "Nama dan bio wajib diisi"}), 400

    cur = mysql.connection.cursor()

    # Jika upload foto baru
    if photo and photo.filename != "":
        if not allowed_file(photo.filename):
            return jsonify({"error": "Format file foto tidak diizinkan"}), 400

        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        # Update dengan foto baru
        cur.execute("""
            UPDATE users SET name=%s, bio=%s, photo=%s WHERE username=%s
        """, (name, bio, filename, username))

    else:
        # Update tanpa ganti foto
        cur.execute("""
            UPDATE users SET name=%s, bio=%s WHERE username=%s
        """, (name, bio, username))

    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Bio berhasil diperbarui!"})

    
@app.route('/api/skills',methods = ['POST'])
def add_skills():
    name = request.form.get('name')
    level = request.form.get('level')
    icon = request.files.get('icon') 

    if not name or not level or not icon or icon.filename == '':
        return jsonify({'Error': 'Semua fields wajib diisi dan icon harus diunggah.'}), 400
    
    if not allowed_file(icon.filename):
        return jsonify({'Error': 'Format file icon tidak diizinkan.'}), 400
        
    filename = secure_filename(icon.filename)
    icon.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO skills (name, level, icon) VALUES (%s, %s, %s)",(name, level, filename))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'Skill berhasil ditambahkan'}), 201

@app.route('/api/skills/<int:id>', methods=['PUT'])
def update_skill(id):
    name = request.form.get('name')
    level = request.form.get('level')
    icon = request.files.get('icon')

    cur = mysql.connection.cursor()
    
    # Ambil nama file lama (jika ada file baru diunggah, file lama akan dihapus)
    old_icon = None
    if icon and icon.filename != '':
        cur.execute("SELECT icon FROM skills WHERE id = %s", [id])
        result = cur.fetchone()
        if result:
            old_icon = result[0]
            
        if not allowed_file(icon.filename):
            return jsonify({'Error': 'Format file icon baru tidak diizinkan.'}), 400
            
        filename = secure_filename(icon.filename)
        icon.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Hapus file lama jika ada
        if old_icon:
            old_path = os.path.join(app.config['UPLOAD_FOLDER'], old_icon)
            if os.path.exists(old_path):
                os.remove(old_path)
                
        # Update dengan icon baru
        cur.execute("UPDATE skills SET name=%s, level=%s, icon=%s WHERE id=%s",
                    (name, level, filename, id))
    else:
        # Update tanpa icon baru
        cur.execute("UPDATE skills SET name=%s, level=%s WHERE id=%s",
                    (name, level, id))

    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Skill berhasil diperbarui!'})

@app.route('/api/skills/<int:id>', methods=['DELETE'])
def delete_skill(id):
    cur = mysql.connection.cursor()
    # Ambil nama file icon sebelum dihapus dari database
    cur.execute("SELECT icon FROM skills WHERE id = %s", [id])
    result = cur.fetchone()
    
    cur.execute("DELETE FROM skills WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    
    # Hapus file dari server
    if result and result[0]:
        filename = result[0]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
    return jsonify({'message': 'Skill berhasil dihapus!'})

#Route untuk Dashboard Project

@app.route('/api/projects', methods=['POST'])
def add_projects():
    title = request.form.get('title')
    description = request.form.get('description')
    image = request.files.get('image')
    link = request.form.get('link')

    if not title or not description or not image or image.filename == '' or not link:
        return jsonify({'Error': 'Semua fields wajib diisi dan image harus diunggah'}), 400

    if not allowed_file(image.filename):
        return jsonify({'Error': 'Format file tidak diizinkan'}), 400

    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO projects (title, description, image, link) VALUES (%s, %s, %s, %s)",
        (title, description, filename, link)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Project berhasil ditambahkan'}), 201
@app.route('/api/projects/<int:id>', methods=['PUT'])
def update_project(id):
    title = request.form.get('title')
    description = request.form.get('description')
    image = request.files.get('image')
    link =  request.form.get('link')

    cur = mysql.connection.cursor()

    old_image = None
    if image and image.filename != '':
        cur.execute("SELECT image FROM projects WHERE id = %s ",[id])
        result = cur.fetchone()
        if result:
            old_image = result[0]

        if not allowed_file(image.filename):
            return jsonify({'Error' : 'Format file icon baru tidak diizinkan.'}),400
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        if old_image:
            old_path = os.path.join(app.config['UPLOAD_FOLDER'],old_image)
            if os.path.exists(old_path):
                os.remove(old_path)
        
        cur.execute("UPDATE projects SET title=%s,description = %s,image=%s,link=%s WHERE id=%s",(title,description,filename,link,id))
    else:
        cur.execute("UPDATE projects SET title=%s,description = %s,link=%s WHERE id=%s",(title,description,link,id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'project berhasil diperbarui'})

@app.route('/api/projects/<int:id>', methods=['DELETE'])
def delete_projects(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT image FROM projects WHERE id = %s",[id])
    result = cur.fetchone()

    cur.execute("DELETE FROM projects WHERE id = %s",[id])
    mysql.connection.commit()
    cur.close()

    if result and result[0]:
        filename = result[0]
        file_path = os.path.join(app.config["UPLOAD_FOLDER"],filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    return jsonify({'message':'Pojects beerhasil dihapus!'})
        

        
        

if __name__ == '__main__':
    # Pastikan direktori upload ada
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)