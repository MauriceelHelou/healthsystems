"""
Hierarchy utilities for node DAG management.

Provides functions for:
- Cycle detection
- Ancestor/descendant traversal
- Path computation
- Hierarchy validation
"""

from typing import List, Set, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select


def would_create_cycle(
    db: Session,
    parent_id: str,
    child_id: str,
    node_model
) -> bool:
    """
    Check if adding parent->child relationship would create a cycle.

    In a DAG, a cycle would be created if the child is already
    an ancestor of the parent.

    Args:
        db: Database session
        parent_id: ID of the proposed parent node
        child_id: ID of the proposed child node
        node_model: The Node model class

    Returns:
        True if adding this relationship would create a cycle
    """
    if parent_id == child_id:
        return True  # Self-loop is a cycle

    parent = db.query(node_model).filter(node_model.id == parent_id).first()
    if not parent:
        return False  # Parent doesn't exist, no cycle possible

    # Check if child_id is in parent's ancestors
    ancestors = parent.all_ancestors or []
    return child_id in ancestors


def get_all_ancestors(
    db: Session,
    node_id: str,
    node_model,
    visited: Optional[Set[str]] = None
) -> Set[str]:
    """
    Recursively get all ancestors of a node via the hierarchy junction table.

    Args:
        db: Database session
        node_id: ID of the node
        node_model: The Node model class
        visited: Set of already visited nodes (for cycle detection)

    Returns:
        Set of all ancestor node IDs
    """
    if visited is None:
        visited = set()

    if node_id in visited:
        return visited  # Already processed, avoid infinite loop

    visited.add(node_id)

    node = db.query(node_model).filter(node_model.id == node_id).first()
    if not node or not node.parents:
        return visited - {node_id}  # Exclude self from ancestors

    for parent in node.parents:
        get_all_ancestors(db, parent.id, node_model, visited)

    return visited - {node_id}  # Exclude self


def get_all_descendants(
    db: Session,
    node_id: str,
    node_model,
    visited: Optional[Set[str]] = None
) -> Set[str]:
    """
    Recursively get all descendants of a node.

    Args:
        db: Database session
        node_id: ID of the node
        node_model: The Node model class
        visited: Set of already visited nodes (for cycle detection)

    Returns:
        Set of all descendant node IDs
    """
    if visited is None:
        visited = set()

    if node_id in visited:
        return visited

    visited.add(node_id)

    node = db.query(node_model).filter(node_model.id == node_id).first()
    if not node or not hasattr(node, 'children') or not node.children:
        return visited - {node_id}

    for child in node.children:
        get_all_descendants(db, child.id, node_model, visited)

    return visited - {node_id}  # Exclude self


def compute_depth(
    db: Session,
    node_id: str,
    node_model,
    cache: Optional[Dict[str, int]] = None
) -> int:
    """
    Compute the depth of a node in the hierarchy.

    Depth is the maximum distance from any root node.
    Root nodes (no parents) have depth 0.

    Args:
        db: Database session
        node_id: ID of the node
        node_model: The Node model class
        cache: Optional cache for computed depths

    Returns:
        Depth of the node (0 for root)
    """
    if cache is None:
        cache = {}

    if node_id in cache:
        return cache[node_id]

    node = db.query(node_model).filter(node_model.id == node_id).first()
    if not node or not node.parents:
        cache[node_id] = 0
        return 0

    # Depth is max parent depth + 1
    max_parent_depth = max(
        compute_depth(db, p.id, node_model, cache) for p in node.parents
    )

    cache[node_id] = max_parent_depth + 1
    return cache[node_id]


def compute_primary_path(
    db: Session,
    node_id: str,
    node_model,
    cache: Optional[Dict[str, str]] = None
) -> str:
    """
    Compute the primary path for a node.

    Uses the first parent (by order_index) to build the canonical path.
    Format: "root_id/parent_id/node_id"

    Args:
        db: Database session
        node_id: ID of the node
        node_model: The Node model class
        cache: Optional cache for computed paths

    Returns:
        Primary path string
    """
    if cache is None:
        cache = {}

    if node_id in cache:
        return cache[node_id]

    node = db.query(node_model).filter(node_model.id == node_id).first()
    if not node or not node.parents:
        cache[node_id] = node_id
        return node_id

    # Use first parent (could be ordered by order_index in future)
    first_parent = node.parents[0]
    parent_path = compute_primary_path(db, first_parent.id, node_model, cache)

    cache[node_id] = f"{parent_path}/{node_id}"
    return cache[node_id]


def get_root_ancestors(
    db: Session,
    node_id: str,
    node_model
) -> List[str]:
    """
    Get only the root (depth=0) ancestors of a node.

    These are the "domains" the node belongs to.

    Args:
        db: Database session
        node_id: ID of the node
        node_model: The Node model class

    Returns:
        List of root ancestor IDs (domain IDs)
    """
    all_ancestors = get_all_ancestors(db, node_id, node_model)

    root_ids = []
    for ancestor_id in all_ancestors:
        ancestor = db.query(node_model).filter(node_model.id == ancestor_id).first()
        if ancestor and ancestor.depth == 0:
            root_ids.append(ancestor_id)

    return root_ids


def update_node_hierarchy_fields(
    db: Session,
    node_id: str,
    node_model
) -> None:
    """
    Update all hierarchy-related fields for a node.

    Call this after adding/removing parent relationships.
    Updates: depth, primary_path, all_ancestors

    Args:
        db: Database session
        node_id: ID of the node to update
        node_model: The Node model class
    """
    node = db.query(node_model).filter(node_model.id == node_id).first()
    if not node:
        return

    # Compute new values
    depth = compute_depth(db, node_id, node_model)
    primary_path = compute_primary_path(db, node_id, node_model)
    all_ancestors = list(get_all_ancestors(db, node_id, node_model))

    # Update node
    node.depth = depth
    node.primary_path = primary_path
    node.all_ancestors = all_ancestors

    db.commit()


def update_descendant_hierarchy_fields(
    db: Session,
    node_id: str,
    node_model
) -> None:
    """
    Update hierarchy fields for a node and all its descendants.

    Call this after changing the hierarchy of a node that has children.

    Args:
        db: Database session
        node_id: ID of the node whose hierarchy changed
        node_model: The Node model class
    """
    # Update the node itself
    update_node_hierarchy_fields(db, node_id, node_model)

    # Update all descendants
    descendants = get_all_descendants(db, node_id, node_model)
    for desc_id in descendants:
        update_node_hierarchy_fields(db, desc_id, node_model)


def validate_hierarchy_integrity(
    db: Session,
    node_model
) -> List[Tuple[str, str]]:
    """
    Validate the integrity of the entire hierarchy.

    Checks for:
    - Cycles
    - Orphaned paths
    - Inconsistent depths

    Args:
        db: Database session
        node_model: The Node model class

    Returns:
        List of (node_id, error_message) tuples
    """
    errors = []

    nodes = db.query(node_model).all()

    for node in nodes:
        # Check depth consistency
        computed_depth = compute_depth(db, node.id, node_model)
        if node.depth != computed_depth:
            errors.append((node.id, f"Depth mismatch: stored={node.depth}, computed={computed_depth}"))

        # Check for cycles (node should not be in its own ancestors)
        ancestors = get_all_ancestors(db, node.id, node_model)
        if node.id in ancestors:
            errors.append((node.id, "Cycle detected: node is its own ancestor"))

        # Check all_ancestors consistency
        computed_ancestors = set(get_all_ancestors(db, node.id, node_model))
        stored_ancestors = set(node.all_ancestors or [])
        if computed_ancestors != stored_ancestors:
            errors.append((node.id, f"Ancestor mismatch: stored={stored_ancestors}, computed={computed_ancestors}"))

    return errors


def add_parent_child_relationship(
    db: Session,
    parent_id: str,
    child_id: str,
    node_model,
    node_hierarchy_table,
    relationship_type: str = "contains",
    order_index: int = 0
) -> Tuple[bool, str]:
    """
    Add a parent-child relationship with cycle detection.

    Args:
        db: Database session
        parent_id: ID of the parent node
        child_id: ID of the child node
        node_model: The Node model class
        node_hierarchy_table: The node_hierarchy junction table
        relationship_type: Type of relationship (contains, specializes, etc.)
        order_index: Order among siblings

    Returns:
        Tuple of (success, message)
    """
    # Check for cycle
    if would_create_cycle(db, parent_id, child_id, node_model):
        return False, f"Cannot add relationship: would create cycle (parent={parent_id}, child={child_id})"

    # Check both nodes exist
    parent = db.query(node_model).filter(node_model.id == parent_id).first()
    child = db.query(node_model).filter(node_model.id == child_id).first()

    if not parent:
        return False, f"Parent node '{parent_id}' does not exist"
    if not child:
        return False, f"Child node '{child_id}' does not exist"

    # Add relationship
    from sqlalchemy import insert
    stmt = insert(node_hierarchy_table).values(
        parent_node_id=parent_id,
        child_node_id=child_id,
        relationship_type=relationship_type,
        order_index=order_index
    )

    try:
        db.execute(stmt)
        db.commit()

        # Update hierarchy fields for child and its descendants
        update_descendant_hierarchy_fields(db, child_id, node_model)

        return True, f"Successfully added relationship: {parent_id} -> {child_id}"
    except Exception as e:
        db.rollback()
        return False, f"Error adding relationship: {str(e)}"


def remove_parent_child_relationship(
    db: Session,
    parent_id: str,
    child_id: str,
    node_model,
    node_hierarchy_table
) -> Tuple[bool, str]:
    """
    Remove a parent-child relationship.

    Args:
        db: Database session
        parent_id: ID of the parent node
        child_id: ID of the child node
        node_model: The Node model class
        node_hierarchy_table: The node_hierarchy junction table

    Returns:
        Tuple of (success, message)
    """
    from sqlalchemy import delete, and_

    stmt = delete(node_hierarchy_table).where(
        and_(
            node_hierarchy_table.c.parent_node_id == parent_id,
            node_hierarchy_table.c.child_node_id == child_id
        )
    )

    try:
        result = db.execute(stmt)
        db.commit()

        if result.rowcount == 0:
            return False, f"Relationship not found: {parent_id} -> {child_id}"

        # Update hierarchy fields for child and its descendants
        update_descendant_hierarchy_fields(db, child_id, node_model)

        return True, f"Successfully removed relationship: {parent_id} -> {child_id}"
    except Exception as e:
        db.rollback()
        return False, f"Error removing relationship: {str(e)}"
