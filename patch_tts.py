"""
Patches installed TTS package for compatibility with current dependencies:

1. stream_generator.py: transformers 4.45+ moved BeamSearchScorer etc. to sub-modules
   (they were removed from top-level transformers namespace after 4.45.x)

2. utils/io.py: PyTorch 2.6 changed torch.load default to weights_only=True,
   which breaks XTTS model loading. We pass weights_only=False explicitly.

3. xtts_manager.py: speaker_names calls .keys() on dict_keys (should be list directly)
"""
import pathlib

BASE = pathlib.Path("/usr/local/lib/python3.11/site-packages/TTS")

# ── Patch 1: stream_generator.py ─────────────────────────────────────────────
sg = BASE / "tts/layers/xtts/stream_generator.py"
src = sg.read_text()

old_sg = (
    "from transformers import (\n"
    "    BeamSearchScorer,\n"
    "    ConstrainedBeamSearchScorer,\n"
    "    DisjunctiveConstraint,\n"
    "    GenerationConfig,\n"
    "    GenerationMixin,\n"
    "    LogitsProcessorList,\n"
    "    PhrasalConstraint,\n"
    "    PreTrainedModel,\n"
    "    StoppingCriteriaList,\n"
    ")"
)

new_sg = (
    "from transformers import (\n"
    "    GenerationConfig,\n"
    "    GenerationMixin,\n"
    "    LogitsProcessorList,\n"
    "    PreTrainedModel,\n"
    "    StoppingCriteriaList,\n"
    ")\n"
    "from transformers.generation.beam_search import BeamSearchScorer, ConstrainedBeamSearchScorer\n"
    "from transformers.generation.beam_constraints import DisjunctiveConstraint, PhrasalConstraint"
)

if old_sg in src:
    sg.write_text(src.replace(old_sg, new_sg))
    print("Patch 1 applied: stream_generator.py")
else:
    print("Patch 1: pattern not found in stream_generator.py (may already be patched)")

# ── Patch 2: utils/io.py  (torch.load weights_only) ─────────────────────────
io_py = BASE / "utils/io.py"
src2 = io_py.read_text()

old_io = "return torch.load(f, map_location=map_location, **kwargs)"
new_io = "return torch.load(f, map_location=map_location, weights_only=False, **kwargs)"

if old_io in src2:
    io_py.write_text(src2.replace(old_io, new_io))
    print("Patch 2 applied: utils/io.py (weights_only=False)")
else:
    print("Patch 2: pattern not found in utils/io.py (may already be patched)")

# ── Patch 3: xtts_manager.py  (speaker_names calls .keys() on dict_keys) ─────
mgr = BASE / "tts/layers/xtts/xtts_manager.py"
src3 = mgr.read_text()

old_mgr = "        return list(self.name_to_id.keys())"
new_mgr = "        return list(self.name_to_id)"

if old_mgr in src3:
    mgr.write_text(src3.replace(old_mgr, new_mgr))
    print("Patch 3 applied: xtts_manager.py (speaker_names)")
else:
    print("Patch 3: pattern not found in xtts_manager.py (may already be patched)")
