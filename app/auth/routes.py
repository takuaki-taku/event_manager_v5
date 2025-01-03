from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.auth import bp
from app.models import User


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if isinstance(user, User) and user.check_password(password):
            login_user(user)
            flash("ログインしました。", "success")
            return redirect(url_for("main.index"))
        else:
            flash("ユーザー名またはパスワードが間違っています。", "error")
    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました。", "success")
    return redirect(url_for("auth.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user:
            flash("このユーザー名はすでに使用されています。", "error")
            return redirect(url_for("auth.register"))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("登録が完了しました。", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")
