from flask import Flask, request, redirect, render_template, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from code_modes import generate_code, MODES
from config import Config
from models import db, Link

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Admin credentials
ADMIN_USER = Config.USER
ADMIN_PASS_HASH = generate_password_hash(Config.PASSWORD)

@app.route('/')
def index():
    if 'user' in session:
        links = Link.query.order_by(Link.created_at.desc()).all()
        return render_template('dashboard.html', links=links, modes=MODES, domain=request.host)
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username')
    pw = request.form.get('password')
    if user == ADMIN_USER and pw and check_password_hash(ADMIN_PASS_HASH, pw):
        session['user'] = user
        return redirect(url_for('index'))
    flash('Invalid credentials')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/shorten', methods=['POST'])
def shorten():
    if 'user' not in session:
        return redirect(url_for('index'))
    url = request.form.get('url')
    mode = request.form.get('mode', 'xd')
    
    # Generate unique code
    code = generate_code(mode)
    while Link.query.filter_by(code=code).first():
        code = generate_code(mode)
    
    # Create new link
    link = Link(code=code, url=url, mode=mode)
    db.session.add(link)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:link_id>', methods=['POST'])
def delete_link(link_id):
    if 'user' not in session:
        return redirect(url_for('index'))
    
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('Link deleted successfully')
    return redirect(url_for('index'))

@app.route('/stats')
def stats():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    total_links = Link.query.count()
    total_clicks = db.session.query(db.func.sum(Link.click_count)).scalar() or 0
    top_links = Link.query.order_by(Link.click_count.desc()).limit(10).all()
    
    return render_template('stats.html', 
                         total_links=total_links, 
                         total_clicks=total_clicks,
                         top_links=top_links,
                         domain=request.host)

@app.route('/<code>')
def redirect_code(code):
    link = Link.query.filter_by(code=code).first()
    if link:
        # Increment click counter
        link.click_count += 1
        db.session.commit()
        return redirect(link.url)
    return 'Link not found', 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
