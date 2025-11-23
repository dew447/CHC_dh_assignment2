import pandas as pd
import networkx as nx

# ===== 1) 读入边表 =====
# 你的csv格式应为：Source,Target,Weight
edge_path = "web/daiyu_edges_cooccur.csv"  # <-- 换成你的文件名
edges = pd.read_csv(edge_path)

# ===== 2) 建图（无向 + 权重）=====
G = nx.from_pandas_edgelist(
    edges,
    source="Source",
    target="Target",
    edge_attr="Weight",
    create_using=nx.Graph()
)

print("节点数:", G.number_of_nodes())
print("边数:", G.number_of_edges())

# ===== 3) 核心指标 =====
deg = dict(G.degree())  # 度
strength = dict(G.degree(weight="Weight"))  # 加权度/强度

bet = nx.betweenness_centrality(G, weight="Weight", normalized=True)
clo = nx.closeness_centrality(G)
eig = nx.eigenvector_centrality(G, weight="Weight", max_iter=500)

# ===== 4) 汇总结果表 =====
df = pd.DataFrame({
    "node": list(G.nodes()),
    "degree": [deg[n] for n in G.nodes()],
    "strength": [strength[n] for n in G.nodes()],
    "betweenness": [bet[n] for n in G.nodes()],
    "closeness": [clo[n] for n in G.nodes()],
    "eigenvector": [eig[n] for n in G.nodes()],
})

df_sorted = df.sort_values(by="strength", ascending=False)
print("\nTop 15 by strength:")
print(df_sorted.head(15))

# ===== 5) 社群划分（greedy modularity，免装包版）=====
communities = nx.algorithms.community.greedy_modularity_communities(G, weight="Weight")
comm_map = {}
for i, comm in enumerate(communities):
    for n in comm:
        comm_map[n] = i

df["community"] = df["node"].map(comm_map)

# ===== 6) 导出给 Gephi =====
# 6.1 nodes
df.to_csv("gephi_nodes.csv", index=False)

# 6.2 edges (原样保留)
edges.to_csv("gephi_edges.csv", index=False)

# 6.3 也可以直接导出 gexf，一键导入 Gephi
nx.write_gexf(G, "web/daiyu_network.gexf")

print("\n已导出 gephi_nodes.csv / gephi_edges.csv / daiyu_network.gexf")
