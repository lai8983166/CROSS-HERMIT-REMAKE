"""Explicit resume preflight using the frozen proof's own authentication only.

This command reads the requested source but does not run a replay or create native
resources. The original proof authenticates again before its fresh execution.
"""
import argparse
import importlib


def authenticate_resume(prefix, index, checkpoint, checkpoint_sha256, prior_orchestrator=None):
    # Lazy import: importing this helper in isolation never loads native tooling.
    proof = importlib.import_module('tools.terminal_unit_frontends_proof')
    data, identity = proof.authenticate_source(prefix)
    proof.need(data['case'] == proof.source.previous.overlay.parent.corpus()[index],
               'fixed source case identity')
    row = proof.corpus.read_case(prefix, index)
    return proof.resume_source_proof(checkpoint, checkpoint_sha256, data, identity,
                                     row, index, prior_orchestrator)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--case', type=int, choices=(0, 1), required=True)
    parser.add_argument('--source-proof-checkpoint', required=True)
    parser.add_argument('--source-proof-checkpoint-sha256', required=True)
    parser.add_argument('--prior-orchestrator')
    args = parser.parse_args(argv)
    authenticate_resume(args.source, args.case, args.source_proof_checkpoint,
                        args.source_proof_checkpoint_sha256, args.prior_orchestrator)


if __name__ == '__main__':
    main()
