"""
Tests for the Session Store and Query Cache.
Covers: CRUD, TTL expiry, LRU eviction, thread safety, cache operations.
"""

import time
import pytest
from datetime import datetime, timedelta

from app.services.session_store import SessionStore, QueryCache, sessions_store


class TestSessionStore:
    """Unit tests for the in-memory SessionStore."""

    def setup_method(self):
        self.store = SessionStore(max_sessions=5, ttl_minutes=1)

    def test_create_session(self):
        data = self.store.create("s1", {"file": "report.pdf"})
        assert "created_at" in data
        assert "updated_at" in data
        assert data["file"] == "report.pdf"

    def test_get_existing_session(self):
        self.store.create("s1", {"status": "pending"})
        session = self.store.get("s1")
        assert session is not None
        assert session["status"] == "pending"

    def test_get_nonexistent_session(self):
        assert self.store.get("nonexistent") is None

    def test_update_session(self):
        self.store.create("s1", {"status": "pending"})
        updated = self.store.update("s1", {"status": "completed"})
        assert updated is not None
        assert updated["status"] == "completed"
        assert "updated_at" in updated

    def test_update_nonexistent_returns_none(self):
        result = self.store.update("missing", {"data": "value"})
        assert result is None

    def test_delete_session(self):
        self.store.create("s1", {"data": "test"})
        assert self.store.delete("s1") is True
        assert self.store.get("s1") is None

    def test_delete_nonexistent_returns_false(self):
        assert self.store.delete("missing") is False

    def test_max_sessions_eviction(self):
        """When max_sessions is reached, the oldest session should be evicted."""
        for i in range(6):  # max is 5
            self.store.create(f"s{i}", {"idx": i})
        # s0 should have been evicted
        assert self.store.get("s0") is None
        # s5 should exist
        assert self.store.get("s5") is not None

    def test_ttl_expiry(self):
        """Sessions older than TTL should be cleaned up."""
        store = SessionStore(max_sessions=10, ttl_minutes=0)  # 0 min TTL
        store.create("s1", {"data": "test"})
        # Manually expire it
        store._store["s1"]["updated_at"] = datetime.now() - timedelta(minutes=1)
        assert store.get("s1") is None

    def test_lru_ordering(self):
        """Accessing a session should move it to the end (most recently used)."""
        self.store.create("s1", {"data": "first"})
        self.store.create("s2", {"data": "second"})
        self.store.create("s3", {"data": "third"})
        # Access s1 → moves to end
        self.store.get("s1")
        # The internal order should now be: s2, s3, s1
        keys = list(self.store._store.keys())
        assert keys[-1] == "s1"

    def test_concurrent_access_safety(self):
        """Basic check that the lock doesn't deadlock on sequential ops."""
        self.store.create("s1", {"data": "a"})
        self.store.update("s1", {"data": "b"})
        assert self.store.get("s1")["data"] == "b"
        self.store.delete("s1")
        assert self.store.get("s1") is None


class TestQueryCache:
    """Unit tests for the QueryCache."""

    def setup_method(self):
        self.cache = QueryCache(max_entries=3, ttl_seconds=2)

    def test_set_and_get(self):
        self.cache.set("hello world", "en", {"result": "cached"})
        result = self.cache.get("hello world", "en")
        assert result is not None
        assert result["result"] == "cached"

    def test_get_miss(self):
        assert self.cache.get("not cached", "en") is None

    def test_different_languages_different_keys(self):
        self.cache.set("same text", "en", {"lang": "en"})
        self.cache.set("same text", "hi", {"lang": "hi"})
        assert self.cache.get("same text", "en")["lang"] == "en"
        assert self.cache.get("same text", "hi")["lang"] == "hi"

    def test_ttl_expiry(self):
        cache = QueryCache(max_entries=10, ttl_seconds=0)  # immediate expiry
        cache.set("test", "en", {"data": "value"})
        # Force time-based expiry by setting timestamp in the past
        key = cache._make_key("test", "en")
        cache._cache[key]["timestamp"] = time.time() - 1
        assert cache.get("test", "en") is None

    def test_max_entries_eviction(self):
        self.cache.set("a", "en", {"v": 1})
        self.cache.set("b", "en", {"v": 2})
        self.cache.set("c", "en", {"v": 3})
        self.cache.set("d", "en", {"v": 4})  # should evict "a"
        assert self.cache.get("a", "en") is None
        assert self.cache.get("d", "en")["v"] == 4

    def test_invalidate(self):
        self.cache.set("test", "en", {"data": "value"})
        self.cache.invalidate("test", "en")
        assert self.cache.get("test", "en") is None

    def test_invalidate_nonexistent(self):
        # Should not raise
        self.cache.invalidate("nothing", "en")

    def test_key_deterministic(self):
        k1 = QueryCache._make_key("text", "en")
        k2 = QueryCache._make_key("text", "en")
        assert k1 == k2

    def test_key_different_for_different_inputs(self):
        k1 = QueryCache._make_key("text1", "en")
        k2 = QueryCache._make_key("text2", "en")
        assert k1 != k2


class TestGlobalInstances:
    """Ensure global singletons are properly initialized."""

    def test_sessions_store_exists(self):
        assert sessions_store is not None
        assert isinstance(sessions_store, SessionStore)
