from workflow import AgentWorkflow, Condition, Loop, WorkflowRepository, WorkflowStep


def test_workflow_version_and_fingerprint_changes() -> None:
    workflow = AgentWorkflow(name="Invoice Bot")
    original = workflow.fingerprint()

    workflow.add_step(
        WorkflowStep(
            action="click",
            payload={"target_text": "Odeslat"},
            condition=Condition(if_text_visible="Chyba", then_action="click_ok"),
            loop=Loop(repeat=2),
        )
    )

    assert workflow.version == 2
    assert workflow.fingerprint() != original


def test_workflow_repository_roundtrip(tmp_path) -> None:
    repo = WorkflowRepository(root=str(tmp_path))
    workflow = AgentWorkflow(name="Email Flow", tags=["email", "timeless"])
    workflow.add_step(WorkflowStep(action="type", payload={"text": "Ahoj"}))

    repo.save(workflow)
    loaded = repo.load("Email Flow")

    assert loaded.name == "Email Flow"
    assert loaded.tags == ["email", "timeless"]
    assert loaded.steps[0].action == "type"
