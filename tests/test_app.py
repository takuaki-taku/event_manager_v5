def test_view_calendar(client):
    """/view_calendarへのリクエストが200 OKで応答し、カレンダー関連のコンテンツを含むことを確認"""
    response = client.get("/view_calendar")
    assert response.status_code == 200
    assert (
        b"calendar" in response.data
    )  # レスポンスボディに"calendar"が含まれることを確認
