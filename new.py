import subprocess
import json
import os
import sys

def run_snyk_scan(target_dir="."):
    try:
        print(f"🔍 Running Snyk scan in: {os.path.abspath(target_dir)}")
        
        # Run snyk test with JSON output
        result = subprocess.run(
            ["snyk", "test", "--json"],
            cwd=target_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode not in [0, 1]:  # 1 = vulns found, 0 = no issues
            print("❌ Snyk scan failed!")
            print(result.stderr)
            sys.exit(1)

        output_json = json.loads(result.stdout)

        if "vulnerabilities" not in output_json:
            print("✅ No vulnerabilities found.")
            return

        vulns = output_json["vulnerabilities"]
        if not vulns:
            print("✅ No vulnerabilities found.")
            return

        print(f"\n🚨 Found {len(vulns)} vulnerabilities:\n")
        for v in vulns:
            print(f"📌 {v['title']} - Severity: {v['severity'].upper()}")
            print(f"   Package: {v['packageName']} | Version: {v['version']}")
            print(f"   CVE: {', '.join(v.get('identifiers', {}).get('CVE', [])) or 'N/A'}")
            print(f"   Path: {v['from']}")
            print(f"   URL: {v['url']}\n")

    except json.JSONDecodeError:
        print("❌ Could not parse Snyk output. Is Snyk CLI installed and working?")
    except FileNotFoundError:
        print("❌ Snyk CLI not found. Please install it with: npm install -g snyk")

if __name__ == "__main__":
    run_snyk_scan()  # or pass a path like run_snyk_scan("my_project/")