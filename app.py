"""Milestone 5 (step 2) — Gradio web interface for the CCSF CS Unofficial Guide.

Run with:
    python app.py

Then open http://localhost:7860 in your browser.
"""

import gradio as gr

from ask import ask


def handle_query(question: str):
    """Call the RAG pipeline and format results for the Gradio UI."""
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="CCSF CS Unofficial Guide") as demo:
    gr.Markdown(
        "# CCSF CS Unofficial Guide\n"
        "Ask questions about CS professors and courses at City College of San Francisco. "
        "Answers are grounded in student reviews from RateMyProfessors and Coursicle, "
        "plus official CCSF catalog entries."
    )

    inp = gr.Textbox(
        label="Your question",
        placeholder='e.g. "Which professor should I take for CS270?" or "What is CS110B?"',
        lines=2,
    )
    btn = gr.Button("Ask", variant="primary")

    answer = gr.Textbox(label="Answer", lines=8, interactive=False)
    sources = gr.Textbox(label="Retrieved from", lines=4, interactive=False)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

    gr.Markdown(
        "---\n"
        "_Answers are based only on collected student reviews and official catalog data. "
        "Always verify important decisions through official CCSF channels._"
    )

demo.launch()
