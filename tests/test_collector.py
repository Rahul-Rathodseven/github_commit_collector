"""
Unit Tests for GitHub Commit Data Collector
Run with: pytest tests/
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from team_mapper import TeamMapper
from models import CommitData, FileChange, RepositoryStats
from commit_processor import CommitProcessor


class TestTeamMapper(unittest.TestCase):
    """Test TeamMapper functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.team_config = {
            "teams": {
                "backend": ["alice", "bob"],
                "frontend": ["charlie"]
            },
            "default_team": "unassigned"
        }
        self.mapper = TeamMapper(self.team_config)
    
    def test_get_team_known_user(self):
        """Test mapping known user to team."""
        team = self.mapper.get_team("alice")
        self.assertEqual(team, "backend")
    
    def test_get_team_unknown_user(self):
        """Test mapping unknown user to default team."""
        team = self.mapper.get_team("unknown")
        self.assertEqual(team, "unassigned")
    
    def test_get_team_none_user(self):
        """Test mapping None user to default team."""
        team = self.mapper.get_team(None)
        self.assertEqual(team, "unassigned")
    
    def test_get_team_case_insensitive(self):
        """Test that username mapping is case-insensitive."""
        team = self.mapper.get_team("ALICE")
        self.assertEqual(team, "backend")
    
    def test_get_all_teams(self):
        """Test getting all teams."""
        teams = self.mapper.get_all_teams()
        self.assertIn("backend", teams)
        self.assertIn("frontend", teams)
        self.assertIn("unassigned", teams)
    
    def test_get_team_members(self):
        """Test getting team members."""
        members = self.mapper.get_team_members("backend")
        self.assertEqual(len(members), 2)
        self.assertIn("alice", members)
        self.assertIn("bob", members)
    
    def test_add_mapping(self):
        """Test dynamically adding a mapping."""
        self.mapper.add_mapping("diana", "frontend")
        team = self.mapper.get_team("diana")
        self.assertEqual(team, "frontend")


class TestModels(unittest.TestCase):
    """Test data models."""
    
    def test_file_change_creation(self):
        """Test FileChange model creation."""
        fc = FileChange(
            filename="test.py",
            status="modified",
            additions=10,
            deletions=5,
            changes=15
        )
        self.assertEqual(fc.filename, "test.py")
        self.assertEqual(fc.status, "modified")
        self.assertEqual(fc.additions, 10)
    
    def test_file_change_to_dict(self):
        """Test FileChange to_dict conversion."""
        fc = FileChange(
            filename="test.py",
            status="modified",
            additions=10,
            deletions=5,
            changes=15
        )
        fc_dict = fc.to_dict()
        self.assertIsInstance(fc_dict, dict)
        self.assertEqual(fc_dict["filename"], "test.py")
    
    def test_commit_data_creation(self):
        """Test CommitData model creation."""
        commit = CommitData(
            repository_name="test-repo",
            repository_owner="test-owner",
            repository_url="https://github.com/test-owner/test-repo",
            commit_sha="abc123",
            commit_message="Test commit",
            commit_date=datetime.now(),
            commit_url="https://github.com/test-owner/test-repo/commit/abc123",
            author_name="Test Author",
            author_username="testuser",
            author_email="test@example.com",
            team_name="backend",
            total_additions=10,
            total_deletions=5,
            total_changes=15,
            files_changed_count=2,
            branch="main"
        )
        self.assertEqual(commit.repository_name, "test-repo")
        self.assertEqual(commit.team_name, "backend")
    
    def test_commit_data_to_dict(self):
        """Test CommitData to_dict conversion."""
        commit = CommitData(
            repository_name="test-repo",
            repository_owner="test-owner",
            repository_url="https://github.com/test-owner/test-repo",
            commit_sha="abc123",
            commit_message="Test commit",
            commit_date=datetime.now(),
            commit_url="https://github.com/test-owner/test-repo/commit/abc123",
            author_name="Test Author",
            author_username="testuser",
            author_email="test@example.com",
            team_name="backend",
            total_additions=10,
            total_deletions=5,
            total_changes=15,
            files_changed_count=2,
            branch="main"
        )
        commit_dict = commit.to_dict()
        self.assertIsInstance(commit_dict, dict)
        self.assertIn("repository", commit_dict)
        self.assertIn("commit", commit_dict)
        self.assertIn("author", commit_dict)


class TestCommitProcessor(unittest.TestCase):
    """Test CommitProcessor functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        team_config = {
            "teams": {"backend": ["alice"]},
            "default_team": "unassigned"
        }
        self.mapper = TeamMapper(team_config)
        self.processor = CommitProcessor(self.mapper)
    
    def test_process_file_changes(self):
        """Test processing file changes."""
        files_data = [
            {
                "filename": "test.py",
                "status": "modified",
                "additions": 10,
                "deletions": 5,
                "changes": 15
            }
        ]
        file_changes = self.processor._process_file_changes(files_data)
        self.assertEqual(len(file_changes), 1)
        self.assertEqual(file_changes[0].filename, "test.py")
    
    def test_filter_commits_by_date(self):
        """Test filtering commits by date."""
        commits = [
            Mock(commit_date=datetime(2024, 1, 15)),
            Mock(commit_date=datetime(2024, 2, 15)),
            Mock(commit_date=datetime(2024, 3, 15))
        ]
        
        filtered = self.processor.filter_commits(
            commits,
            date_from=datetime(2024, 2, 1)
        )
        self.assertEqual(len(filtered), 2)
    
    def test_filter_commits_by_team(self):
        """Test filtering commits by team."""
        commits = [
            Mock(team_name="backend"),
            Mock(team_name="frontend"),
            Mock(team_name="backend")
        ]
        
        filtered = self.processor.filter_commits(
            commits,
            teams=["backend"]
        )
        self.assertEqual(len(filtered), 2)


if __name__ == "__main__":
    unittest.main()