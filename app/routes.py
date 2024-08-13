from datetime import datetime
from app import app, db, load_user
from app.models import User
from flask import flash, render_template, redirect, session, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
import bcrypt

@app.route('/')
def index():
    return render_template('index.html')