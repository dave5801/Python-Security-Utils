import os
import re

# Common patterns to catch secrets
patterns = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "AWS Secret Key": r"(?i)aws.*['\"][0-9a-zA-Z\/+=]{40}['\"]",
    "Password": r"(?i)password\s*[:=]\s*['\"][^'\"]+['\"]",
    "Secret": r"(?i)secret\s*[:=]\s*['\"][^'\"]+['\"]",
    "Token": r"(?i)token\s*[:=]\s*['\"][^'\"]+['\"]",
    "Private Key": r"-----BEGIN (RSA|DSA|EC|PGP|OPENSSH|PRIVATE) KEY-----"
}

# File extensions worth scanning
extensions = (".py", ".js", ".php", ".env", ".json", ".yml", ".sh", ".config", ".ini")

def scan_file(filepath):
    findings = []
    try:
        with open(filepath, "r", errors="ignore") as f:
            lines = f.readlines()
            for lineno, line in enumerate(lines, 1):
                for label, pattern in patterns.items():
                    if re.search(pattern, line):
                        findings.append((label, lineno, line.strip()))
    except Exception as e:
        pass
    return findings

def hunt_secrets(base_dir):
    print(f"🔍 Scanning directory: {base_dir}\n")
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(extensions):
                path = os.path.join(root, file)
                secrets = scan_file(path)
                for label, lineno, content in secrets:
                    print(f"[{label}] {path}:{lineno} → {content}")

if __name__ == "__main__":
    repo_dir = input("📁 Enter path to downloaded Git repo: ").strip()
    hunt_secrets(repo_dir)
