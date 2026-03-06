from safety import SensitiveDataGuard


def test_sensitive_data_guard_redacts_email_and_password() -> None:
    guard = SensitiveDataGuard()

    value = "email john@doe.com password=secret123"
    redacted = guard.redact(value)

    assert "john@doe.com" not in redacted
    assert "secret123" not in redacted
    assert "[REDACTED]" in redacted
