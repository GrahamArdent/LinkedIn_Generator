#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.app.codex_provider import CodexConfig,CodexProvider
from src.app.codex_trial import run_trial,show_trial,complete_comparison,validate_trial_evidence,reconcile_trial
from src.app.editorial_structure import save_preparation,validate_prepared_request

def main():
    p=argparse.ArgumentParser(description="Subscription-only LinkedIn engine/baseline trial; no API fallback.")
    p.add_argument("action",choices=["prepare","generate","complete-comparison","show"])
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--request",type=Path)
    p.add_argument("--config",type=Path)
    p.add_argument("--evidence-bundle",type=Path)
    p.add_argument("--score-baseline",action="store_true")
    args=p.parse_args()
    if args.action=="show": result=show_trial(args.out)
    else:
        if not args.request: p.error("action needs --request")
        data=json.loads(args.request.read_text())
        bundle=json.loads(args.evidence_bundle.read_text()) if args.evidence_bundle else None
        if args.action=="prepare":
            result=save_preparation(args.out,data,bundle)
        else:
            if not args.config: p.error("generate needs --config")
            cfg=json.loads(args.config.read_text())
            config=CodexConfig(**{**cfg,"resume_root":Path(cfg["resume_root"]),"python":Path(cfg["python"])})
            old=reconcile_trial(data,args.out,model=config.model,score_baseline=args.score_baseline,evidence_bundle=bundle)
            if old is not None and old['state']=='completed':
                result=old
            else:
                if args.action=='complete-comparison':
                    if not (old and old['state']=='failed' and old.get('error_code')=='NO_QUALIFIED_CANDIDATE'
                            and old.get('engine',{}).get('body')):
                        raise ValueError('RECONCILIATION_REQUIRED')
                elif old is not None:
                    raise ValueError('RECONCILIATION_REQUIRED')
                elif data.get('persona_key','graham')=='graham':
                    validate_prepared_request(data,bundle)
                if bundle is not None: validate_trial_evidence(data,bundle)
                provider=CodexProvider(config,args.out/'codex-attempts',data['request_id'])
                action=complete_comparison if args.action=='complete-comparison' else run_trial
                result=action(data,args.out,provider,model=config.model,score_baseline=args.score_baseline,evidence_bundle=bundle)
    print(json.dumps({"state":result["state"],"engine_gate":result.get("engine_gate"),"mode":result["mode"],"review":str(args.out/"review.md")}))
if __name__=="__main__":
    try: main()
    except Exception as exc:
        print(json.dumps({"status":"failed","error_code":getattr(exc,"code",str(exc))}),file=sys.stderr)
        sys.exit(2)
