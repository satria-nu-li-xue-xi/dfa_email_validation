from graphviz import Digraph

def render_email_dfa(output_path: str = "docs/figures/email_dfa.svg"):
    g = Digraph("EmailDFA", format="svg")
    g.attr(rankdir="LR", fontsize="12")

    # Nodes
    for state in ["q0", "q1", "q2", "q3", "qReject"]:
        shape = "doublecircle" if state == "q3" else ("circle" if state != "qReject" else "Msquare")
        g.node(state, shape=shape)

    # Invisible start arrow
    g.node("start", shape="point")
    g.edge("start", "q0")

    # Edges
    g.edge("q0", "q1", label="username chars")
    g.edge("q1", "q1", label="username chars")
    g.edge("q1", "q2", label="@")
    g.edge("q2", "q2", label="domain chars")
    g.edge("q2", "q3", label=".")
    g.edge("q3", "q3", label="extension chars")

    # Rejects (optional minimal)
    g.edge("q0", "qReject", label="other")
    g.edge("q1", "qReject", label="other")
    g.edge("q2", "qReject", label="other")
    g.edge("q3", "qReject", label="other")

    g.render(filename=output_path, cleanup=True)
    print(f"Diagram disimpan di {output_path}")

if __name__ == "__main__":
    render_email_dfa()
