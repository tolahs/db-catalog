from typing import Any, AsyncGenerator
from backend.config import db
import pytest

from backend.config import DatabaseSession
from backend.repository.project import Project, ProjectRepository

pk_list = []


def create_mock_data():
    # Insert test data
    test_projects = [
        Project(
            type="mysql",
            display_name="Test Project 1",
            catalog="test_catalog",
            schema="test_schema",
            connection_info={
                "host": "localhost",
                "port": 3306,
                "user": "user",
                "password": "password",
                "database": "test_db",
            },
        ),
        Project(
            type="mysql",
            display_name="Test Project 2",
            catalog="test_catalog",
            schema="test_schema",
            connection_info={
                "host": "localhost",
                "port": 3306,
                "user": "user",
                "password": "password",
                "database": "test_db",
            },
        ),
        Project(
            type="mysql",
            display_name="Test Project 3",
            catalog="test_catalog",
            schema="test_schema",
            connection_info={
                "host": "localhost",
                "port": 3306,
                "user": "user",
                "password": "password",
                "database": "test_db",
            }, 
        ),
        Project(
            type="postgres",
            display_name="Test Project 4",
            catalog="test_catalog",
            schema="test_schema",
            connection_info={
                "host": "localhost",
                "port": 5432,
                "user": "user",
                "password": "password",
                "database": "test_db",
            },
        ),
        Project(
            type="postgres",
            display_name="Test Project 5",
            catalog="test_catalog",
            schema="test_schema",
            connection_info={
                "host": "localhost",
                "port": 5432,
                "user": "user",
                "password": "password",
                "database": "test_db",
            },
        ),
        Project(
            type="postgres",
            display_name="Test Project 6",
            catalog="test_catalog",
            schema="test_schema",
            connection_info={
                "host": "localhost",
                "port": 5432,
                "user": "user",
                "password": "password",
                "database": "test_db",
            },
        ),
        Project(
            type="postgres",
            display_name="Test Project 7",
            catalog="test_catalog",
            schema="test_schema",
            connection_info={
                "host": "localhost",
                "port": 5432,
                "user": "user",
                "password": "password",
                "database": "test_db",
            },
        ),
        Project(
            type="postgres",
            display_name="Test Project 8",
            catalog="test_catalog",
            schema="test_schema",
            connection_info={
                "host": "localhost",
                "port": 5432,
                "user": "user",
                "password": "password",
                "database": "test_db",
            },
        ),
    ]
    return test_projects



@pytest.fixture(scope="session", autouse=True)
async def db():
    print("Creating tables and db")
    await db.create_all()

@pytest.fixture()
async def project_repo():
    # db: DatabaseSession = DatabaseSession("postgresql+asyncpg://postgres:postgres@db-server/db_test")
    test_projects = create_mock_data()
    repo = ProjectRepository(entity=Project)
    try:
        for project in test_projects:
            x = await repo.create_one(project)
            pk_list.append(x.id)
            print(x)
        yield repo
    except Exception as e:
        print(e)
        raise e
    finally:
        # Clean up test data
        for project in test_projects:
            await repo.delete_one(project.id)
        await db.drop_all()
        await db.close()

class TestRepositoryProjectTest:
   
    @pytest.mark.asyncio
    async def test_get_one_by_id(self, project_repo):
        project_repo = await anext(project_repo)  # Ensure project_repo is correctly awaited
        id = pk_list[0]
        project: object | None = await project_repo.get_one_by_id(id)
        assert project is not None
        assert getattr(project, "id") == id

    @pytest.mark.asyncio
    async def test_create_project(self, project_repo):
        project_repo = await anext(project_repo)
        new_project = Project(
            type="mysql",
            display_name="Test Project",
            catalog="test_catalog",
            schema="test_schema",
            connection_info={
                "host": "localhost",
                "port": 3306,
                "user": "user",
                "password": "password",
                "database": "test_db",
            },
        )
        created_project = await project_repo.create_one(new_project)
        assert created_project is not None
        assert created_project.id is not None
        assert created_project.display_name == "Test Project"
        assert created_project.catalog == "test_catalog"
        assert created_project.schema == "test_schema"
        assert created_project.connection_info == {
            "host": "localhost",
            "port": 3306,
            "user": "user",
            "password": "password",
            "database": "test_db",
        }

    @pytest.mark.asyncio
    async def test_update_project(self, project_repo):
        project_repo = await anext(project_repo)
        id = pk_list[0]
        updated_data = {"display_name": "Updated Project"}
        updated_project = await project_repo.update_one(id, updated_data)
        assert updated_project is not None
        assert updated_project.id == id
        assert updated_project.display_name == "Updated Project"

    @pytest.mark.asyncio
    async def test_delete_project(self, project_repo):
        project_repo = await anext(project_repo)
        id = pk_list[0]
        delete_count = await project_repo.delete_one(id)
        assert delete_count == 1

    @pytest.mark.asyncio
    async def test_find_one_by(self, project_repo):
        project_repo = await anext(project_repo)
        filter_criteria = {"type": "mysql"}
        project = await project_repo.find_one_by(filter_criteria)
        assert project is not None
        assert project.type == "mysql"

    @pytest.mark.asyncio
    async def test_find_all_by(self, project_repo):
        project_repo = await anext(project_repo)
        filter_criteria = {"type": "mysql"}
        projects = await project_repo.find_all_by(filter_criteria)
        assert isinstance(projects, list)
        assert all(project.type == "mysql" for project in projects)

    @pytest.mark.asyncio
    async def test_find_all(self, project_repo):
        project_repo = await anext(project_repo)
        projects = await project_repo.find_all()
        assert isinstance(projects, list)
        assert len(projects) > 0

    @pytest.mark.asyncio
    async def test_create_many(self, project_repo: Any):  # ignore: F821
        repo: ProjectRepository = await anext(project_repo)
        new_projects = [
            Project(
                type="mysql",
                display_name="Bulk Test Project 1",
                catalog="test_catalog",
                schema="test_schema",
                connection_info={
                    "host": "localhost",
                    "port": 3306,
                    "user": "user",
                    "password": "password",
                    "database": "test_db",
                },
            ),
            Project(
                type="mysql",
                display_name="Bulk Test Project 2",
                catalog="test_catalog",
                schema="test_schema",
                connection_info={
                    "host": "localhost",
                    "port": 3306,
                    "user": "user",
                    "password": "password",
                    "database": "test_db",
                },
            ),
        ]
        created_projects = await repo.create_many(new_projects)
        assert len(created_projects) == 2
        assert all(
            project.id is not None
            and project.display_name.startswith("Bulk Test Project")
            for project in created_projects
        )

    @pytest.mark.asyncio
    async def test_delete_many(self, project_repo):
        project_repo = await anext(project_repo)
        delete_count = await project_repo.delete_many([pk_list[3] , pk_list[4]])
        assert delete_count == 2

    @pytest.mark.asyncio
    async def test_soft_delete_one(self, project_repo):
        project_repo = await anext(project_repo)
        delete_count = await project_repo.soft_delete_one(pk_list[5])
        assert delete_count == 1

    @pytest.mark.asyncio
    async def test_soft_delete_many(self, project_repo):
        project_repo = await anext(project_repo)
        delete_count = await project_repo.soft_delete_many([pk_list[6], pk_list[7]])
        assert delete_count == 2
