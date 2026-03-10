import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.category_service import (
    DEFAULT_CATEGORIES_I18N,
    create_category,
    create_default_categories,
    delete_category,
    get_categories,
    update_category,
)


async def test_create_default_categories(session: AsyncSession, test_user: User):
    """create_default_categories should create all default system categories."""
    categories = await create_default_categories(session, test_user.id)
    assert len(categories) == len(DEFAULT_CATEGORIES_I18N)
    # All should be system categories
    for cat in categories:
        assert cat.is_system is True
        assert cat.user_id == test_user.id
    # Verify names match the DEFAULT_CATEGORIES_I18N (pt-BR by default)
    expected_names = {data["pt-BR"] for data in DEFAULT_CATEGORIES_I18N.values()}
    actual_names = {c.name for c in categories}
    assert actual_names == expected_names


async def test_get_categories(
    session: AsyncSession, test_user: User, test_categories: list[Category]
):
    """get_categories should return all categories for the given user."""
    categories = await get_categories(session, test_user.id)
    assert len(categories) == len(test_categories)
    returned_ids = {c.id for c in categories}
    expected_ids = {c.id for c in test_categories}
    assert returned_ids == expected_ids


async def test_get_categories_excludes_other_users(
    session: AsyncSession, test_user: User, test_categories: list[Category]
):
    """get_categories should not return categories belonging to other users."""
    other_user_id = uuid.uuid4()
    categories = await get_categories(session, other_user_id)
    assert len(categories) == 0


async def test_create_category(session: AsyncSession, test_user: User):
    """create_category should create a custom (non-system) category."""
    data = CategoryCreate(name="Educacao", icon="📚", color="#9333EA")
    category = await create_category(session, test_user.id, data)

    assert category.id is not None
    assert category.name == "Educacao"
    assert category.icon == "📚"
    assert category.color == "#9333EA"
    assert category.user_id == test_user.id
    assert category.is_system is False


async def test_update_category(
    session: AsyncSession, test_user: User, test_categories: list[Category]
):
    """update_category should update name, icon, and color."""
    cat = test_categories[0]  # Alimentacao
    data = CategoryUpdate(name="Comida", icon="🍕", color="#FF6347")
    updated = await update_category(session, cat.id, test_user.id, data)

    assert updated is not None
    assert updated.name == "Comida"
    assert updated.icon == "🍕"
    assert updated.color == "#FF6347"


async def test_update_category_partial(
    session: AsyncSession, test_user: User, test_categories: list[Category]
):
    """update_category with partial data should only update provided fields."""
    cat = test_categories[1]  # Transporte
    original_icon = cat.icon
    original_color = cat.color
    data = CategoryUpdate(name="Mobilidade")
    updated = await update_category(session, cat.id, test_user.id, data)

    assert updated is not None
    assert updated.name == "Mobilidade"
    assert updated.icon == original_icon
    assert updated.color == original_color


async def test_update_category_not_found(session: AsyncSession, test_user: User):
    """update_category should return None for non-existent category."""
    data = CategoryUpdate(name="Ghost")
    result = await update_category(session, uuid.uuid4(), test_user.id, data)
    assert result is None


async def test_delete_category(session: AsyncSession, test_user: User):
    """delete_category should successfully delete a non-system category."""
    # Create a non-system category first
    data = CategoryCreate(name="Temporaria", icon="🗑️", color="#000000")
    cat = await create_category(session, test_user.id, data)
    assert cat.is_system is False

    result = await delete_category(session, cat.id, test_user.id)
    assert result is True

    # Verify it's gone
    from app.services.category_service import get_category

    deleted = await get_category(session, cat.id, test_user.id)
    assert deleted is None


async def test_delete_system_category_fails(
    session: AsyncSession, test_user: User, test_categories: list[Category]
):
    """delete_category should refuse to delete system categories (returns False)."""
    system_cat = test_categories[0]  # is_system=True from fixture
    assert system_cat.is_system is True

    result = await delete_category(session, system_cat.id, test_user.id)
    assert result is False

    # Verify it still exists
    from app.services.category_service import get_category

    still_exists = await get_category(session, system_cat.id, test_user.id)
    assert still_exists is not None
    assert still_exists.id == system_cat.id
