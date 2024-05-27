from dataclasses import dataclass, field, asdict
from collections.abc import Hashable
from typing import TypeAlias, Literal, Any

ROOT_ITEM = "root" 
Id: TypeAlias = Hashable | Literal[ROOT_ITEM]


@dataclass
class Item:
    # Since there's no clarification on item id type
    # and preserved items' order in the input data, let's
    # just assume that the id is a hashable immutable object.
    id: Id
    parent: Id
    children: list[Hashable] = field(default_factory=list)
    type: Any = None

    def _to_dict(self) -> dict:
        output = asdict(self)
        output.pop("id")
        output.pop("children")
        if self.parent == ROOT_ITEM:
            # To conform with provided testing set structure
            output.pop("type")
        return output


class ItemIsMissing(Exception):
    def __init__(self, id):
        self.message = f"Item with ID {id} does not exist"
        super().__init__(self.message)


class TreeStore:
    def __init__(self, items: list[dict]):
        # Adding this intermediate representation makes tree
        # creation O(n) but enables O(1) access.
        # Also, storing the original items list will render `getAll()` as O(1),
        # but that would cost extra memory, so let's refrain from that,
        # even though there are no restrictions on memory usage in the quiz.
        self.items = {}
        for item in items:
            item = Item(**item)
            self.items[item.id] = item
            if item.parent in self.items:
                self.items[item.parent].children.append(item.id)

    def _ensure_item(self, id: Id) -> Item:
        item = self.items.get(id)
        if not item:
            raise ItemIsMissing(id)
        else:
            return item

    def _get_parents_path(self, id: Id, parents: list[Item] = []) -> list[Item]:
        # Using recursion here is not really desired, because by default it
        # has nesting level of 1000, which is easy to exceed on relative small
        # data, and raising recursion limit may lead to undefined behavior of
        # the interpreter. Leaving it here just for a showcase, it can easily
        # be replaced with a stack and a cycle.
        parent = self._ensure_item(id)
        parents.append(parent)

        if parent.parent == ROOT_ITEM:
            return parents
        else:
            return self._get_parents_path(parent.parent, parents)

    def getAll(self) -> list[dict]:
        return [{"id": id, **self.items[id]._to_dict()} for id in self.items.keys()]

    def getItem(self, id: int) -> dict | None:
        item = self._ensure_item(id)
        return {"id": id, **item._to_dict()} if item else None

    def getChildren(self, id: int) -> list[dict]:
        item = self._ensure_item(id)
        result = []
        for child_id in item.children:
            child = self._ensure_item(child_id)
            result.append({"id": child.id, **child._to_dict()})
        return result

    def getAllParents(self, id: int) -> list[dict]:
        path = self._get_parents_path(id)[1:]
        return [{"id": item.id, **item._to_dict()} for item in path]
