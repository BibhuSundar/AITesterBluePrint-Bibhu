"""
Chapter 08 — Simple RAG Demo: Document Chunking + Nomic Embedding Visualization
=================================================================================
This script demonstrates the core steps of a RAG pipeline:
  1. Read a text document
  2. Split (chunk) the document into smaller passages
  3. Generate vector embeddings for each chunk using Ollama's Nomic-embed-text model
  4. Print the chunks and their embedding previews to the terminal
  5. Export an interactive HTML visualization file
"""

import json
import os
import math
import httpx
import sys

# ─── Configuration ────────────────────────────────────────────────────────────
DOCUMENT_PATH = os.path.join(os.path.dirname(__file__), "promod_testing_academy_story.txt")
OUTPUT_HTML    = os.path.join(os.path.dirname(__file__), "rag_visualization.html")
OLLAMA_URL     = os.getenv("OLLAMA_URL", "http://localhost:11434")
EMBED_MODEL    = "nomic-embed-text"
CHUNK_SIZE     = 500   # characters per chunk
CHUNK_OVERLAP  = 100   # overlap between consecutive chunks


# ─── Step 1: Read the Source Document ─────────────────────────────────────────
def read_document(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ─── Step 2: Chunk the Document ──────────────────────────────────────────────
def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[dict]:
    """
    Split text into overlapping chunks of `chunk_size` characters.
    Tries to break at sentence boundaries. Skips degenerate tiny chunks.
    Returns a list of dicts: { id, text, start, end, char_count, word_count }
    """
    chunks = []
    start = 0
    chunk_id = 1
    min_chunk_len = 50  # skip degenerate chunks

    while start < len(text):
        end = min(start + chunk_size, len(text))

        # Try to break at a sentence boundary (period followed by space/newline)
        if end < len(text):
            last_period = text.rfind(". ", start, end)
            if last_period != -1 and last_period > start + min_chunk_len:
                end = last_period + 1  # include the period

        chunk_text_slice = text[start:end].strip()

        if len(chunk_text_slice) >= min_chunk_len or start + chunk_size >= len(text):
            if chunk_text_slice:
                chunks.append({
                    "id": f"chunk_{chunk_id:03d}",
                    "text": chunk_text_slice,
                    "start_char": start,
                    "end_char": end,
                    "char_count": len(chunk_text_slice),
                    "word_count": len(chunk_text_slice.split()),
                })
                chunk_id += 1

        # Advance by (chunk_size - overlap), never less than half the chunk_size
        step = max(chunk_size - overlap, chunk_size // 2)
        start += step

        # If somehow past the end already, break
        if start >= len(text):
            break

    return chunks


# ─── Step 3: Generate Embeddings via Ollama Nomic-Embed-Text ─────────────────
def get_embedding(text: str) -> list[float]:
    """Call Ollama embedding endpoint for a single piece of text."""
    resp = httpx.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=60.0,
    )
    resp.raise_for_status()
    return resp.json()["embedding"]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# ─── Step 4: Pretty-Print to Terminal ────────────────────────────────────────
def print_chunks(chunks: list[dict]):
    print("=" * 80)
    print(f"  DOCUMENT CHUNKING RESULTS — {len(chunks)} chunks generated")
    print(f"  Chunk Size: {CHUNK_SIZE} chars | Overlap: {CHUNK_OVERLAP} chars")
    print("=" * 80)

    for i, chunk in enumerate(chunks):
        print(f"\n{'─' * 80}")
        print(f"  📄 {chunk['id'].upper()}")
        print(f"  Characters: {chunk['char_count']} | Words: {chunk['word_count']} | Chars [{chunk['start_char']}–{chunk['end_char']}]")
        
        if "embedding" in chunk:
            emb = chunk["embedding"]
            print(f"  🧬 Embedding Dimensions: {len(emb)}")
            print(f"  🧬 First 8 values: [{', '.join(f'{v:.6f}' for v in emb[:8])} ...]")
            print(f"  🧬 Magnitude: {math.sqrt(sum(v*v for v in emb)):.6f}")
        
        print(f"  {'─' * 76}")
        # Print text with word wrap
        words = chunk["text"].split()
        line = "  "
        for word in words:
            if len(line) + len(word) + 1 > 78:
                print(line)
                line = "  " + word
            else:
                line += " " + word if line.strip() else "  " + word
        if line.strip():
            print(line)

    print(f"\n{'=' * 80}")


# ─── Step 5: Generate HTML Visualization ─────────────────────────────────────
def generate_html(chunks: list[dict], similarity_matrix: list[list[float]], document_text: str):
    # Prepare JSON data for JavaScript
    chunks_json = json.dumps([{
        "id": c["id"],
        "text": c["text"],
        "start_char": c["start_char"],
        "end_char": c["end_char"],
        "char_count": c["char_count"],
        "word_count": c["word_count"],
        "embedding_dim": len(c.get("embedding", [])),
        "embedding_preview": c.get("embedding", [])[:20],
        "magnitude": round(math.sqrt(sum(v*v for v in c.get("embedding", []))), 4),
    } for c in chunks], indent=2)

    sim_json = json.dumps([[round(v, 4) for v in row] for row in similarity_matrix])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>RAG Chunking & Embedding Visualizer</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Inter', sans-serif;
    background: #0a0e1a;
    color: #e2e8f0;
    min-height: 100vh;
  }}

  /* Animated background blobs */
  .bg-blob {{
    position: fixed; border-radius: 50%; filter: blur(120px); opacity: 0.12; pointer-events: none; z-index: 0;
    animation: blobFloat 12s ease-in-out infinite alternate;
  }}
  .bg-blob.a {{ width: 500px; height: 500px; background: #06b6d4; top: -100px; left: -80px; }}
  .bg-blob.b {{ width: 400px; height: 400px; background: #d946ef; bottom: -50px; right: -50px; animation-delay: 3s; }}
  .bg-blob.c {{ width: 350px; height: 350px; background: #8b5cf6; top: 40%; left: 50%; animation-delay: 6s; }}
  @keyframes blobFloat {{
    0% {{ transform: translate(0, 0) scale(1); }}
    50% {{ transform: translate(30px, -40px) scale(1.08); }}
    100% {{ transform: translate(-20px, 20px) scale(0.95); }}
  }}

  .container {{ max-width: 1200px; margin: 0 auto; padding: 40px 20px; position: relative; z-index: 1; }}

  /* Header */
  .hero {{ text-align: center; margin-bottom: 50px; }}
  .hero h1 {{
    font-size: 2.8rem; font-weight: 800;
    background: linear-gradient(135deg, #06b6d4, #d946ef, #8b5cf6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
  }}
  .hero p {{ color: #94a3b8; font-size: 1.1rem; font-weight: 300; }}

  /* Stats bar */
  .stats {{
    display: flex; justify-content: center; gap: 30px; margin-bottom: 40px; flex-wrap: wrap;
  }}
  .stat-card {{
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 18px 28px; text-align: center;
    backdrop-filter: blur(12px);
    transition: transform 0.2s, border-color 0.3s;
  }}
  .stat-card:hover {{ transform: translateY(-3px); border-color: rgba(6,182,212,0.4); }}
  .stat-card .num {{ font-size: 2rem; font-weight: 700; color: #06b6d4; }}
  .stat-card .label {{ font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px; }}

  /* Section titles */
  .section-title {{
    font-size: 1.4rem; font-weight: 700; margin-bottom: 20px;
    display: flex; align-items: center; gap: 10px;
  }}
  .section-title .icon {{ font-size: 1.3rem; }}

  /* Tabs */
  .tabs {{ display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }}
  .tab {{
    padding: 10px 22px; border-radius: 12px; cursor: pointer; font-weight: 500; font-size: 0.85rem;
    border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.03);
    color: #94a3b8; transition: all 0.25s;
  }}
  .tab:hover {{ border-color: rgba(217,70,239,0.5); color: #e2e8f0; }}
  .tab.active {{ background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; border-color: transparent; }}

  /* Panels */
  .panel {{ display: none; }}
  .panel.active {{ display: block; }}

  /* Chunk cards */
  .chunk-card {{
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px; padding: 24px; margin-bottom: 20px;
    backdrop-filter: blur(14px);
    transition: border-color 0.3s, box-shadow 0.3s;
  }}
  .chunk-card:hover {{
    border-color: rgba(6,182,212,0.35);
    box-shadow: 0 0 30px rgba(6,182,212,0.06);
  }}
  .chunk-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 10px; }}
  .chunk-id {{
    font-weight: 700; font-size: 0.9rem;
    background: linear-gradient(135deg, #06b6d4, #8b5cf6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }}
  .chunk-badges {{ display: flex; gap: 8px; flex-wrap: wrap; }}
  .badge {{
    font-size: 0.7rem; padding: 4px 12px; border-radius: 20px; font-weight: 600;
  }}
  .badge-chars {{ background: rgba(6,182,212,0.15); color: #06b6d4; border: 1px solid rgba(6,182,212,0.25); }}
  .badge-words {{ background: rgba(217,70,239,0.15); color: #d946ef; border: 1px solid rgba(217,70,239,0.25); }}
  .badge-dim {{ background: rgba(139,92,246,0.15); color: #a78bfa; border: 1px solid rgba(139,92,246,0.25); }}
  
  .chunk-text {{
    font-size: 0.88rem; line-height: 1.75; color: #cbd5e1;
    background: rgba(0,0,0,0.25); padding: 16px; border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.04); margin-bottom: 14px;
    white-space: pre-wrap;
  }}
  .embed-preview {{
    font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 0.72rem;
    color: #64748b; background: rgba(0,0,0,0.3); padding: 12px; border-radius: 10px;
    overflow-x: auto; border: 1px solid rgba(255,255,255,0.04);
  }}
  .embed-preview .val {{ color: #06b6d4; }}

  /* Similarity matrix */
  .matrix-container {{ overflow-x: auto; }}
  table.sim-matrix {{
    border-collapse: collapse; font-size: 0.75rem; width: 100%;
  }}
  table.sim-matrix th, table.sim-matrix td {{
    padding: 10px 8px; text-align: center; border: 1px solid rgba(255,255,255,0.06);
    min-width: 60px;
  }}
  table.sim-matrix th {{
    background: rgba(6,182,212,0.1); color: #06b6d4; font-weight: 700; font-size: 0.7rem;
  }}

  /* Original doc */
  .original-doc {{
    background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.06);
    padding: 24px; border-radius: 16px; font-size: 0.9rem; line-height: 1.85; color: #94a3b8;
    white-space: pre-wrap; max-height: 500px; overflow-y: auto;
  }}

  /* Footer */
  .footer {{ text-align: center; margin-top: 60px; color: #475569; font-size: 0.8rem; }}
</style>
</head>
<body>
<div class="bg-blob a"></div>
<div class="bg-blob b"></div>
<div class="bg-blob c"></div>

<div class="container">
  <div class="hero">
    <h1>RAG Chunking & Embedding Visualizer</h1>
    <p>Powered by Nomic-Embed-Text via Ollama &bull; Chapter 08 — The Testing Academy AI Blueprint</p>
  </div>

  <div class="stats" id="stats"></div>

  <div class="tabs">
    <div class="tab active" onclick="showPanel('chunks')">📄 Chunks</div>
    <div class="tab" onclick="showPanel('embeddings')">🧬 Embedding Details</div>
    <div class="tab" onclick="showPanel('similarity')">🔗 Similarity Matrix</div>
    <div class="tab" onclick="showPanel('original')">📖 Original Document</div>
  </div>

  <div class="panel active" id="panel-chunks"></div>
  <div class="panel" id="panel-embeddings"></div>
  <div class="panel" id="panel-similarity"></div>
  <div class="panel" id="panel-original">
    <h3 class="section-title"><span class="icon">📖</span> Original Document</h3>
    <div class="original-doc">{document_text.replace(chr(60), '&lt;').replace(chr(62), '&gt;')}</div>
  </div>

  <div class="footer">
    Built with ❤️ by The Testing Academy &bull; Simple RAG Demo &bull; 2026
  </div>
</div>

<script>
const chunks = {chunks_json};
const simMatrix = {sim_json};

// Stats
document.getElementById('stats').innerHTML = `
  <div class="stat-card"><div class="num">${{chunks.length}}</div><div class="label">Chunks Created</div></div>
  <div class="stat-card"><div class="num">${{chunks[0]?.embedding_dim || 0}}</div><div class="label">Embedding Dims</div></div>
  <div class="stat-card"><div class="num">{CHUNK_SIZE}</div><div class="label">Chunk Size (chars)</div></div>
  <div class="stat-card"><div class="num">{CHUNK_OVERLAP}</div><div class="label">Overlap (chars)</div></div>
`;

// Chunks panel
let chunksHtml = '<h3 class="section-title"><span class="icon">📄</span> Document Chunks</h3>';
chunks.forEach(c => {{
  chunksHtml += `
    <div class="chunk-card">
      <div class="chunk-header">
        <span class="chunk-id">${{c.id.toUpperCase()}}</span>
        <div class="chunk-badges">
          <span class="badge badge-chars">${{c.char_count}} chars</span>
          <span class="badge badge-words">${{c.word_count}} words</span>
          <span class="badge badge-dim">${{c.embedding_dim}}D vector</span>
        </div>
      </div>
      <div class="chunk-text">${{c.text}}</div>
    </div>`;
}});
document.getElementById('panel-chunks').innerHTML = chunksHtml;

// Embeddings panel
let embHtml = '<h3 class="section-title"><span class="icon">🧬</span> Embedding Vectors (Preview — first 20 dimensions)</h3>';
chunks.forEach(c => {{
  const vals = c.embedding_preview.map(v => `<span class="val">${{v.toFixed(6)}}</span>`).join(', ');
  embHtml += `
    <div class="chunk-card">
      <div class="chunk-header">
        <span class="chunk-id">${{c.id.toUpperCase()}}</span>
        <div class="chunk-badges">
          <span class="badge badge-dim">Magnitude: ${{c.magnitude}}</span>
        </div>
      </div>
      <div class="embed-preview">[${{vals}}, ...]</div>
    </div>`;
}});
document.getElementById('panel-embeddings').innerHTML = embHtml;

// Similarity matrix
let simHtml = '<h3 class="section-title"><span class="icon">🔗</span> Cosine Similarity Between Chunks</h3><div class="matrix-container"><table class="sim-matrix"><tr><th></th>';
chunks.forEach(c => {{ simHtml += `<th>${{c.id.replace('chunk_','')}}</th>`; }});
simHtml += '</tr>';
simMatrix.forEach((row, i) => {{
  simHtml += `<tr><th>${{chunks[i].id.replace('chunk_','')}}</th>`;
  row.forEach((val, j) => {{
    const intensity = Math.floor(val * 255);
    const bg = i === j ? 'rgba(6,182,212,0.3)' : `rgba(217,70,239,${{(val * 0.5).toFixed(2)}})`;
    simHtml += `<td style="background:${{bg}}; color:${{val > 0.6 ? '#fff' : '#94a3b8'}}">${{val.toFixed(2)}}</td>`;
  }});
  simHtml += '</tr>';
}});
simHtml += '</table></div>';
document.getElementById('panel-similarity').innerHTML = simHtml;

function showPanel(name) {{
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById('panel-' + name).classList.add('active');
  event.target.classList.add('active');
}}
</script>
</body>
</html>"""
    
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n  ✅ HTML visualization saved to: {OUTPUT_HTML}")


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("\n🚀 RAG Pipeline — Document Chunking & Embedding Demo")
    print(f"   Document: {DOCUMENT_PATH}\n")

    # 1. Read
    if not os.path.exists(DOCUMENT_PATH):
        print(f"  ❌ File not found: {DOCUMENT_PATH}")
        sys.exit(1)

    document_text = read_document(DOCUMENT_PATH)
    print(f"  📖 Document loaded: {len(document_text)} characters, {len(document_text.split())} words\n")

    # 2. Chunk
    chunks = chunk_text(document_text)
    print(f"  ✂️  Chunking complete: {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})\n")

    # 3. Embed
    print("  🧬 Generating embeddings via Ollama nomic-embed-text ...\n")
    for i, chunk in enumerate(chunks):
        try:
            emb = get_embedding(chunk["text"])
            chunk["embedding"] = emb
            print(f"    ✅ {chunk['id']} — {len(emb)} dimensions")
        except Exception as e:
            print(f"    ❌ {chunk['id']} — Embedding failed: {e}")
            chunk["embedding"] = []

    # 4. Print terminal results
    print_chunks(chunks)

    # 5. Compute similarity matrix
    n = len(chunks)
    sim_matrix = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if chunks[i].get("embedding") and chunks[j].get("embedding"):
                sim_matrix[i][j] = cosine_similarity(chunks[i]["embedding"], chunks[j]["embedding"])

    print("\n  🔗 Cosine Similarity Matrix (first 5x5 preview):")
    print("       ", "  ".join(f"C{j+1:02d}" for j in range(min(5, n))))
    for i in range(min(5, n)):
        row_str = "  ".join(f"{sim_matrix[i][j]:.2f}" for j in range(min(5, n)))
        print(f"  C{i+1:02d}  {row_str}")

    # 6. Generate HTML
    generate_html(chunks, sim_matrix, document_text)

    print("\n  🎉 Done! Open rag_visualization.html in your browser to explore.\n")


if __name__ == "__main__":
    main()
