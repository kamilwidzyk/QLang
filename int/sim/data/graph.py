from .consts import QuantumID

class EntaglementGraph:
    def __init__(self):
        self.parent: dict[QuantumID, QuantumID] = {}
        self.rank: dict[QuantumID, QuantumID] = {}
        self.members: dict[QuantumID, set[QuantumID]] = {}

    def add(self, x: QuantumID):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self.members[x] = {x}

    def find(self, x: QuantumID) -> QuantumID:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, a: QuantumID, b: QuantumID):
        self.add(a)
        self.add(b)

        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return
        
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra

        self.members[ra].update(self.members[rb])
        del self.members[rb]

        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        
    def connected(self, a: QuantumID, b: QuantumID) -> bool:
        return self.find(a) == self.find(b)
    
    def split(self, x: QuantumID):
        if x not in self.parent:
            return
        
        root = self.find(x)
        if root not in self.members:
            return
        
        group = set(self.members[root])
        del self.members[root]
        remaining = [node for node in group if node != x]

        self.parent[x] = x
        self.rank[x] = 0
        self.members[x] = {x}
        
        for node in remaining:
            self.parent[node] = node
            self.rank[node] = 0
            self.members[node] = {node}

    def component(self, x: QuantumID) -> set[QuantumID]:
        root = self.find(x)
        return self.members.get(root, {x})
    
    def components(self) -> dict[QuantumID, list[QuantumID]]:
        groups = {}
        for node in self.parent:
            root = self.find(node)
            groups.setdefault(root, []).append(node)

        return groups
    
    def remove(self, x: QuantumID):
        if x in self.parent:
            root = self.find(x)
            if root in self.members:
                self.members[root].discard(x)
                if not self.members[root]:
                    del self.members[root]
            del self.parent[x]
            del self.rank[x]

    def __str__(self) -> str:
        groups = self.components()

        lines = []
        for root, nodes in groups.items():
            lines.append(f"[{root}] -> {', '.join(nodes)}")

        return "\n".join(lines)

