import yara
import os
import time
import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MalwareScanner:
    def __init__(self, rule_file: str = "rules/malware_rules.yar"):
        self.rule_file = rule_file
        self.rules = self._compile_rules()

    def _compile_rules(self) -> yara.Rules:
        """Compiles YARA rules from the specified file."""
        if not os.path.exists(self.rule_file):
            logger.error(f"Rule file not found: {self.rule_file}")
            raise FileNotFoundError(f"Rule file not found: {self.rule_file}")
        
        try:
            return yara.compile(filepath=self.rule_file)
        except yara.SyntaxError as e:
            logger.error(f"YARA Syntax Error in {self.rule_file}: {e}")
            raise

    def scan_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Scans a single file and returns a list of matches."""
        try:
            matches = self.rules.match(filepath)
            results = []
            for match in matches:
                results.append({
                    "rule": match.rule,
                    "tags": match.tags,
                    "meta": dict(match.meta),
                    "strings": [ (s.identifier, s.instances[0].offset, s.instances[0].matched_data) for s in match.strings if s.instances ]
                })
            return results
        except Exception as e:
            logger.warning(f"Could not scan {filepath}: {e}")
            return []

    def scan_directory(self, directory: str = "samples") -> Dict[str, Any]:
        """Scans all files in a directory recursively."""
        logger.info(f"Starting scan in directory: {directory}")
        
        summary = {
            "total_files": 0,
            "threats_found": 0,
            "scan_time_seconds": 0.0,
            "matches": {}
        }

        start_time = time.time()

        if not os.path.exists(directory):
            logger.error(f"Directory not found: {directory}")
            return summary

        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                summary["total_files"] += 1
                
                matches = self.scan_file(filepath)
                if matches:
                    summary["threats_found"] += 1
                    summary["matches"][filepath] = matches
                    logger.info(f"Threat found in {filepath}: {[m['rule'] for m in matches]}")

        summary["scan_time_seconds"] = round(time.time() - start_time, 2)
        logger.info(f"Scan completed. Found {summary['threats_found']} threats in {summary['total_files']} files.")
        
        return summary

if __name__ == "__main__":
    scanner = MalwareScanner()
    report = scanner.scan_directory()
    
    print("\n" + "="*40)
    print("        SCAN RESULTS REPORT")
    print("="*40)
    print(f"Files Scanned:   {report['total_files']}")
    print(f"Threats Found:   {report['threats_found']}")
    print(f"Time Taken:      {report['scan_time_seconds']}s")
    print("-" * 40)
    
    for filepath, matches in report["matches"].items():
        print(f"\n[!] FILE: {filepath}")
        for match in matches:
            desc = match['meta'].get('description', 'No description')
            sev = match['meta'].get('severity', 'UNKNOWN')
            mitigation = match['meta'].get('mitigation', 'No mitigation strategy provided.')
            print(f"    - Rule: {match['rule']}")
            print(f"      Severity: {sev}")
            print(f"      Description: {desc}")
            print(f"      Mitigation: {mitigation}")
    print("="*40 + "\n")
