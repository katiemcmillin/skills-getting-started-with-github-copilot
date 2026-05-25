from src.app import activities


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_shape(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload

    chess = payload["Chess Club"]
    assert "description" in chess
    assert "schedule" in chess
    assert "max_participants" in chess
    assert "participants" in chess
    assert isinstance(chess["participants"], list)


def test_signup_adds_participant(client):
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_signup_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_returns_400(client):
    email = activities["Chess Club"]["participants"][0]

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_removes_participant(client):
    email = activities["Programming Class"]["participants"][0]

    response = client.delete(f"/activities/Programming Class/signup?email={email}")

    assert response.status_code == 200
    assert email not in activities["Programming Class"]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete("/activities/Unknown Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_not_registered_returns_404(client):
    email = "not-signed-up@mergington.edu"

    response = client.delete(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"
