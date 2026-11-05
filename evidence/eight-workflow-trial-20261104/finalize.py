from pathlib import Path
import json,secrets,importlib.util,sys
spec=importlib.util.spec_from_file_location("trialrunner",Path(__file__).with_name("run.py"))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
e=r.OUT;packet=r.packet
assert all((e/f"route-{i}.json").exists() for i in range(1,9))
items=[]
for i in range(1,9):
 d=json.loads((e/f"route-{i}.json").read_text())
 if d["status"]=="DRAFTED":items.append((f"route-{i}",d["draft"]))
for name in ["control","telling-literal","telling-analogy","telling-documented","voice-relatable_provocateur","voice-concise_challenger","voice-reflective_leader"]:
 f=e/(name+".json")
 if f.exists():items.append((name,json.loads(f.read_text())["output"]))
mapping=e/"review-mapping.json"
if mapping.exists():mapping_data=json.loads(mapping.read_text())
else:
 secrets.SystemRandom().shuffle(items)
 mapping_data={f"D{i+1:02}":name for i,(name,body) in enumerate(items)}
 r.save(mapping,mapping_data)
byname=dict(items)
drafts={label:byname[name] for label,name in mapping_data.items()}
review="# Shuffled private writing review\n\nHuman preferences are pending. Labels identify review artifacts, not provider IDs. Preserve actual editing minutes separately from estimates.\n\n"
for label,body in drafts.items():review+="## "+label+"\n\n"+body+"\n\n"
review+="## Review questions\n\nFor each draft, paraphrase the thesis, identify the earned evidence, name a forwarding recipient/reason, flag unsupported implications, describe voice/narrative effects and required edits. Record keep/edit/reject and actual editing minutes if you edit. Leave unknowns blank.\n"
(e/"BLIND_REVIEW.md").write_text(review)
provider=r.CodexProvider(r.CodexConfig(**r.cfg),e/"attempts","eight-controls")
audit=r.call(provider,"audit","Audit all drafts only now that all eight outcomes and controls exist. Assess factual support against the supplied sources, usefulness, genuinely distinct telling versus synonyms, naturalness and specific needed edits. Cite draft labels and exact short passages. Human preference is pending. Editing effort may be estimated only with that label. Choose strongest_single_draft_label only from eligible route labels. Do not declare a winner. Identify a hybrid only if complementary strengths are demonstrable. Return artifact with findings_by_draft, comparison, strongest_single_draft_label, proposed_hybrid (null or specific steps with evidence).",{"drafts":drafts,"sources":packet["sources"],"human_preferences":None,"eligible_route_labels":[k for k,v in mapping_data.items() if v.startswith("route-")]})
artifact=audit.get("artifact",{})
proposal=artifact.get("proposed_hybrid") if isinstance(artifact,dict) else None
if proposal:
 second={"question":"What evidence should an organization require before declaring incident remediation complete?","sources":packet["sources"],"author":"Graham Hill","audience":packet["audience"],"voice":packet["voice"]}
 for name,method in [("hybrid",proposal),("single",{"reference":artifact.get("strongest_single_draft_label"),"instruction":"Use the reasoning and narrative approach of the referenced strongest individual draft, adapted to the second concept."}),("simple",{"instruction":"Direct useful source-backed explanation."})]:
  r.call(provider,"second-"+name,"Write one160-220-word private post on the second concept using the specified method. Attribute evidence. Do not invent outcome measurements. This tests transfer, not a declared winner.",{"common":second,"method":method,"reference_drafts":{artifact["strongest_single_draft_label"]:drafts[artifact["strongest_single_draft_label"]]} if name=="single" else None},True)
 r.save(e/"hybrid-status.json",{"status":"SECOND_CONCEPT_DRAFTS_RETAINED","human_preferences":None,"proposal":proposal})
else:r.save(e/"hybrid-status.json",{"status":"NO_SPECIFIC_HYBRID_PROPOSED_BY_MODEL_AUDIT","human_preferences":None})
print("Shuffled review and post-outcome audit retained")
