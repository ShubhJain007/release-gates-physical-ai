# Release Gates for Physical AI

A unified framework for functional, adversarial, cyber, and hardware verification of
learned robot systems.

**Paper:** [`paper/main.tex`](paper/main.tex) · build produces `docs/release-gates-physical-ai.pdf`
**Project page:** `docs/index.html` (GitHub Pages target)
**Evidence spec:** [`schema/evidence.schema.json`](schema/evidence.schema.json)

---

## What this is

A framework and position paper. Learned manipulation policies now ship to fleets on a
monthly cadence, while the evidence behind each release is scattered across four
disconnected practices: functional evaluation, adversarial robustness, product
cybersecurity, and hardware reliability. This work specifies how to compose them into a
single release decision.

The core rule the paper proposes, **fidelity gating**:

> A test may block a release only once its predictive validity against real outcomes has
> been measured. Otherwise it reports as advisory. Apparent realism is not a
> qualification.

The repository ships the paper, the project page, and a machine-readable schema for the
evidence record defined in §3 of the paper, so the model can be implemented and argued
with rather than only read.

## Status

- Version: **0.1.0** (preprint draft, not peer reviewed)
- Contains **no new experimental results**. Every quantitative figure is attributed to
  published work or a named standard; every threshold proposed is labelled as a proposal.
- Scope: manipulation and station-based mobile manipulation. Locomotion, whole-body
  balance, and public-road autonomy are out of scope.

## Repository layout

```
paper/     LaTeX source, bibliography, Makefile
docs/      Project page (static, GitHub Pages) + built PDF
schema/    JSON Schema for the evidence record (Definition 2)
```

## Building the paper

Requires [Tectonic](https://tectonic-typesetting.github.io/) (no system TeX install needed):

```sh
cd paper && make          # → ../docs/release-gates-physical-ai.pdf
make clean                # remove build intermediates
```

With a conventional TeX Live installation:

```sh
cd paper && latexmk -pdf main.tex
```

## Serving the project page locally

```sh
python3 -m http.server -d docs 8000   # http://localhost:8000
```

## Citing

See [`CITATION.cff`](CITATION.cff), or:

```bibtex
@techreport{releasegates2026,
  title       = {Release Gates for Physical AI: A Unified Framework for Functional,
                 Adversarial, Cyber, and Hardware Verification of Learned Robot Systems},
  author      = {Jain, Shubh},
  institution = {Carnegie Mellon University},
  year        = {2026},
  month       = sep,
  note        = {Preprint, version 0.1.0}
}
```

## Contributing

Disagreements about the thresholds in Table 3 are the most useful contribution. They are
stated numerically so they can be falsified. Open an issue with the domain, the metric,
and the measurement.

## License

- Paper and figures: [CC BY 4.0](LICENSE-PAPER)
- Schema and code: [MIT](LICENSE)
