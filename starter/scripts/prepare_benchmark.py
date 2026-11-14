"""Freeze answerable questions and evidence before any retrieval experiment."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Questions and answers are authored from the source, before retrieval is run.
ITEMS = [
    ("controlflow", "break statement breaks", "Which enclosing loop does Python break leave?", "The innermost enclosing for or while loop.", False),
    ("controlflow", "may be paired with an else", "When does a for or while loop run its else block?", "When it finishes without executing break.", False),
    ("controlflow", "default value is evaluated only once", "Why can a mutable default argument accumulate values across function calls?", "The default is evaluated once and shared between calls.", False),
    ("controlflow", "Looking at this in a bit more detail", "What does the slash in a Python function signature mean for preceding parameters?", "Parameters before / are positional-only.", False),
    ("controlflow", "Normally, these variadic arguments", "How must callers supply formal parameters placed after *args?", "By keyword rather than by position.", False),
    ("datastructures", "You might have noticed that methods", "What do list methods that only modify the list return?", "The default None value.", False),
    ("datastructures", "A list comprehension consists", "What is the basic structure of a list comprehension?", "Brackets around an expression, followed by a for clause and optionally more for or if clauses.", False),
    ("datastructures", "Curly braces or the set()", "Why should an empty set be written set() instead of {}?", "{} creates an empty dictionary.", False),
    ("datastructures", "Another useful data type built", "Why is a list unsuitable as a dictionary key?", "Dictionary keys must be immutable, but a list can be modified in place.", False),
    ("modules", "A module can contain executable statements", "In the tutorial's modules chapter, when do module initialization statements execute during imports?", "Only the first time the module name is encountered in an import statement.", True),
    ("modules", "sys.path is initialized", "Where is the module search path initialized from?", "The script directory, PYTHONPATH, and the installation-dependent default.", False),
    ("inputoutput", "It is good practice to use the with", "In the input/output chapter, what happens to a file managed by with if its body raises an exception?", "The file is properly closed when the suite finishes.", True),
    ("inputoutput", "JSON files must be encoded", "What text encoding should be used when opening JSON files for reading and writing?", "UTF-8.", False),
    ("errors", "The use of the else clause is better", "Why put code in try/except/else rather than adding it inside try?", "To avoid accidentally catching exceptions raised by code outside the protected operation.", False),
    ("errors", "If a finally clause is present", "In the errors chapter, does finally run when the try block produces no exception?", "Yes. It runs as the last task whether or not an exception occurred.", True),
    ("classes", "Generally speaking, instance variables", "Which data belongs in instance variables and which in class variables?", "Instance variables hold data unique to an instance; class variables hold shared attributes and methods.", False),
    ("classes", "There’s nothing special about instantiation", "How does a derived Python class resolve a method reference?", "Search its class attributes and then descend through base classes as necessary.", False),
    ("classes", "such a mechanism, called name mangling", "How does the classes chapter transform an identifier such as __spam to avoid subclass name clashes?", "It is textually replaced with _classname__spam, stripping leading underscores from the class name.", True),
    ("classes", "Behind the scenes, the for statement", "What tells a for loop that an iterator has no elements left?", "Its __next__ method raises StopIteration.", False),
    ("classes", "Generators are a simple", "How does a generator return data and continue from its last position?", "It uses yield and resumes where it left off when next is called.", False),
]


def main():
    folder = ROOT / "benchmark"
    folder.mkdir(exist_ok=True)
    if (folder / "questions.jsonl").exists():
        raise FileExistsError("Benchmark already frozen; preserve its split and evidence")
    pages = [json.loads(line) for line in (ROOT / "data/pages.jsonl").read_text(encoding="utf-8").splitlines()]
    questions = []
    for i, (chapter, phrase, question, answer, filtered) in enumerate(ITEMS, 1):
        matches = [(page, block) for page in pages if page["metadata"]["chapter"] == chapter
                   for block in page["text"].split("\n\n") if phrase.casefold() in block.casefold()]
        if not matches:
            raise ValueError(f"Missing evidence for q{i}: {phrase}")
        page, evidence = matches[0]
        if i == 9:
            evidence = evidence[evidence.index("You can’t use lists as keys"):]
        if i == 18:
            evidence = evidence[evidence.index("Any identifier of the form"):]
            evidence = evidence[:evidence.index("stripped.") + len("stripped.")]
        if i == 19:
            evidence = evidence[evidence.index("When there are no more elements"):]
            evidence = evidence[:evidence.index("terminate.") + len("terminate.")]
        questions.append({"id": f"q{i:02}", "split": "dev" if i <= 15 else "test",
                          "question": question, "expected_answer": answer,
                          "gold_source_id": page["document_id"], "gold_page": page["page"],
                          "evidence_quote": evidence,
                          "filter": {"chapter": chapter} if filtered else None,
                          "filter_origin": "Chapter explicitly named in question" if filtered else None})
    content = "".join(json.dumps(q, ensure_ascii=False) + "\n" for q in questions)
    (folder / "questions.jsonl").write_text(content, encoding="utf-8", newline="\n")
    ordered = sorted(pages, key=lambda p: (p["document_id"], p["page"]))
    positions = [{"document_id": ordered[i]["document_id"], "page": ordered[i]["page"],
                  "char_offset": ordered[i]["text"].find("\n\n") + 2}
                 for i in [round(j * (len(ordered) - 1) / 9) for j in range(10)]]
    (folder / "coherence_positions.json").write_text(json.dumps(positions, indent=2), encoding="utf-8")
    plan = {"frozen_at": datetime.now(timezone.utc).isoformat(),
            "benchmark_sha256": hashlib.sha256(content.encode()).hexdigest(),
            "split": "q01-q15 dev; q16-q20 classes-only topic holdout; same author prepared all questions",
            "selection_rule": ["highest dev Evidence Hit@3", "highest dev Hit@1", "fewest chunks", "alphabetical strategy ID"],
            "coherence_sampling": "10 evenly spaced source units in document_id/page order; first paragraph start",
            "model": "BAAI/bge-small-en-v1.5", "dimensions": 384,
            "strategies": {"A": {"chunking": "fixed", "size": 500, "overlap": 50, "filter": False},
                           "B": {"chunking": "paragraph", "max_size": 1000, "filter": False},
                           "C": {"chunking": "paragraph", "max_size": 1000, "filter": True}}}
    (folder / "plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(f"Frozen {len(questions)} questions and 10 shared coherence positions")
    for q in questions:
        print(q["id"], q["split"], q["gold_source_id"], q["gold_page"], len(q["evidence_quote"]))


if __name__ == "__main__":
    main()
