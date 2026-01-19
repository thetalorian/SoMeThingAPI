from fastapi.testclient import TestClient

from app.api.v1.post import get_post_service
from app.main import app
from app.db.schema import User
from app.models.post import PostCreate
from app.services.post_service import PostService
from tests.test_db import TestingSessionLocal

# Setup the TestClient
client = TestClient(app)

# Dependency to override the get_db dependency in the main app
def override_get_post_service():
    session = TestingSessionLocal()
    yield PostService(session=session)

app.dependency_overrides[get_post_service] = override_get_post_service

def test_create_and_get_post(default_user: User):
    # Create a new post
    response = client.post("/api/v1/posts", json={"title": "Test Post", "content": "This is a test post", "published": True})
    assert response.status_code == 200
    created_post = response.json()
    assert created_post["title"] == "Test Post"
    assert "id" in created_post

    # Fetch the created post
    get_response = client.get(f"/api/v1/posts/{created_post['id']}")
    assert get_response.status_code == 200
    fetched_post = get_response.json()
    assert fetched_post["id"] == created_post["id"]
    assert fetched_post["title"] == created_post["title"]

def test_get_nonexistent_post():
    response = client.get("/api/v1/posts/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}

def test_list_posts():
    # Ensure there is at least one post
    response = client.post("/api/v1/posts", json={"title": "Another Post", "content": "Another post content", "published": True})
    posts = client.get("/api/v1/posts")
    assert posts.status_code == 200
    assert len(posts.json()) >= 1

def test_update_post():
    # Create a new post to update
    response = client.post("/api/v1/posts", json={"title": "Update Post", "content": "Update post content", "published": True})
    created_post = response.json()
    post_id = created_post["id"]
    # Update the post's title
    update_response = client.put(f"/api/v1/posts/{post_id}", json={"title": "Updated Title", "content": "Updated post content", "published": False})
    assert update_response.status_code == 200
    updated_post = update_response.json()
    assert updated_post["title"] == "Updated Title"


def test_update_nonexistent_post():
    update_response = client.put("/api/v1/posts/9999", json={"title": "Nonexistent Post", "content": "No content", "published": False})
    assert update_response.status_code == 404
    assert update_response.json() == {"detail": "Post not found"}


def test_unauthorized_update_post():
    # Create a new post via service with a different user_id
    service = PostService(session=TestingSessionLocal())
    post_data = PostCreate(title="Auth Post", content="Auth post content", published=True)
    created_post = service.create_post(post=post_data, user_id=2)
    post_id = created_post.id
    # API Currently defaults to user_id=1, so this should raise Unauthorized
    update_response = client.put(f"/api/v1/posts/{post_id}", json={"title": "Hacked Title", "content": "Hacked content", "published": False})
    assert update_response.status_code == 403
    assert update_response.json() == {"detail": "Unauthorized to update this post"}

def test_delete_post():
    # Create a new post to delete
    response = client.post("/api/v1/posts", json={"title": "Delete Post", "content": "Delete post content", "published": True})
    created_post = response.json()
    post_id = created_post["id"]
    # Delete the post
    delete_response = client.delete(f"/api/v1/posts/{post_id}")
    assert delete_response.status_code == 200
    # Verify the post is deleted
    get_response = client.get(f"/api/v1/posts/{post_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Post not found"}


def test_delete_nonexistent_post():
    delete_response = client.delete("/api/v1/posts/9999")
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "Post not found"}


def test_unauthorized_delete_post():
    # Create a new post via service with a different user_id
    service = PostService(session=TestingSessionLocal())
    post_data = PostCreate(title="Auth Delete Post", content="Auth delete post content", published=True)
    created_post = service.create_post(post=post_data, user_id=2)
    post_id = created_post.id
    # API Currently defaults to user_id=1, so this should raise Unauthorized
    delete_response = client.delete(f"/api/v1/posts/{post_id}")
    assert delete_response.status_code == 403
    assert delete_response.json() == {"detail": "Unauthorized to update this post"}
