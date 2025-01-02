from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,  # jsonify をインポート
)
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.models import Event, Participant, User
from app import login_manager  # login_managerをインポート
from app.decorators import admin_required  # または適切なパス
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials


@bp.route("/test")
def test():
    """just for test"""
    return render_template("neon.html")


@login_manager.user_loader
def load_user(user_id):
    """
    Load user object by user ID.
    """
    return User.query.get(int(user_id))


def get_locale():
    """
    Determine the preferred language for the user.
    """
    return session.get("lang", request.accept_languages.best_match(["en", "ja"]))


@bp.route("/api/fetch_sheet_data")
def fetch_sheet_data():
    """
    Fetch data from Google Sheet.
    """
    try:
        # Use service account credentials
        gc = gspread.service_account(filename="gspread-bulk.json")
        sh = gc.open(
            "pickleball_schedule", folder_id="19sRblznzoxO2ntl3vW48x3AsXzBR_W7K"
        )
        ws = sh.worksheet("シート1")

        # Get values from A5 to F25
        values = ws.get_values("A5:F25")

        # Process the data: Skip rows that start with an empty or whitespace string
        data = [
            ", ".join(row)
            for row in values
            if row
            and row[0].strip()  # Check if first cell is non-empty and non-whitespace
        ]
        data_str = "\n".join(data)

        return jsonify({"data": data_str})

    except Exception as e:
        bp.logger.error("シートデータの取得中にエラーが発生しました: %s", str(e))
        return jsonify({"error": str(e)}), 500


@bp.route("/set-language/<lang>")
def set_language(lang):
    """
    Set the language for the session.
    """
    session["lang"] = lang
    return redirect(request.referrer or url_for("index"))


@bp.route("/view_calendar")
def view_calendar():
    """
    Just view calender for public
    """
    return render_template("view_calendar.html")


@bp.route("/")
@login_required
def index():
    """
    Main page of the application.
    """
    return render_template("index.html")


@bp.route("/events", methods=["GET"])
def get_events():
    """get event"""
    start = request.args.get("start")
    end = request.args.get("end")
    events = (
        Event.query.filter(Event.start >= start, Event.end <= end)
        .order_by(Event.start)
        .all()
    )

    if current_user.is_authenticated:  # ログイン済みの場合
        return jsonify(
            [
                {
                    "id": event.id,
                    "title": event.title,
                    "start": event.start.isoformat(),
                    "end": event.end.isoformat(),
                    "color": event.color,
                    "location": event.location,
                    "created_by": event.created_by,  # 追加情報を含む
                }
                for event in events
            ]
        )
    else:  # 未ログインの場合
        return jsonify(
            [
                {
                    "title": event.title,
                    "start": event.start.isoformat(),
                    "end": event.end.isoformat(),
                    "color": event.color,
                    "location": event.location,
                }
                for event in events
            ]
        )


@bp.route("/event", methods=["POST"])
@login_required
@admin_required
def add_or_update_event():
    """add event"""
    event_data = request.json
    if "id" in event_data:
        event = Event.query.get(event_data["id"])
        if not event:
            return jsonify({"error": "Event not found"}), 404
    else:
        event = Event(created_by=current_user.id)

    event.title = event_data["title"]
    event.start = datetime.fromisoformat(event_data["start"])
    event.end = datetime.fromisoformat(event_data["end"])
    event.location = event_data.get("location", "")
    event.color = event_data.get("color", "#3788d8")

    if "id" in event_data:
        db.session.commit()
        return jsonify({"message": "Event updated successfully"}), 200
    else:
        db.session.add(event)
        db.session.commit()
        return jsonify({"message": "Event created successfully"}), 201


@bp.route("/event/<int:id>/delete", methods=["DELETE"])
@login_required
@admin_required
def delete_event(id):
    """Deletes an event."""
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    try:
        # イベントに関連付けられた参加者を削除
        for participant in event.participants:
            db.session.delete(participant)
        # イベントを削除
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting event: {str(e)}")
        return jsonify({"error": "Failed to delete event"}), 500


@bp.route("/event/<int:id>/participants", methods=["GET", "POST"])
@login_required
def get_or_update_participants(id):
    """get or update participants"""
    event = Event.query.get(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    if request.method == "POST":
        status = request.json.get("status")
        print(f"Received status update: {status}")  # ログ出力

    if request.method == "GET":
        participants = Participant.query.filter_by(event_id=id).all()
        return jsonify(
            [
                {
                    "id": p.id,
                    "user_id": p.user_id,
                    "username": User.query.get(p.user_id).username,
                    "status": p.status,
                }
                for p in participants
            ]
        )

    elif request.method == "POST":
        status = request.json.get("status")
        if status not in ["参加", "不参加", "未定"]:
            return jsonify({"error": "Invalid status"}), 400
        participant = Participant.query.filter_by(
            event_id=id, user_id=current_user.id
        ).first()
        if participant:
            participant.status = status
        else:
            participant = Participant(
                event_id=id, user_id=current_user.id, status=status
            )
            db.session.add(participant)
        db.session.commit()
        return jsonify({"status": status}), 201


@bp.route("/event/<int:id>/participant/<int:participant_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_participant(id, participant_id):
    """delete participant"""
    participant = Participant.query.get(participant_id)
    if participant and participant.event_id == id:
        db.session.delete(participant)
        db.session.commit()
        return "", 204
    return (
        jsonify(
            {"error": "Participant not found or you do not have permission to delete"}
        ),
        404,
    )


@bp.route("/collect")
@login_required
def collect():
    """make collect list"""
    date_str = request.args.get("date")
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        events = Event.query.filter(db.func.date(Event.start) == date).all()

        for event in events:
            event.attending = [p.user for p in event.participants if p.status == "参加"]
            event.not_attending = [
                p.user for p in event.participants if p.status == "不参加"
            ]
            event.undecided = [p.user for p in event.participants if p.status == "未定"]

        return render_template("collect.html", events=events, selected_date=date)

    return render_template("collect.html", events=None, selected_date=None)


@bp.route("/admin/bulk_create_events", methods=["GET", "POST"])
@login_required
@admin_required
def bulk_create_events():
    """bulk create events"""
    if request.method == "POST":
        try:
            events_data = request.json.get("events").split("\n")
        except (KeyError, AttributeError):
            app.logger.error("リクエストデータに 'events' キーがありません")
            return jsonify({"error": "Invalid request data"}), 400
        except Exception as e:
            app.logger.error(
                f"リクエストデータの処理中にエラーが発生しました: {str(e)}"
            )
            return jsonify({"error": "Failed to process request data"}), 400

        events = []
        for event_line in events_data:
            try:
                if event_line.strip():  # 空行をスキップ
                    date, title, start_time, end_time, location, color = (
                        event_line.strip().split(",")
                    )
                    start = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
                    end = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

                    # 開始時間と終了時間の検証
                    if end <= start:
                        raise ValueError(
                            f"Invalid time range for event '{title}': End time must be after start time."
                        )

                    # 重複チェック: 同じタイトル、日時、場所のイベントがすでに存在するか
                    duplicate_event = Event.query.filter_by(
                        title=title, start=start, end=end, location=location
                    ).first()
                    if duplicate_event:
                        raise ValueError(
                            f"Duplicate event detected: An event with title '{title}' at '{location}' during '{start}' to '{end}' already exists."
                        )

                    # イベントオブジェクトの作成
                    event = Event(
                        title=title,
                        start=start,
                        end=end,
                        location=location,
                        color=color,
                        created_by=current_user.id,
                    )
                    events.append(event)
            except ValueError as e:
                app.logger.error(f"イベントデータの検証エラー: {str(e)}")
                return jsonify({"error": str(e)}), 400
            except TypeError as e:
                app.logger.error(f"イベントデータの型エラー: {str(e)}")
                return jsonify({"error": "Invalid event data type"}), 400
            except Exception as e:
                app.logger.exception(
                    f"イベントデータの処理中に予期せぬエラーが発生しました: {str(e)}"
                )  # exceptionを使うことでスタックトレースもログに出力
                return jsonify({"error": "Failed to process event data"}), 500

        try:
            # データベースに一括保存
            db.session.bulk_save_objects(events)
            db.session.commit()
            return jsonify({"message": "Events created successfully"}), 201
        except Exception as e:
            db.session.rollback()
            app.logger.exception(
                f"データベースへの保存中にエラーが発生しました: {str(e)}"
            )  # スタックトレースを出力
            return jsonify({"error": "Failed to save events to database"}), 500

    return render_template("bulk_create_events.html")
