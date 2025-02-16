from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.admin import bp
from app.models import User, Event, Participant
from app.decorators import admin_required


@bp.route("/admin")
@login_required
@admin_required
def admin_panel():
    users = User.query.all()
    return render_template("admin/admin.html", users=users)


@bp.route("/admin/toggle_admin/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_admin = not user.is_admin
        db.session.commit()
        flash(
            f'ユーザー {user.username} の管理者権限を{"付与" if user.is_admin else "削除"}しました。',
            "success",
        )
    else:
        flash("ユーザーが見つかりません。", "error")
    return redirect(url_for("admin.admin_panel"))


@bp.route("/admin/delete_user/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    """delete user"""
    user = User.query.get(user_id)
    if user:
        # ユーザーに関連付けられたイベントの参加者を削除
        for event in user.events:
            for participant in event.participants:
                if participant.user_id == user_id:
                    db.session.delete(participant)
        # ユーザーを削除
        db.session.delete(user)
        db.session.commit()
        flash(f"ユーザー {user.username} を削除しました。", "success")
    else:
        flash("ユーザーが見つかりません。", "error")
    return redirect(url_for("admin_panel"))
